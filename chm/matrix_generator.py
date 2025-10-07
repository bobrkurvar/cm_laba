import numpy as np

def generate_nice_solution(n):
    nice_numbers = set()
    for i in range(-8, 9):
        nice_numbers.add(float(i))
    for denom in [2, 4, 8, 16]:
        for num in range(-8*denom, 8*denom + 1):
            if num % denom != 0:
                val = num / denom
                if abs(val) <= 8:
                    nice_numbers.add(val)
    return np.random.choice(sorted(list(nice_numbers)), n, replace=True)

def generate_system_arrays(n, coef_range=(-10,10)):
    min_coef, max_coef = coef_range
    x_exact = generate_nice_solution(n)

    # главная диагональ, не может быть 0
    b = np.random.randint(min_coef, max_coef+1, n)
    b[b==0] = 1
    b = b.astype(float)

    # поддиагональ a
    a = np.random.randint(min_coef, max_coef+1, n-1).astype(float)
    # наддиагональ c
    c = np.random.randint(min_coef, max_coef+1, n-1).astype(float)

    # первый и второй столбцы (случайные)
    p = np.random.randint(min_coef, max_coef+1, n).astype(float)
    q = np.random.randint(min_coef, max_coef+1, n).astype(float)

    # фиксированные пересечения
    p[0] = b[0]
    p[1] = a[0]
    q[0] = c[0]
    if n > 1:
        q[1] = b[1]
    if n > 2:
        q[2] = a[1]

    # создаём матрицу для вычисления f
    A = np.zeros((n,n), dtype=float)
    for i in range(n):
        A[i,i] = b[i]  # главная диагональ
        A[i,0] = p[i]  # первый столбец
        if n > 1:
            A[i,1] = q[i]  # второй столбец
        if i < n-1:
            A[i+1,i] = a[i]  # поддиагональ
        if i < n-1:
            A[i,i+1] = c[i]  # наддиагональ

    f = A @ x_exact

    return a.tolist(), b.tolist(), c.tolist(), p.tolist(), q.tolist(), f.tolist(), x_exact.tolist()


def generate_system_arrays_without_zero(n, coef_range=(-10,10)):
    min_coef, max_coef = coef_range
    x_exact = generate_nice_solution(n)

    # поддиагональ a
    a = np.random.randint(min_coef, max_coef+1, n-1).astype(float)
    # наддиагональ c
    c = np.random.randint(min_coef, max_coef+1, n-1).astype(float)

    # главная диагональ b, делаем диагонально доминирующей
    b = np.zeros(n, dtype=float)
    for i in range(n):
        lower = abs(a[i-1]) if i > 0 else 0
        upper = abs(c[i]) if i < n-1 else 0
        b[i] = lower + upper + np.random.uniform(1,5)  # запас
        # случайный знак
        if np.random.rand() > 0.5:
            b[i] *= -1

    # первый и второй столбцы (случайные)
    p = np.random.randint(min_coef, max_coef+1, n).astype(float)
    q = np.random.randint(min_coef, max_coef+1, n).astype(float)

    # фиксированные пересечения
    p[0] = b[0]
    if n > 1:
        p[1] = a[0]
    q[0] = c[0]
    if n > 1:
        q[1] = b[1]
    if n > 2:
        q[2] = a[1]

    # создаём матрицу для вычисления f
    A = np.zeros((n,n), dtype=float)
    for i in range(n):
        A[i,i] = b[i]  # главная диагональ
        A[i,0] = p[i]  # первый столбец
        if n > 1:
            A[i,1] = q[i]  # второй столбец
        if i < n-1:
            A[i+1,i] = a[i]  # поддиагональ
        if i < n-1:
            A[i,i+1] = c[i]  # наддиагональ

    f = A @ x_exact

    return a.tolist(), b.tolist(), c.tolist(), p.tolist(), q.tolist(), f.tolist(), x_exact.tolist()

if __name__ == "__main__":
    n = 10
    a,b,c,p,q,f,x = generate_system_arrays(n)

    print("a:", a)
    print("b:", b)
    print("c:", c)
    print("p:", p)
    print("q:", q)
    print("x_exact:", " ".join(f"{v:.4f}" for v in x))
    print("f:", " ".join(f"{v:.4f}" for v in f))

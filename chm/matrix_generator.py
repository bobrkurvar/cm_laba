import random

def generate_system_arrays(n, coef_range=(-10,10), decimals: int = 3):
    x = list(round(random.uniform(*coef_range), decimals) for _ in range(n))
    a = list(round(random.uniform(*coef_range), decimals) for _ in range(n - 1))
    b = list(round(random.uniform(*coef_range), decimals) for _ in range(n))
    c = list(round(random.uniform(*coef_range), decimals) for _ in range(n - 1))
    p = b[0:1] + a[0:1] + list(round(random.uniform(*coef_range), decimals) for _ in range(n-2))
    q = c[0:1] + b[1:2] + a[1:2] + list(round(random.uniform(*coef_range), decimals) for _ in range(n-3))
    f = list()
    print("a: ", a)
    print("b: ", b)
    print("c: ", c)
    print("p: ", p)
    print("q: ", q)
    for i in range(n):
        if i == 0:
            to_f = p[i] * x[0] + q[i] * x[1]
        elif i == 1:
            to_f = p[i] * x[0] + q[i] * x[1] + c[i] * x[2]
        elif i == 2:
            to_f = p[i] * x[0] + q[i] * x[1] + b[i] * x[2] + c[i] * x[3]
        elif i < n - 1:
            to_f = p[i] * x[0] + q[i] * x[1] + a[i-1] * x[i - 1] + b[i] * x[i] + c[i] * x[i + 1]
        else:
            to_f = p[i] * x[0] + q[i] * x[1] + a[i-1] * x[i - 1] + b[i] * x[i]
        f.append(to_f)
    return a, b, c, p, q, f, x

if __name__ == "__main__":
    n = 10
    a, b, c, p, q, f, x = generate_system_arrays(n)

    print("a: ", a)
    print("b: ", b)
    print("c: ", c)
    print("p: ", p)
    print("q: ", q)
    print("f: ", f)
    print("x: ", x)

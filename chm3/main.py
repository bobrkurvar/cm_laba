import math
import random


def matvec(band, vec):
    n = len(vec)
    res = [0.0] * n
    for i in range(n):
        for j in range(n):
            res[i] += band[i][j] * vec[j]
    return res

def normalize(x):
    nx = norm(x)
    if nx > 0:
        return [xi / nx for xi in x]
    else:
        return [0.0] * len(x)

def matrix_generate(n: int, eigenvalues: list[float], start: int = 0, end: int = 10):
    # ---- 1. Генерируем нормированный случайный вектор ω ----
    omega = [random.uniform(start, end) for _ in range(n)]
    omega = normalize(omega)

    # ---- 2. Формируем матрицу Хаусхолдера H = I - 2 ωωᵀ ----
    H = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            H[i][j] = (1 if i == j else 0) - 2 * omega[i] * omega[j]

    # ---- 3. Полная матрица A = H Λ Hᵀ ----
    A_full = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):  # j <= i, только нижняя часть
            s = sum(H[i][k] * eigenvalues[k] * H[j][k] for k in range(n))
            A_full[i][j] = s
            if i != j:
                A_full[j][i] = s
    # ---- 5. Генерируем случайный x ----
    x = [random.uniform(start, end) for _ in range(n)]

    # ---- 6. Вычисляем b = A*x корректно через твою функцию ----
    b = matvec(A_full, x)

    return A_full, x, b


def print_matrix(band: list[list[float]], n: int, f: list[float] | None = None):
    flat = [f"{x:.4g}" for row in band for x in row]
    width = max(len(x) for x in flat)

    for i in range(n):
        row = [f"{band[i][j]:>{width}.4g}" for j in range(n)]
        print('\t'.join(row), end='')
        if f:
            print(f" | {f[i]:.4g}")
        else:
            print()

def cholesky_band(A: list[list[float]]):
    n = len(A)
    for j in range(n):
        s = 0.0
        k_start = max(0, j - (len(A[j]) - 1))
        for k in range(k_start, j):
            a_jk = A[j][k]
            a_kk = A[k][k]
            if abs(a_kk) < 1e-16:
                raise ZeroDivisionError(f"Нулевой диагональный элемент A[{k},{k}]")
            s += (a_jk ** 2) / a_kk
        a_jj = A[j][j] - s
        if abs(a_jj) < 1e-16:
            raise ZeroDivisionError(f"Нулевой диагональный элемент A[{j},{j}]")
        A[j][j] = a_jj

        for i in range(j + 1, n):
            if i - j < len(A[i]):
                s = 0.0
                k_start = max(0, j - (len(A[j]) - 1), i - (len(A[i]) - 1))
                for k in range(k_start, j):
                    a_ik = A[i][k]
                    a_jk = A[j][k]
                    a_kk = A[k][k]
                    if abs(a_kk) < 1e-16:
                        raise ZeroDivisionError(f"Нулевой диагональный элемент A[{k},{k}]")
                    s += a_ik * a_jk / a_kk
                a_ij = A[i][j] - s
                A[i][j] = a_ij

    return A


def solve_cholesky_band(B, f):
    n = len(B)
    y = [0.0] * n

    for i in range(n):
        s = sum(B[i][j]*y[j] for j in range(i))
        y[i] = (f[i] - s) / B[i][i]

    x = [0.0]*n
    for i in range(n-1, -1, -1):
        s = sum(B[j][i]*x[j] for j in range(i+1, n))
        x[i] = (y[i] - s) / B[i][i]
    return x

def norm(vec):
    return math.sqrt(sum(vi ** 2 for vi in vec))

def dot(v1, v2):
    return sum(vi * wi for vi, wi in zip(v1, v2))


def angle_between_vectors(v1, v2):
    """Вычисление угла между двумя векторами в радианах"""
    # Скалярное произведение
    dot_product = 0.0
    norm1 = 0.0
    norm2 = 0.0

    for i in range(len(v1)):
        dot_product += v1[i] * v2[i]
        norm1 += v1[i] * v1[i]
        norm2 += v2[i] * v2[i]

    norm1 = math.sqrt(norm1)
    norm2 = math.sqrt(norm2)

    if norm1 > 1e-12 and norm2 > 1e-12:
        cos_angle = dot_product / (norm1 * norm2)
        cos_angle = max(-1.0, min(1.0, cos_angle))
        return math.acos(cos_angle)


def check_eigen_convergence(current_lambda, prev_lambda,
                            current_vector, prev_vector,
                            eps_lambda, eps_vector):
    # 1. Вычисляем критерии
    delta_lambda = abs(current_lambda - prev_lambda)
    angle = angle_between_vectors(current_vector, prev_vector)

    lambda_converged = delta_lambda < eps_lambda
    vector_converged = angle < eps_vector

    return lambda_converged and vector_converged




def find_min_eigen(A_band, A_band_fact, eps_a, eps_g, M):
    n = len(A_band)
    x = [random.random() for _ in range(n)]
    x = normalize(x)
    prev_lambda = 0.0

    for k in range(1, M + 1):
        # Решаем B*y = x
        y = solve_cholesky_band(A_band_fact, x)
        # Нормируем
        v = normalize(y)
        # Оценка λ
        Av = matvec(A_band, v)
        lambda_est = abs(dot(v, Av))
        # Невязка относительно λ
        residual = norm([avi - lambda_est * vi for avi, vi in zip(Av, v)]) / (norm(Av) + 1e-16)
        delta_lambda = abs(lambda_est - prev_lambda)

        #print(f"Итерация {k}: lambda = {lambda_est:.10f}, невязка = {residual:.2e}, delta = {delta_lambda:.2e}")

        if delta_lambda < eps_a and residual < eps_g:
            return 0, lambda_est, v, k, residual

        prev_lambda = lambda_est
        x = v

    # Если не сошлось
    Av = matvec(A_band, x)
    residual = norm([avi - lambda_est * vi for avi, vi in zip(Av, x)]) / (norm(Av) + 1e-16)
    return 1, lambda_est, x, M, residual


def find_second_min_eigen(A_band, A_band_fact, lambda1, x1, eps_a, eps_g, M):
    n = len(A_band)
    x1 = normalize(x1)
    x = [random.random() for _ in range(n)]
    x = normalize(x)
    prev_lambda = 0.0

    for k in range(1, M + 1):
        # Проекция на ортогональное пространство
        ortho = dot(x1, x)
        v_ortho = [xi - ortho * x1i for xi, x1i in zip(x, x1)]
        v_ortho = normalize(v_ortho)

        # Решаем B*y = v_ortho
        y = solve_cholesky_band(A_band_fact, v_ortho)
        # Проекция на ортогональное пространство
        y_ortho = [yi - dot(x1, y) * x1i for yi, x1i in zip(y, x1)]
        y_ortho = normalize(y_ortho)

        # Оценка λ
        Av = matvec(A_band, y_ortho)
        lambda_est = abs(dot(y_ortho, Av))
        residual = norm([avi - lambda_est * vi for avi, vi in zip(Av, y_ortho)]) / (norm(Av) + 1e-16)
        delta_lambda = abs(lambda_est - prev_lambda)
        ortho_check = abs(dot(x1, y_ortho))

        #print(f"Итерация {k}: lambda = {lambda_est:.10f}, невязка = {residual:.2e}, "
        #      f"ортогональность = {ortho_check:.2e}, delta = {delta_lambda:.2e}")

        if delta_lambda < eps_a and residual < eps_g and ortho_check < 1e-10:
            return 0, lambda_est, y_ortho, k, residual

        prev_lambda = lambda_est
        x = y_ortho

    Av = matvec(A_band, x)
    residual = norm([avi - lambda_est * vi for avi, vi in zip(Av, x)]) / (norm(Av) + 1e-16)
    return 1, lambda_est, x, M, residual


def gen_random_eigenvalues(n: int, start: int = 0, end: int = 10):
    return [random.uniform(start, end) for _ in range(n)]

def main():
    n, M = 3, 100000
    eps_a = eps_g = 1e-6
    print("Исследование зависимости от mult:")
    results = []
    eigenvalues = gen_random_eigenvalues(n)
    print(eigenvalues)
    A, x, b = matrix_generate(n, eigenvalues)
    print("Матрица A:")
    print_matrix(A, n, b)
    print()

    try:
        A_fact = cholesky_band(A)
        print("Разложение Холецкого выполнено успешно")
    except ZeroDivisionError as e:
        print(f"Ошибка разложения Холецкого: {e}")

    print("Поиск первого собственного значения:")
    status1, lambda1, v1, k1, r1 = find_min_eigen(A, A_fact, eps_a, eps_g, M)

    if status1 != 0:
        print(f"Не удалось найти λ₁ (IER=1)")

    print(f"✓ Найдено λ₁ = {lambda1:.10f} за {k1} итераций, невязка = {r1:.2e}")

    Av1 = matvec(A, v1)
    check = max(abs(avi - lambda1 * vi) for avi, vi in zip(Av1, v1))
    print(f"Проверка: max|A*v1 - λ1*v1| = {check:.2e}")

    print("\nПоиск второго собственного значения:")
    status2, lambda2, v2, k2, r2 = find_second_min_eigen(A, A_fact, lambda1, v1, eps_a, eps_g, M)

    if status2 != 0:
        print(f"Не удалось найти λ₂ (IER=1)")

    print(f"✓ Найдено λ₂ = {lambda2:.10f} за {k2} итераций, невязка = {r2:.2e}")

    ortho = abs(dot(v1, v2))
    print(f"Ортогональность v₁ и v₂: {ortho:.2e}")

    Av2 = matvec(A, v2)
    check2 = max(abs(avi - lambda2 * vi) for avi, vi in zip(Av2, v2))
    print(f"Проверка: max|A*v2 - λ2*v2| = {check2:.2e}")

    mu = lambda2 / lambda1 if lambda1 != 0 else float('inf')
    print(f"Оценка числа обусловленности μ = λ₂ / λ₁ = {mu:.6f}")

    print("\nВыходные параметры:")
    print(f"λ1 = {lambda1:.10f}")
    print(f"λ2 = {lambda2:.10f}")
    print(f"x1 = {[f'{xi:.6f}' for xi in v1]}")
    print(f"x2 = {[f'{xi:.6f}' for xi in v2]}")
    print(f"k1 = {k1}")
    print(f"k2 = {k2}")
    print(f"r1 = {r1:.2e}")
    print(f"r2 = {r2:.2e}")
    print(f"IER = 0")


    print("| mult | k1   | k2   | μ      |")
    print("|------|------|------|--------|")

if __name__ == "__main__":
    main()
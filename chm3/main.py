import math
import random

def get(i, j, band):
    if i < j:
        i, j = j, i
    d = i - j
    if d < len(band[i]):
        return band[i][-d - 1]
    else:
        return 0.0

def set_in_band(i, j, band, value):
    if i < j:
        i, j = j, i
    d = i - j
    if d < len(band[i]):
        band[i][-d - 1] = value

def matrix_generate(n: int, l: int, start: float = 1, end: float = 10, mult: int | None = None):
    result = []
    x = [random.uniform(start, end) for _ in range(n)]
    l -= 1
    for i in range(n):
        j = 0
        row = []
        while j <= l and j <= i:
            elem = random.uniform(start, end)
            row.append(elem)
            j += 1
        result.append(row)
        if mult is not None:
            row[-1] *= 10 ** (-2*mult)

    b = [0.0] * n
    for i in range(n):
        for j in range(n):
            b[i] += get(i, j, result) * x[j]
    return result, x, b

def print_like_full_matrix(band: list[list[float]], n: int, f: list[float] | None = None):
    flat = [f"{x:.4g}" for row in band for x in row]
    width = max(len(x) for x in flat)

    for i in range(n):
        row = [f"{get(i, j, band):>{width}.4g}" for j in range(n)]
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
            a_jk = get(j, k, A)
            a_kk = get(k, k, A)
            if abs(a_kk) < 1e-16:
                raise ZeroDivisionError(f"Нулевой диагональный элемент A[{k},{k}]")
            s += (a_jk ** 2) / a_kk
        a_jj = get(j, j, A) - s
        if abs(a_jj) < 1e-16:
            raise ZeroDivisionError(f"Нулевой диагональный элемент A[{j},{j}]")
        set_in_band(j, j, A, a_jj)

        for i in range(j + 1, n):
            if i - j < len(A[i]):
                s = 0.0
                k_start = max(0, j - (len(A[j]) - 1), i - (len(A[i]) - 1))
                for k in range(k_start, j):
                    a_ik = get(i, k, A)
                    a_jk = get(j, k, A)
                    a_kk = get(k, k, A)
                    if abs(a_kk) < 1e-16:
                        raise ZeroDivisionError(f"Нулевой диагональный элемент A[{k},{k}]")
                    s += a_ik * a_jk / a_kk
                aij = get(i, j, A) - s
                set_in_band(i, j, A, aij)

    return A


def solve_cholesky_band(B: list[list[float]], f: list[float]) -> list[float]:
    n = len(B)

    y = [0.0] * n
    for i in range(n):
        s = 0.0
        j_start = max(0, i - (len(B[i]) - 1))
        for j in range(j_start, i):
            s += get(i, j, B) * y[j]
        bii = get(i, i, B)
        if abs(bii) < 1e-16:
            raise ZeroDivisionError(f"Нулевой диагональный элемент B[{i},{i}]")
        y[i] = (f[i] - s) / bii

    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = 0.0
        bii = get(i, i, B)
        if abs(bii) < 1e-16:
            raise ZeroDivisionError(f"Нулевой диагональный элемент B[{i},{i}]")
        for j in range(i + 1, n):
            if j - i < len(B[j]):
                b_ji = get(j, i, B)
                s += (b_ji / bii) * x[j]
        x[i] = y[i] - s

    return x

def norm(vec):
    return math.sqrt(sum(vi ** 2 for vi in vec))

def dot(v1, v2):
    return sum(vi * wi for vi, wi in zip(v1, v2))

def matvec(band, vec):
    n = len(vec)
    res = [0.0] * n
    for i in range(n):
        offset = len(band[i]) - 1
        for jj in range(len(band[i])):
            j = i - offset + jj
            res[i] += band[i][jj] * vec[j]
        for j in range(i + 1, n):
            d = j - i
            if d < len(band[j]):
                val = band[j][-d - 1]
                res[i] += val * vec[j]
    return res

def find_min_eigen(A_band: list[list[float]], A_band_fact: list[list[float]],
                   eps_a: float, eps_g: float, M: int) -> tuple[int, float, list[float], int, float]:
    n = len(A_band)
    x = [random.random() for _ in range(n)]
    nx = norm(x)
    if nx > 0:
        x = [xi / nx for xi in x]
    else:
        x = [0.0] * n
    k = 0
    lambda_est = 0.0
    prev_lambda = float('inf')
    while k < M:
        nv = norm(x)
        if nv > 0:
            v = [xi / nv for xi in x]
        else:
            v = [0.0] * n
        right_hand = v[:]
        y = solve_cholesky_band(A_band_fact, right_hand)
        alpha = dot(v, y)
        if abs(alpha) < 1e-16:
            return 2, 0.0, v, k, float('inf')  # ошибка: alpha=0
        lambda_est = 1 / alpha
        av = matvec(A_band, v)
        residual = norm([avi - lambda_est * vi for avi, vi in zip(av, v)])
        delta_lambda = abs(lambda_est - prev_lambda)
        if delta_lambda < eps_a and residual < eps_g:
            return 0, lambda_est, v, k + 1, residual
        prev_lambda = lambda_est
        x = y[:]
        k += 1
    return 1, lambda_est, v, k, residual

def find_second_min_eigen(A_band: list[list[float]], A_band_fact: list[list[float]],
                          lambda1: float, x1: list[float],
                          eps_a: float, eps_g: float, M: int) -> tuple[int, float, list[float], int, float]:
    n = len(A_band)
    x = [random.random() for _ in range(n)]
    nx = norm(x)
    if nx > 0:
        x = [xi / nx for xi in x]
    else:
        x = [0.0] * n
    k = 0
    lambda_est = 0.0
    prev_lambda = float('inf')
    nx1 = norm(x1)
    if nx1 > 0:
        x1 = [xi / nx1 for xi in x1]
    else:
        x1 = [0.0] * n
    while k < M:
        nv = norm(x)
        if nv > 0:
            v = [xi / nv for xi in x]
        else:
            v = [0.0] * n
        vt = dot(x1, v)
        right_hand = [vi - vt * x1i for vi, x1i in zip(v, x1)]
        y = solve_cholesky_band(A_band_fact, right_hand)
        alpha = dot(v, y)
        if abs(alpha) < 1e-16:
            return 2, 0.0, v, k, float('inf')  # ошибка: alpha=0
        lambda_est = 1 / alpha
        av = matvec(A_band, v)
        residual = norm([avi - lambda_est * vi for avi, vi in zip(av, v)])
        delta_lambda = abs(lambda_est - prev_lambda)
        if delta_lambda < eps_a and residual < eps_g:
            return 0, lambda_est, v, k + 1, residual
        prev_lambda = lambda_est
        x = y[:]
        k += 1
    return 1, lambda_est, v, k, residual
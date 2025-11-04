from random import randint
from typing import List

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

def copy_band_structure_like(A: List[List[float]]) -> List[List[float]]:
    return [[0.0] * len(row) for row in A]

def matrix_generate(n: int, l: int, mult: int | None = None):
    result = []
    x = [randint(1, 15) for _ in range(n)]

    for i in range(n):
        j = 0
        row = []
        while j <= l and j <= i:
            elem = randint(1, 15)
            row.append(elem)
            j += 1
        result.append(row)
        if mult is not None:
            row[-1] *= 10 ** (-2 * mult)

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

def cholesky_band(A: List[List[float]]):
    n = len(A)
    B = copy_band_structure_like(A)

    for j in range(n):
        # Диагональ b_jj по формуле (1.1.11)
        s = 0.0
        k_start = max(0, j - (len(B[j]) - 1))
        for k in range(k_start, j):
            b_jk = get(j, k, B)
            b_kk = get(k, k, B)
            if abs(b_kk) < 1e-16:
                raise ZeroDivisionError(f"Нулевой диагональный элемент B[{k},{k}]")
            s += (b_jk ** 2) / b_kk
        b_jj = get(j, j, A) - s
        # Нет проверки на b_jj < 0, только на zero
        if abs(b_jj) < 1e-16:
            raise ZeroDivisionError(f"Нулевой диагональный элемент B[{j},{j}]")
        set_in_band(j, j, B, b_jj)

        # Поддиагональные b_ij по формуле (1.1.11)
        for i in range(j + 1, n):
            if i - j < len(A[i]):
                s = 0.0
                k_start = max(0, j - (len(B[j]) - 1), i - (len(B[i]) - 1))
                for k in range(k_start, j):
                    b_ik = get(i, k, B)
                    b_jk = get(j, k, B)
                    b_kk = get(k, k, B)
                    if abs(b_kk) < 1e-16:
                        raise ZeroDivisionError(f"Нулевой диагональный элемент B[{k},{k}]")
                    s += b_ik * b_jk / b_kk
                bij = get(i, j, A) - s
                set_in_band(i, j, B, bij)

    return B

def solve_cholesky_band(B: List[List[float]], f: List[float]) -> List[float]:
    n = len(B)
    # Прямой ход: B y = f по (1.1.12)
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

    # Обратный ход: C x = y, с c_ij = b_ji / b_ii на лету по (1.1.12)
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

def main():
    n, l = 8, 4
    A, x_true, f = matrix_generate(n, l)

    print("Сгенерированная матрица A (полная):")
    print_like_full_matrix(A, n, f)
    print("\nИстинное решение x:", x_true)

    B = cholesky_band(A)
    x_sol = solve_cholesky_band(B, f)

    print("\nНижняя B (лента):")
    print(B)

    print("\nРешение x_sol:", [round(v, 8) for v in x_sol])
    print("Разность x_sol - x_true:", [x_sol[i] - x_true[i] for i in range(n)])

if __name__ == "__main__":
    main()
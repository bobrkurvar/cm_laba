from random import uniform
from typing import List
import pandas as pd

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
    x = [uniform(start, end) for _ in range(n)]

    for i in range(n):
        j = 0
        row = []
        while j <= l and j <= i:
            elem = uniform(start, end)
            row.append(elem)
            j += 1
        result.append(row)
        if mult is not None:
            row[-1] *= 10 ** (-mult)

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

    for j in range(n):
        # Диагональ A[j][j] по формуле (1.1.11)
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

        # Поддиагональные элементы A[i][j]
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


def relative_error(x_true, x_calc):
    diffs = [abs(x_calc[i] - x_true[i]) / (abs(x_true[i]) + 1e-12) for i in range(len(x_true))]
    return sum(diffs) / len(diffs)


def run_band_tests(l: bool = True):
    tests = []
    Ns = [10, 100] if l else [10, 40, 100, 200]
    for N in Ns:
        if l:
            if N == 10:
                L_values = [1, 8]
            elif N == 40:
                L_values = [4, 38]
            elif N == 100:
                L_values = [10, 90]
            elif N == 200:
                L_values = [2, 190]
            else:
                continue
        else:
            L_values = [N]

        for L in L_values:
            print(f"\n=== ТЕСТ ДЛЯ N={N}, L={L} ===")

            A, x_true, f = matrix_generate(N, L, start=1e-1, end=1e1)

            if N == 10:
                print("\nСгенерированная матрица A:")
                print_like_full_matrix(A, N, f)
                print()

            cholesky_band(A)
            x_sol = solve_cholesky_band(A, f)
            err = relative_error(x_true, x_sol)

            print("Истинное решение x_true:", [round(v, 4) for v in x_true])
            print("Найденное решение x_sol:", [round(v, 4) for v in x_sol])
            diff = [x_sol[i] - x_true[i] for i in range(N)]
            print("Разность (x_sol - x_true):", diff)
            print(f"Средняя относительная погрешность: {err:.4e}\n")

            to_test = {
                "№ теста": len(tests) + 1,
                "Размерность системы": N,
                "Средняя относительная погрешность решения": err
            }
            if l:
                to_test["Отношение L/N"] = round(L / N, 4)
            tests.append(to_test)

    df = pd.DataFrame(tests)
    print("\nРезультаты тестов:\n", df)
    file = "band_test_results_l_true.tex" if l else "band_test_results_l_false.tex"
    latex_table = df.to_latex(index=False, float_format="%.4e", escape=False)
    with open(f"C:\\Users\\Andy\\Desktop\\{file}.tex", "w", encoding="utf-8") as f:
        f.write(latex_table)

    print("\nТаблица сохранена в файл 'band_test_results.tex'")
    return df

def run_bad_band_tests():
    tests = []
    k = [2, 4, 6]
    Ns = [10, 40]
    for N in Ns:
        for i in k:
            print(f"\n=== ТЕСТ ДЛЯ N={N}, L={N} K={k}===")
            A, x_true, f = matrix_generate(N, N, start=1e-1, end=1e1, mult=i)

            if N == 10:
                print("\nСгенерированная матрица A:")
                print_like_full_matrix(A, N, f)
                print()

            cholesky_band(A)
            x_sol = solve_cholesky_band(A, f)
            err = relative_error(x_true, x_sol)

            print("Истинное решение x_true:", [round(v, 4) for v in x_true])
            print("Найденное решение x_sol:", [round(v, 4) for v in x_sol])
            diff = [x_sol[i] - x_true[i] for i in range(N)]
            print("Разность (x_sol - x_true):", diff)
            print(f"Средняя относительная погрешность: {err:.4e}\n")

            to_test = {
                "№ теста": len(tests) + 1,
                "Порядок k": i,
                "Размерность системы": N,
                "Средняя относительная погрешность решения": err
            }
            tests.append(to_test)

    df = pd.DataFrame(tests)
    print("\nРезультаты тестов:\n", df)
    file = "band_test_results_l_bad.tex"
    latex_table = df.to_latex(index=False, float_format="%.4e", escape=False)
    with open(f"C:\\Users\\Andy\\Desktop\\{file}.tex", "w", encoding="utf-8") as f:
        f.write(latex_table)

    print("\nТаблица сохранена в файл 'band_test_results.tex'")
    return df

def main():
    n, l = 8, 4
    A, x_true, f = matrix_generate(n, l)

    print("Сгенерированная матрица A (полная):")
    print_like_full_matrix(A, n, f)
    print("\nИстинное решение x:", [round(x, 3) for x in x_true])
    print()

    cholesky_band(A)
    x_sol = solve_cholesky_band(A, f)


    print("\nРешение x_sol:", [round(v, 3) for v in x_sol])
    print("Разность x_sol - x_true:", [x_sol[i] - x_true[i] for i in range(n)])


    print("\n\n=== ТЕСТЫ С ОТНОШЕНИЯМИ L/N ===")
    run_band_tests()

    print("\n\n=== ТЕСТЫ ДЛЯ СЛУЧАЯ L = N ===")
    run_band_tests(l=False)

    print("\n\n=== ТЕСТЫ ДЛЯ СЛУЧАЯ L = N С ПЛОХООБУСЛОВЛЕННОЙ МАТРИЦЕЙ===")
    run_bad_band_tests()

if __name__ == "__main__":
    main()
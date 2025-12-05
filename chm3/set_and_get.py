# import math
# import random
#
# # --- Работа с нижнетреугольной матрицей ---
# def get(i, j, band):
#     if i < j:
#         i, j = j, i
#     return band[i][j]
#
# def set_in_band(i, j, band, value):
#     if i < j:
#         i, j = j, i
#     band[i][j] = value
#
# # --- Векторные операции ---
# def norm(vec):
#     return math.sqrt(sum(vi ** 2 for vi in vec))
#
# def dot(v1, v2):
#     return sum(vi * wi for vi, wi in zip(v1, v2))
#
# def normalize(x):
#     nx = norm(x)
#     if nx > 0:
#         return [xi / nx for xi in x]
#     else:
#         return [0.0] * len(x)
#
# # --- Умножение матрицы на вектор через get ---
# def matvec(band, vec):
#     n = len(vec)
#     res = [0.0] * n
#     for i in range(n):
#         for j in range(n):
#             res[i] += get(i, j, band) * vec[j]
#     return res
#
# # --- Генерация полной симметричной матрицы ---
# def matrix_generate(n: int, eigenvalues: list[float], start: int = 0, end: int = 10):
#     # ---- 1. Генерируем нормированный случайный вектор ω ----
#     omega = [random.uniform(start, end) for _ in range(n)]
#     omega = normalize(omega)
#
#     # ---- 2. Формируем матрицу Хаусхолдера H = I - 2 ωωᵀ ----
#     H = [[0.0] * n for _ in range(n)]
#     for i in range(n):
#         for j in range(n):
#             H[i][j] = (1 if i == j else 0) - 2 * omega[i] * omega[j]
#
#     # ---- 3. Полная симметричная матрица A ----
#     A_full = [[0.0] * n for _ in range(n)]
#     for i in range(n):
#         for j in range(i + 1):
#             s = sum(H[i][k] * eigenvalues[k] * H
#
#             A_full[i][j] = s
#             if i != j:
#                 A_full[j][i] = s
#
#     # Храним только нижнюю треугольную часть
#     A_band = [[A_full[i][j] if j <= i else 0.0 for j in range(i + 1)] for i in range(n)]
#
#     # ---- 5. Генерируем случайный вектор x ----
#     x = [random.uniform(start, end) for _ in range(n)]
#
#     # ---- 6. Вычисляем b = A*x через matvec ----
#     b = matvec(A_band, x)
#
#     return A_band, x, b
#
# # --- Печать нижнетреугольной матрицы ---
# def print_matrix(band, n, f=None):
#     flat = [f"{get(i,j,band):.4g}" for i in range(n) for j in range(n)]
#     width = max(len(x) for x in flat)
#     for i in range(n):
#         row = [f"{get(i,j,band):>{width}.4g}" for j in range(n)]
#         print('\t'.join(row), end='')
#         if f:
#             print(f" | {f[i]:.4g}")
#         else:
#             print()
#
# # --- Разложение Холецкого для нижней матрицы ---
# def cholesky_band(A):
#     n = len(A)
#     for j in range(n):
#         s = 0.0
#         for k in range(j):
#             a_jk = get(j, k, A)
#             a_kk = get(k, k, A)
#             if abs(a_kk) < 1e-16:
#                 raise ZeroDivisionError(f"Нулевой диагональный элемент A[{k},{k}]")
#             s += (a_jk ** 2) / a_kk
#         a_jj = get(j, j, A) - s
#         if abs(a_jj) < 1e-16:
#             raise ZeroDivisionError(f"Нулевой диагональный элемент A[{j},{j}]")
#         set_in_band(j, j, A, a_jj)
#
#         for i in range(j + 1, n):
#             s = 0.0
#             for k in range(j):
#                 s += get(i, k, A) * get(j, k, A) / get(k, k, A)
#             a_ij = get(i, j, A) - s
#             set_in_band(i, j, A, a_ij)
#     return A
#
# # --- Решение системы через разложение Холецкого ---
# def solve_cholesky_band(B, f):
#     n = len(B)
#     y = [0.0] * n
#     # Прямой ход L*y = f
#     for i in range(n):
#         s = sum(get(i,j,B)*y[j] for j in range(i))
#         y[i] = (f[i] - s) / get(i,i,B)
#     # Обратный ход Lᵀ*x = y
#     x = [0.0] * n
#     for i in range(n-1, -1, -1):
#         s = sum(get(j,i,B)*x[j] for j in range(i+1,n))
#         x[i] = (y[i] - s) / get(i,i,B)
#     return x
#
# # --- Поиск минимального собственного значения ---
# def find_min_eigen(A_band, A_band_fact, eps_a, eps_g, M):
#     n = len(A_band)
#     x = normalize([random.random() for _ in range(n)])
#     prev_lambda = 0.0
#     for k in range(1, M+1):
#         y = solve_cholesky_band(A_band_fact, x)
#         v = normalize(y)
#         Av = matvec(A_band, v)
#         lambda_est = abs(dot(v, Av))
#         residual = norm([avi - lambda_est * vi for avi, vi in zip(Av, v)]) / (norm(Av)+1e-16)
#         delta_lambda = abs(lambda_est - prev_lambda)
#         if delta_lambda < eps_a and residual < eps_g:
#             return 0, lambda_est, v, k, residual
#         prev_lambda = lambda_est
#         x = v
#     Av = matvec(A_band, x)
#     residual = norm([avi - lambda_est * vi for avi, vi in zip(Av, x)]) / (norm(Av)+1e-16)
#     return 1, lambda_est, x, M, residual
#
# # --- Поиск второго минимального собственного значения ---
# def find_second_min_eigen(A_band, A_band_fact, lambda1, x1, eps_a, eps_g, M):
#     n = len(A_band)
#     x1 = normalize(x1)
#     x = normalize([random.random() for _ in range(n)])
#     prev_lambda = 0.0
#     for k in range(1, M+1):
#         ortho = dot(x1, x)
#         v_ortho = normalize([xi - ortho*x1i for xi, x1i in zip(x, x1)])
#         y = solve_cholesky_band(A_band_fact, v_ortho)
#         y_ortho = normalize([yi - dot(x1, y)*x1i for yi, x1i in zip(y, x1)])
#         Av = matvec(A_band, y_ortho)
#         lambda_est = abs(dot(y_ortho, Av))
#         residual = norm([avi - lambda_est * vi for avi, vi in zip(Av, y_ortho)]) / (norm(Av)+1e-16)
#         delta_lambda = abs(lambda_est - prev_lambda)
#         ortho_check = abs(dot(x1, y_ortho))
#         if delta_lambda < eps_a and residual < eps_g and ortho_check < 1e-10:
#             return 0, lambda_est, y_ortho, k, residual
#         prev_lambda = lambda_est
#         x = y_ortho
#     Av = matvec(A_band, x)
#     residual = norm([avi - lambda_est * vi for avi, vi in zip(Av, x)]) / (norm(Av)+1e-16)
#     return 1, lambda_est, x, M, residual
#
# # --- Генерация случайных собственных значений ---
# def gen_random_eigenvalues(n, start=0, end=10):
#     return [random.uniform(start, end) for _ in range(n)]
#
# # --- Основная программа ---
# def main():
#     n, M = 3, 100000
#     eps_a = eps_g = 1e-6
#     eigenvalues = gen_random_eigenvalues(n)
#     print("Случайные собственные значения:", eigenvalues)
#     A_band, x, b = matrix_generate(n, eigenvalues)
#     print("Матрица A (нижняя часть):")
#     print_matrix(A_band, n, b)
#     print()
#     try:
#         A_fact = cholesky_band(A_band)
#         print("Разложение Холецкого выполнено успешно")
#     except ZeroDivisionError as e:
#         print(f"Ошибка разложения Холецкого: {e}")
#
#     print("Поиск первого собственного значения:")
#     status1, lambda1, v1, k1, r1 = find_min_eigen(A_band, A_fact, eps_a, eps_g, M)
#     print(f"λ₁ = {lambda1:.10f}, итерации = {k1}, невязка = {r1:.2e}")
#
#     print("Поиск второго собственного значения:")
#     status2, lambda2, v2, k2, r2 = find_second_min_eigen(A_band, A_fact, lambda1, v1, eps_a, eps_g, M)
#     print(f"λ₂ = {lambda2:.10f}, итерации = {k2}, невязка = {r2:.2e}")
#
# if __name__ == "__main__":
#     main()

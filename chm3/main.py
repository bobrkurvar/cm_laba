import math
import random
import copy
import pandas as pd


def matvec(A, vec):
    n = len(vec)
    res = [0.0] * n
    for i in range(n):
        s = 0.0
        row = A[i]
        for j in range(n):
            s += row[j] * vec[j]
        res[i] = s
    return res

def norm(x):
    return math.sqrt(sum(xi*xi for xi in x))

def normalize(x):
    nx = norm(x)
    if nx > 0:
        return [xi/nx for xi in x]
    else:
        return [0.0]*len(x)

def dot(v1, v2):
    return sum(a*b for a,b in zip(v1,v2))

def angle_between_vectors(v1, v2):
    """Вычисление угла между двумя векторами в радианах"""
    # Скалярное произведение
    # dot_product = 0.0
    # norm1 = 0.0
    # norm2 = 0.0
    #
    # for i in range(len(v1)):
    #     dot_product += v1[i] * v2[i]
    #     norm1 += v1[i] * v1[i]
    #     norm2 += v2[i] * v2[i]
    #
    # norm1 = math.sqrt(norm1)
    # norm2 = math.sqrt(norm2)
    #
    # if norm1 > 1e-12 and norm2 > 1e-12:
    #     cos_angle = dot_product / (norm1 * norm2)
    #     cos_angle = max(-1.0, min(1.0, cos_angle))
    #     return math.acos(cos_angle)
    # else:
    #     return math.pi  # Фикс: возвращаем большой угол при нулевых нормах
    dot_product = sum(a*b for a, b in zip(v1, v2))
    norm1 = math.sqrt(sum(a*a for a in v1))
    norm2 = math.sqrt(sum(b*b for b in v2))

    if norm1 < 1e-12 or norm2 < 1e-12:
        return math.pi

    cosv = abs(dot_product) / (norm1 * norm2)
    cosv = max(-1.0, min(1.0, cosv))
    return math.acos(cosv)

def matrix_generate(n: int, eigenvalues: list[float], start: int = 1, end: int = 10):
    omega = [random.uniform(start, end) for _ in range(n)]
    omega = normalize(omega)
    # H = I - 2 ω ω^T
    H = [[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            H[i][j] = (1.0 if i==j else 0.0) - 2.0 * omega[i] * omega[j]
    # A = H * diag(eigenvalues) * H^T
    A = [[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1):
            s = 0.0
            for k in range(n):
                s += H[i][k] * eigenvalues[k] * H[j][k]
            A[i][j] = s
            A[j][i] = s
    x_true = [random.uniform(start, end) for _ in range(n)]
    b = matvec(A, x_true)
    return A, x_true, b, H, eigenvalues

def cholesky_full(A):
    n = len(A)
    for j in range(n):
        s = 0.0
        for k in range(j):
            a_jk = A[j][k]
            a_kk = A[k][k]
            if abs(a_kk) < 1e-16:
                raise ZeroDivisionError(f"Нулевой диагональный элемент A[{k},{k}]")
            s += (a_jk ** 2) / a_kk
        a_jj = A[j][j] - s
        if abs(a_jj) < 1e-16:
            raise ZeroDivisionError(f"Нулевой диагональный элемент A[{j},{j}]")
        A[j][j] = a_jj
        for i in range(j+1, n):
            s = 0.0
            for k in range(j):
                s += A[i][k] * A[j][k] / A[k][k]
            A[i][j] = A[i][j] - s
    return A


def solve_cholesky_band(B, f):
    n = len(B)
    y = [0.0]*n
    for i in range(n):
        s = 0.0
        for j in range(i):
            s += B[i][j] * y[j]
        y[i] = (f[i] - s) / B[i][i]
    x = [0.0]*n
    for i in range(n-1, -1, -1):
        s = 0.0
        for j in range(i+1, n):
            s += (B[j][i] / B[i][i]) * x[j]
        x[i] = y[i] - s
    return x


def check_eigen_convergence(current_lambda, prev_lambda, current_vector, prev_vector, eps_lambda, eps_vector):
    delta_lambda = abs(current_lambda - prev_lambda)
    angle = angle_between_vectors(current_vector, prev_vector)
    return (delta_lambda < eps_lambda) and (angle < eps_vector)


def find_min_eigen(A, A_fact, eps_a, eps_g, M):
    n = len(A)
    x = normalize([random.random() for _ in range(n)])
    prev_lambda = 0.0
    prev_v = [0.0] * n
    iteration_log = []

    for k in range(1, M+1):
        y = solve_cholesky_band(A_fact, x)
        v = normalize(y)
        Av = matvec(A, v)
        lambda_est = dot(v, Av)
        residual_vec = [avi - lambda_est * vi for avi,vi in zip(Av,v)]
        r = max(abs(c) for c in residual_vec)
        delta = abs(lambda_est - prev_lambda) if k>1 else None
        angle = angle_between_vectors(v, prev_v) if k>1 else None

        delta_str = f"{delta:.2e}" if delta is not None else "  —  "
        angle_str = f"{angle:.2e} rad" if angle is not None else "  —  "
        print(f"[k={k:3d}] λ={lambda_est:.10f}  Δλ={delta_str}  angle={angle_str}  r={r:.2e}")
        iteration_log.append((k, lambda_est, delta, angle, r))
        if k>1 and check_eigen_convergence(lambda_est, prev_lambda, v, prev_v, eps_a, eps_g):
            return 0, lambda_est, v, k, r, iteration_log
        prev_lambda = lambda_est
        prev_v = v[:]
        x = v
    return 1, lambda_est, x, M, r, iteration_log


def find_second_min_eigen(A, A_fact, lambda1, x1, eps_a, eps_g, M):
    n = len(A)
    x1 = normalize(x1)
    x = normalize([random.random() for _ in range(n)])
    prev_lambda = 0.0
    prev_v = [0.0]*n
    iteration_log = []

    for k in range(1, M+1):

        c = dot(x1, x)
        v_temp = [xi - c * x1i for xi, x1i in zip(x, x1)]
        c = dot(x1, v_temp)
        v_temp = [vi - c * x1i for vi, x1i in zip(v_temp, x1)]
        v_ortho = normalize(v_temp)
        y = solve_cholesky_band(A_fact, v_ortho)
        c = dot(x1, y)
        y_temp = [yi - c * x1i for yi, x1i in zip(y, x1)]
        c = dot(x1, y_temp)
        y_temp = [yi - c * x1i for yi, x1i in zip(y_temp, x1)]
        y_ortho = normalize(y_temp)
        Av = matvec(A, y_ortho)
        lambda_est = dot(y_ortho, Av)
        residual_vec = [avi - lambda_est * vi for avi,vi in zip(Av,y_ortho)]
        r = max(abs(c) for c in residual_vec)
        ortho_check = abs(dot(x1, y_ortho))

        delta = abs(lambda_est - prev_lambda) if k>1 else None
        angle = angle_between_vectors(y_ortho, prev_v) if k>1 else None

        delta_str = f"{delta:.2e}" if delta is not None else "  —  "
        angle_str = f"{angle:.2e} rad" if angle is not None else "  —  "
        print(f"[k={k:3d}] λ={lambda_est:.10f}  Δλ={delta_str}  angle={angle_str}  r={r:.2e}  ortho={ortho_check:.2e}")

        iteration_log.append((k, lambda_est, delta, angle, r, ortho_check))

        if k>1 and check_eigen_convergence(lambda_est, prev_lambda, y_ortho, prev_v, eps_a, eps_g) and ortho_check < 1e-10:
            return 0, lambda_est, y_ortho, k, r, iteration_log

        prev_lambda = lambda_est
        prev_v = y_ortho[:]
        x = y_ortho

    return 1, lambda_est, x, M, r, iteration_log


def run_test_second_min(test_id, n, eigen_range, eps_a, eps_g, M):
    print("\n" + "="*70)
    print(f"ТЕСТ №{test_id}  (N={n}, диапазон λ = {eigen_range})")
    print("="*70)

    eigenvalues = sorted([random.uniform(eigen_range[0], eigen_range[1]) for _ in range(n)])
    A, x_true, b, H, eigs = matrix_generate(n, eigenvalues)

    A_copy = copy.deepcopy(A)
    A_fact = cholesky_full(A_copy)

    _, _, v1, _, _, _ = find_min_eigen(A, A_fact, eps_a, eps_g, M)


    status2, lambda2, v2, k2, r2, log2 = find_second_min_eigen(A, A_fact, 0, v1, eps_a, eps_g, M)

    #Находим соответствие с истинным собственным вектором
    # def find_best_match(vec, H):
    #     best_idx = 0
    #     best_dot = 0
    #     for j in range(len(H)):
    #         hj = [H[i][j] for i in range(len(H))]
    #         d = abs(dot(vec, hj)) / (norm(vec)*norm(hj))
    #         if d > best_dot:
    #             best_dot = d
    #             best_idx = j
    #     return best_idx, best_dot
    #
    # idx2, match2 = find_best_match(v2, H)
    # true_lambda2 = eigenvalues[idx2]
    # true_vec2 = [H[i][idx2] for i in range(n)]

    true_lambda2 = eigenvalues[1]

    #ищем столбец H, который максимально совпадает с найденным v2
    best_idx = max(range(n), key=lambda j: abs(dot(v2, [H[i][j] for i in range(n)])))
    true_vec2 = [H[i][best_idx] for i in range(n)]

    err_lambda2 = abs(lambda2 - true_lambda2)
    angle_v2_rad = angle_between_vectors(v2, true_vec2)

    return {
        "test": test_id,
        "N": n,
        "range": eigen_range,
        "eps_lambda": eps_a,
        "eps_vector": eps_g,

        "lambda2": lambda2,
        "true_lambda2": true_lambda2,
        "err_lambda2": err_lambda2,
        "angle_v2_rad": angle_v2_rad,
        "r2": r2,
        "k2": k2
    }


def to_latex(tests: list):
    df = pd.DataFrame(tests)

    df.rename(columns={
        "test": "№", "N": "N", "range": "Диапазон λ", "eps_lambda": "ελ",
        "eps_vector": "εv", "err_lambda2": "|λ2-λ2*|", "angle_v2_rad": "angle(v2,v2*)[rad]",
        "r2": "r2", "k2": "k2"
    }, inplace=True)

    latex_table = df.to_latex(index=False, float_format="%.3e",
                              caption="Результаты поиска второго минимального собственного значения",
                              label="tab:second_min_eigen")

    with open(f"C:\\Users\\Andy\\Desktop\\test3.tex", "w", encoding="utf-8") as f:
        f.write(latex_table)

def main():
    random.seed(0)
    M = 2000
    tests = []
    test_id = 1
    for n in [10, 30, 50]:
        for eigen_range in [(-2,2), (-50,50)]:
            for eps_a, eps_g in ((1e-5, 1e-5), (1e-8, 1e-8)):
                res = run_test_second_min(test_id, n, eigen_range, eps_a, eps_g, M)
                if res is not None:
                    tests.append(res)
                test_id += 1

    print("\n" + "="*100)
    print("ТАБЛИЦА")
    print("="*100)
    hdr = ("№","N","Диапазон λ","ελ","εv",
           "|λ2-λ2*|","angle(v2,v2*)[rad]","r2","k2")
    print("{:>2} {:>4} {:>13} {:>7} {:>7} {:>12} {:>20} {:>10} {:>4}".format(*hdr))
    print("-"*100)
    for t in tests:
        print("{:2d} {:4d} {:13} {:7.1e} {:7.1e} {:12.2e} {:20.6f} {:10.2e} {:4d}".format(
            t["test"], t["N"], str(t["range"]), t["eps_lambda"], t["eps_vector"],
            t["err_lambda2"], t["angle_v2_rad"], t["r2"], t["k2"]
        ))
    to_latex(tests)


if __name__ == "__main__":
    main()

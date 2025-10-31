from random import randint
import math

def get(i, j, band):
    if i < j:
        i, j = j, i
    d = i - j
    if d < len(band[i]):
        return band[i][-d - 1]
    else:
        return 0


def matrix_generate(n: int, l: int):
    result, f = [], []
    x = [randint(1, 15) for _ in range(n)]
    for i in range(n):
        j = 0
        k = l
        row = []
        while j <= k and j <= i:
            elem = randint(1, 15)
            row.append(elem)
            j += 1
        result.append(row)
        row[-1] += n * 10

    b = [0] * n
    for i in range(n):
        for j in range(n):
            b[i] += get(i, j, result) * x[j]
    return result, x, b


def print_like_full_matrix(band: list[list[int]], n: int, f: list[int] | None = None):
    flat = [f"{x:.4g}" for row in band for x in row]
    width = max(len(x) for x in flat)

    for i in range(n):
        row = [f"{get(i, j, band):>{width}.4g}" for j in range(n)]
        print('\t'.join(row), end='')
        if f:
            print(f" | {f[i]}")
        else:
            print()

def set_in_band(i, j, band, value):
    if i < j:
        i, j = j, i
    d = i - j
    if d < len(band[i]):
        band[i][-d - 1] = value


def c_band(A):
    n = len(A)
    L = [[0.0] * len(A[i]) for i in range(n)]

    for i in range(n):
        j_start = max(0, i - (len(A[i]) - 1))

        for j in range(j_start, i + 1):
            s = 0.0
            k_start = max(0, j - (len(L[j]) - 1))
            for k in range(k_start, j):
                s += get(i, k, L) * get(j, k, L)

            val = get(i, j, A) - s

            if i == j:
                set_in_band(i, j, L, math.sqrt(val))
            else:
                set_in_band(i, j, L, val / get(j, j, L))
    return L

def solve(L: list[list[float]], f: list[float]) -> list[float]:
    n = len(L)

    y = [0.0] * n
    for i in range(n):
        s = 0.0
        row = L[i]
        j_start = max(0, i - (len(row) - 1))

        for j in range(j_start, i):
            index_in_row = j - j_start
            s += row[index_in_row] * y[j]
        y[i] = (f[i] - s) / row[-1]

    x = [0.0] * n
    for i in reversed(range(n)):
        s = 0.0

        for j in range(i + 1, n):
            row_j = L[j]
            j_start = max(0, j - (len(row_j) - 1))

            if j_start <= i:
                index_in_row_j = i - j_start
                if index_in_row_j < len(row_j) - 1:
                    s += row_j[index_in_row_j] * x[j]

        x[i] = (y[i] - s) / L[i][-1]

    return x


def main():
    n, l = 8, 4
    A, x, f = matrix_generate(n, l)
    print(A)
    print(x)
    print(f, end='\n\n')
    print_like_full_matrix(A, n, f)
    L = c_band(A)
    result = solve(L, f)
    print(result)

if __name__ == "__main__":
    main()
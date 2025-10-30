from random import randint


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

    b = [0] * n
    for i in range(n):
        for j in range(n):
            b[i] += get(i, j, result) * x[j]
    return result, x, b


def print_like_matrix(band: list[list[int]], n: int, f: list[int]):
    flat = [f"{x:.4g}" for row in band for x in row]
    width = max(len(x) for x in flat)

    for i in range(n):
        row = [f"{get(i, j, band):>{width}.4g}" for j in range(n)]
        print('\t'.join(row), end='')
        print(f" | {f[i]}")

def solve_from_L_band(L: list[list[float]], f: list[float]) -> list[float]:
    n = len(L)

    # Прямой ход: решаем L * y = f
    y = [0.0] * n
    for i in range(n):
        s = 0.0
        row = L[i]
        j_start = max(0, i - (len(row) - 1))

        for j in range(j_start, i):
            index_in_row = j - j_start
            s += row[index_in_row] * y[j]
        y[i] = (f[i] - s) / row[-1]

    # Обратный ход: решаем L^T * x = y
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
    print(f)
    print_like_matrix(A, n, f)
    result = solve_from_L_band(A, f)
    print(result)

if __name__ == "__main__":
    main()
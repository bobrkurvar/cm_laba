from random import randint

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
        row = result[i]
        for k, j in enumerate(range(i - len(row) + 1, i)):
            b[i] += row[k] * x[j]
            b[j] += row[k] * x[i]
        b[i] += row[-1] * x[i]
    return result, x, b


def print_like_matrix(band: list[list[int]], n: int, l: int, f: list[int]):
    flat = [f"{x:.4g}" for row in band for x in row]
    width = max(len(x) for x in flat)

    def get(i, j):
        if i < j:
            i, j = j, i
        d = i - j
        if d < len(band[i]):
            return band[i][-d-1]
        else:
            return 0

    for i in range(n):
        row = [f"{get(i, j):>{width}.4g}" for j in range(n)]
        print('\t'.join(row), end='')
        print(f" | {f[i]}")

def solve_from_L_band(A: list[list[float]], b: list[float], l: int) -> list[float]:
    n = len(A)
    y = [0.0] * n

    # Прямой ход: решаем L * y = b
    for i in range(n):
        s = 0.0
        row = A[i]
        j_start = max(0, i - l)
        for j in range(j_start, i):
            index_in_row = j - j_start
            s += row[index_in_row] * y[j]
        y[i] = (b[i] - s) / row[-1]  # делим на диагональ

    # Обратный ход: решаем L^T * x = y
    x = [0.0] * n
    for i in reversed(range(n)):
        s = 0.0
        # Проходим по строкам ниже i, которые используют элемент i
        for j in range(i + 1, min(n, i + l + 1)):
            row = A[j]
            j_start = max(0, j - l)
            index_in_row = i - j_start
            if 0 <= index_in_row < len(row) - 1:  # не диагональ
                s += row[index_in_row] * x[j]
        x[i] = (y[i] - s) / A[i][-1]

    return x



def main():
    n, l = 8, 4
    A, x, f = matrix_generate(n, l)
    print(A)
    print(x)
    print(f)
    print_like_matrix(A, n, l,f)
    result = solve_from_L_band(A, x, l)
    print(result)

if __name__ == "__main__":
    main()
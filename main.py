

def print_matrix(matrix: list):
    str_matrix = [[f"{x:.4f}" for x in row] for row in matrix]
    max_len = max(len(s) for row in str_matrix for s in row)
    for row in matrix:
        for i in row:
            if i == 0: i = abs(i)
            print(f'{i:>{max_len}.4g}', end='\t')
        print('\t')
    print('\n')

def extract_from_file(k: int, l: int, a: list, b: list, c: list, p: list, q: list):
    with open('my_data.txt') as f:
        i = 0
        for row in f:
            ch = row.split()
            ch = [int(i) for i in ch]
            print(ch)
            try:
                if i == k-1: p.extend(ch)
                if i == l-1: q.extend(ch)
                if i > 0: a.append(ch[i-1])
                b.append(ch[i])
                c.append(ch[i+1])
                i += 1
            except IndexError as err:
                print(err)
                pass


def to_matrix(n: int, matrix: list, a: list, b: list, c: list, p: list, q: list):
    for i in range(n):
        row = []
        if i == k-1:
            row = p
            matrix.append(row)
            continue
        if i == l-1:
            row = q
            matrix.append(row)
            continue
        row.extend([0]*(i-1))
        if i > 0: row.append(a[i-1])
        row.append(b[i])
        if i < n - 1: row.append(c[i])
        row.extend([0]*(n-(i+2)))
        matrix.append(row)


def go_to_k_on_matrix(k: int, rows: list):
    #до k строки приводим к 1 на главной диагонали и 0 под ней и в строке k вплоть до k-1 0
    for i in range(1, k):
        to_divide = rows[i-1][i-1]
        print(f'to_divide {to_divide:.3f}')
        coef = rows[i][i - 1] / (rows[i - 1][i - 1] / to_divide)
        coef_k = rows[k-1][i - 1] / (rows[i - 1][i - 1] / to_divide)
        coef_l = rows[l - 1][i - 1] / (rows[i - 1][i - 1] / to_divide)
        print(f'coef: {coef:.3f}\ncoef_k: {coef_k:.3f}\ncoef_l: {coef_l:.3f}')
        for j in range(n):
            rows[i-1][j] /= to_divide
            to_sub_k = rows[i - 1][j] * coef_k
            to_sub_l = rows[i - 1][j] * coef_l
            #print(f'вычитаем k: {to_sub_k}\nвычитаем l: {to_sub_l}')
            rows[k - 1][j] -= to_sub_k
            rows[l-1][j] -= to_sub_l
            if i != k-1:
                to_sub = rows[i - 1][j] * coef
                #print(f'вычитаем: {to_sub:.3f}')
                rows[i][j] -= to_sub
        print_matrix(rows)

def go_to_k_on_arrays(a: list, b: list, c: list, p: list, q: list, k: int):
    for i in range(1, k-1):
        coef = a[i] / b[i-1]
        to_divide = b[i-1]
        b[i-1] /= to_divide
        if i > 1: a[i-1] /= to_divide
        if i < k: c[i-1] /= to_divide
        a[i] -= a[i-1] * coef if i == 1 else b[i-1] * coef
        b[i] -= b[i-1] * coef if i == 1 else c[i-1] * coef

# def print_like_matrix(a: list, b: list, c: list, p: list, q: list):
#     numbers = [a, b, c, p, q]
#     str_matrix = [[f"{x:.4f}" for x in num] for num in numbers]
#     max_len = max(len(s) for row in str_matrix for s in row)
#     for i in range(n):
#         print(*([0] * (i - 1)), sep='\t')
#         if i > 0: print(f'{a[i]:>{max_len}.4g}', end='\t')
#         print(f'{b[i]:>{max_len}.4g}', end='\t')
#         print(f'{b[i]:>{max_len}.4g}', end='\t')
#         print(*([0] * (n - (i + 2))), sep='\t')
#
# def input_arrays(a: list, b: list, c: list, p: list, q: list):
#     str_a = input('Введите через пробел массив a: ')
#     str_b = input('Введите через пробел массив b: ')
#     str_c = input('Введите через пробел массив c: ')
#     str_p = input('Введите через пробел массив p: ')
#     str_q = input('Введите через пробел массив q: ')
#     a.extend(int(i) for i in str_a.split())
#     b.extend(int(i) for i in str_b.split())
#     c.extend(int(i) for i in str_c.split())
#     p.extend(int(i) for i in str_p.split())
#     q.extend(int(i) for i in str_q.split())


if __name__ == '__main__':
    from_file = input('From file? (y/n): ')
    a, b, c, p, q = list(), list(), list(), list(), list()
    if from_file == 'y':
        n, k, l = 10, 9, 10
        extract_from_file(k, l, a, b, c, p, q)
        print()
        print(p, q, sep='\n', end='\n\n')
        print(a, b, c, sep='\n', end='\n\n')
        #print_like_matrix(a, b, c, p, q)
        matrix = []
        to_matrix(n, matrix, a, b, c, p, q)
        print_matrix(matrix)
        go_to_k_on_matrix(k, matrix)
        print_matrix(matrix)
    elif from_file == 'n':
        n, k, l = int(input('Введите n: ')), int(input('Введите k: ')), int(input('Введите l: '))
        # input_arrays(a,b,c,p,q)
        # print_like_matrix(a, b, c, p, q)

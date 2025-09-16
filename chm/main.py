def print_like_matrix(a: list, b: list, c: list, p: list, q: list, n: int):
    nulls = 1
    str_a = [f'{x:.4g}' for x in a]
    str_b = [f'{x:.4g}' for x in b]
    str_c = [f'{x:.4g}' for x in c]
    str_p = [f'{x:.4g}' for x in p]
    str_q = [f'{x:.4g}' for x in q]
    max_len = max(len(s) for s in (str_a + str_b + str_c + str_p + str_q))
    #print(f'max_len: {max_len}')
    for i in range(n):
        print(f'{p[i]:>{max_len}.4g}', end='\t')
        print(f'{q[i]:>{max_len}.4g}', end='\t')
        if i >= 4:
            for j in ([0] * nulls):
                print(f'{j:>{max_len}.4g}', sep='\t', end='\t')
            nulls += 1
        try:
            if i >= 3: print(f'{a[i-1]:>{max_len}.4g}', end='\t')
            if i >= 2: print(f'{b[i]:>{max_len}.4g}', end='\t')
            if  i >= 1: print(f'{c[i]:>{max_len}.4g}', end='\t')
        except IndexError:
            pass
        for j in ([0] * (n-i-2)):
            print(f'{j:>{max_len}.4g}', end='\t')
        print()



def extract_from_file(a: list, b: list, c: list, p: list, q: list):
    with open('data.txt') as f:
        i = 0
        for row in f:
            ch = row.split()
            ch = [float(i) for i in ch]
            #print(ch)
            try:
                #print(f'i: {i}')
                p.append(ch[0])
                q.append(ch[1])
                #print(p, q, sep='\t', end='\n')
                if i > 0: a.append(ch[i-1])
                b.append(ch[i])
                c.append(ch[i+1])
                i += 1
            except IndexError as err:
                #print(err)
                break

# def go_to_k_on_matrix(k: int, rows: list):
#     #до k строки приводим к 1 на главной диагонали и 0 под ней и в строке k вплоть до k-1 0
#     for i in range(1, k):
#         to_divide = rows[i-1][i-1]
#         print(f'to_divide {to_divide:.3f}')
#         coef = rows[i][i - 1] / (rows[i - 1][i - 1] / to_divide)
#         coef_k = rows[k-1][i - 1] / (rows[i - 1][i - 1] / to_divide)
#         coef_l = rows[l - 1][i - 1] / (rows[i - 1][i - 1] / to_divide)
#         print(f'coef: {coef:.3f}\ncoef_k: {coef_k:.3f}\ncoef_l: {coef_l:.3f}')
#         for j in range(n):
#             rows[i-1][j] /= to_divide
#             to_sub_k = rows[i - 1][j] * coef_k
#             to_sub_l = rows[i - 1][j] * coef_l
#             #print(f'вычитаем k: {to_sub_k}\nвычитаем l: {to_sub_l}')
#             rows[k - 1][j] -= to_sub_k
#             rows[l-1][j] -= to_sub_l
#             if i != k-1:
#                 to_sub = rows[i - 1][j] * coef
#                 #print(f'вычитаем: {to_sub:.3f}')
#                 rows[i][j] -= to_sub
#         print_matrix(rows)

def go_to_k_on_arrays(a: list, b: list, c: list, p: list, q: list, n: int):
    #ext_p, ext_q = list(), list()
    for i in range(n-2):
        print(f'\n {i}')
        if i == 0:
            cur = p
        else:
            next_cur = list()
        for j in range(1, n-i):
            try:
                coef = cur[j] / b[i]
                print(f'coef: {cur[j+i]} / {b[i]}')
                b[i+j] -= c[i+j-1] * coef
                if i == 0:
                    q[i+j] -= q[i+j-1] * coef
                a[i + j - 1] -= b[i+j-1] * coef
                cur[j+i] = 0
            except ZeroDivisionError:
                print(f'error in {j}')
        print_like_matrix(a, b, c, p, q, n)
        cur = q



if __name__ == '__main__':
    a, b, c, p, q = list(), list(), list(), list(), list()
    n, k, l = 10, 9, 10
    extract_from_file(a, b, c, p, q)
    print()
    print(p, q, sep='\n', end='\n\n')
    print(a, b, c, sep='\n', end='\n\n')
    print_like_matrix(a, b, c, p, q, n)
    go_to_k_on_arrays(a, b, c, p, q, n)
    print()
    print(p, q, sep='\n', end='\n\n')
    print(a, b, c, sep='\n', end='\n\n')

def print_like_matrix(a: list, b: list, c: list, p: list, q: list, n: int, f: list, ext_arr: dict | None = None):
    str_a, str_b, str_c, str_p, str_q = ([f'{x:.4g}' for x in a], [f'{x:.4g}' for x in b], [f'{x:.4g}' for x in c], [f'{x:.4g}' for x in p], [f'{x:.4g}' for x in q])
    max_len = max(len(s) for s in (str_a + str_b + str_c + str_p + str_q))
    rows = ''
    flag = False
    if ext_arr:
        ext_arr_index = 0
        print('EXT_ARR IS EXISTS')
        flag = True
    for i in range(n):
        for j in range(n):
            if p[i] == 0: p[i] = abs(p[i])
            if j == 0: rows += f'{p[i]:>{max_len}.4g}\t'
            elif j == 1: rows += f'{q[i]:>{max_len}.4g}\t'
            elif i == j: rows += f'{b[i]:>{max_len}.4g}\t'
            elif j == i + 1: rows += f'{c[i]:>{max_len}.4g}\t'
            elif j == i - 1:
                if a[i-1] == 0: a[i-1] = abs(a[i-1])
                rows += f'{a[i-1]:>{max_len}.4g}\t'
            elif flag and ext_arr['row'] <= i and ext_arr['col'] == j:
                print('EXTRA')
                try:
                    rows += f'{ext_arr['arr'][ext_arr_index]:>{max_len}.4g}\t'
                    ext_arr_index += 1
                except IndexError:
                    flag = False
                    rows += f'{0:>{max_len}.4g}\t'
            else:
                rows += f'{0:>{max_len}.4g}\t'
        rows += f'| {f[i]:>{max_len}.4g}\t'
        rows += '\n'
    print(rows)

def extract_from_file(a: list, b: list, c: list, p: list, q: list, ans: list):
    with open('data.txt') as f:
        i = 0
        for row in f:
            ch = row.split()
            ch = [float(i) for i in ch]
            try:
                p.append(ch[0])
                q.append(ch[1])
                if i > 0: a.append(ch[i-1])
                b.append(ch[i])
                c.append(ch[i+1])
                i += 1
            except IndexError:
                break
        for row in f:
            try:
                ch = row.split()
                ch = [float(i) for i in ch]
                ans.append(ch[0])
            except IndexError:
                continue

# def go_down_on_arrays(a: list, b: list, c: list, p: list, q: list, n: int):
#     cur = None
#     for i in range(n):
#         if cur is None:
#             cur = p
#         coefs = []
#         temp = b[i]
#         b[i] = 1
#         if i > 0:
#             a[i - 1] /= temp
#         else:
#             p[i] = 1
#         if i == 1:
#             q[i] = 1
#         if i < n-1:
#             c[i] /= temp
#         print('На диагонали единицы:', end=' ')
#         if not (cur is None) and not (cur is q) and not (cur is p):
#             print('С extra arr')
#             print_like_matrix(a, b, c, p, q, n, dict(arr=cur[1:], row=i+2, col=i))
#         else:
#             print('Без extra arr')
#             print_like_matrix(a, b, c, p, q, n)
#         for j in range(n):
#             if j <= i and (cur is p or cur is q) : continue
#             try:
#                 coef = cur[j]
#                 coefs.append(coef)
#                 print(f"coef: {cur[j]} / {b[i]} : {coef}")
#                 print(f'Обнуляется {cur[j]}')
#                 cur[j] = 0
#                 if i >= 1:
#                     a[i-1] = 0
#             except IndexError:
#                 break
#         if i >= 1:
#             try:
#                 for pos, z in enumerate((b, a)):
#                     print(f'{z[i + 1]} - {c[i]} * {coefs[pos]} ({c[i] * coefs[pos]})', sep=' ')
#                     z[i + 1] -= c[i] * coefs[pos]
#                     print(f'= {z[i + 1]}')
#                 cur = [a[i + 1]]
#             except IndexError: pass
#             for z in range(2, len(range(i+1, n))):
#                 try:
#                     print(f'cur_name: {-1 * coefs[z]} * {c[i]} : {-1 * coefs[z] * c[i]}')
#                     cur_num = -1 * (coefs[z]) * c[i]
#                     cur.append(cur_num)
#                 except IndexError:
#                     break
#         else:
#             cur = q
#         print(cur)
#         print('После вычета: ')
#         if cur is p or cur is q:
#             print_like_matrix(a, b, c, p, q, n)
#         else:
#             print(f"PRINT WITH EXTRA ARRAY WITH ROW {i + 4} AND COLS {i + 1}")
#             print_like_matrix(a, b, c, p, q, n, dict(arr=cur[1:], row=i+3, col=i + 1))
#
# def go_up_on_arrays(c: list):
#     for i in range(len(c)):
#         c[i] = 0

def divide_by_diagonal_elem(i, n, a, b, c, p, q, f):
    temp = b[i]
    print('Делим на %s', temp)
    b[i] = 1
    f[i] /= temp
    if i == 0:
        p[i] = 1
    elif i == 1:
        q[i] = 1
        b[i - 1] = 1
        p[i - 1] = 1
    else:
        p[i] /= temp
        q[i] /= temp
    if i > 0:
        a[i - 1] /= temp
    if i < n - 1:
        c[i] /= temp

def sub_to_diagonal_elem_up(i, n, a, b, c, f):
    coef = c[i - 1] / b[i]
    print(f'Coef: {c[i - 1]} / {b[i]} : {coef}')
    print(f'Обнуляется {c[i - 1]}')
    print(f'f: {f[i-1]} - {f[i]} * ({c[i - 1]} / {b[i]}) ({coef})')
    f[i - 1] -= f[i] * coef
    c[i - 1] = 0
    if i > n - 1:
        print(f'b - {a[i - 1]} * ({c[i - 1]} / {b[i]}) ({coef})')
        b[i] -= a[i - 1] * coef

def sub_to_diagonal_elem_down(i, n, b, f):
    if i < n - 1 and a[i] != 0:
        coef = a[i] * b[i - 1]
        print(f'Coef for a: {a[i]} / {b[i]} : {coef}')
        print(f'Обнуляется {a[i]}')
        print(f'f: {f[i + 1]} - {f[i]} * ({a[i]} / {b[i]}) ({coef})')
        f[i + 1] -= f[i] * coef
        a[i] -= 0


def go_up(a, b, c, p, q, f, n):
    for i in range(n-1, 0, -1):
        divide_by_diagonal_elem(i, n, a, b, c, p, q, f)
        print_like_matrix(a, b, c, p, q, n, f)
        sub_to_diagonal_elem_up(i, n, a, b, c, f)
        print_like_matrix(a, b, c, p, q, n, f)
        sub_to_diagonal_elem_down(i, n, b, f)
        print_like_matrix(a, b, c, p, q, n, f)

# def answer_from_matrix(n: int, f: list) -> list:
#     x = list()
#     for i in range(n):
#         x.append(f[i])
#     return x

if __name__ == '__main__':
    a, b, c, p, q, f = list(), list(), list(), list(), list(), list()
    n, k, l = 10, 9, 10
    extract_from_file(a, b, c, p, q, f)
    print()
    print(p, q, sep='\n', end='\n\n')
    print(a, b, c, f, sep='\n', end='\n\n')
    print_like_matrix(a, b, c, p, q, n, f)
    go_up(a, b, c, p, q, f, n)
    print_like_matrix(a, b, c, p, q, n, f)
    #answer_arr = answer_from_matrix(n, f)
    print()
    print(p, q, sep='\n', end='\n\n')
    print(a, b, c, sep='\n', end='\n\n')
    #print(answer_arr)
    #Сделать проходку снизу вверх лишний массив не понадобится даже?
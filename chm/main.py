def print_like_matrix(a: list, b: list, c: list, p: list, q: list, n: int, ext_arr: dict | None = None):
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
            if j == 0: rows += f'{p[i]:>{max_len}.4g}\t'
            elif j == 1: rows += f'{q[i]:>{max_len}.4g}\t'
            elif i == j: rows += f'{b[i]:>{max_len}.4g}\t'
            elif j == i + 1: rows += f'{c[i]:>{max_len}.4g}\t'
            elif j == i - 1: rows += f'{a[i-1]:>{max_len}.4g}\t'
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
        rows += '\n'
    print(rows)

def extract_from_file(a: list, b: list, c: list, p: list, q: list):
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

def go_to_k_on_arrays(a: list, b: list, c: list, p: list, q: list, n: int):
    cur = None
    for i in range(n):
        if cur is None:
            cur = p
        coefs = []
        for j in range(n):
            if j <= i and (cur is p or cur is q) : continue
            try:
                coef = cur[j] / b[i]
                coefs.append(coef)
                print(f"coef: {cur[j]} / {b[i]} : {coef}")
                cur[j] -= cur[j]
            except IndexError:
                break
        if i >= 1:
            for pos, z in enumerate((b, a)):
                print(f'{z[i+1]} - {c[i]} * {coefs[pos]} ({c[i] * coefs[pos]})', sep=' ')
                z[i + 1] -= c[i] * coefs[pos]
                print(f'= {z[i + 1]}')
            cur = [a[i + 1]]
            for z in range(1, len(range(i+1, n))):
                try:
                    cur_num = -1 * (coefs[z])
                    cur.append(cur_num)
                except IndexError:
                    break
        else:
            cur = q
        print(cur)
        if cur is p or cur is q:
            print_like_matrix(a, b, c, p, q, n)
        else:
            print(f"PRINT WITH EXTRA ARRAY WITH ROW {i + 3} AND COLS {i + 1}")
            print_like_matrix(a, b, c, p, q, n, dict(arr=cur[1:], row=i+3, col=i + 1))


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

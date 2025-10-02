

def print_like_matrix(a: list, b: list, c: list, p: list, q: list, n: int, f: list | None = None):
    str_a, str_b, str_c, str_p, str_q = ([f'{x:.4g}' for x in a], [f'{x:.4g}' for x in b], [f'{x:.4g}' for x in c], [f'{x:.4g}' for x in p], [f'{x:.4g}' for x in q])
    max_len = max(len(s) for s in (str_a + str_b + str_c + str_p + str_q))
    rows = ''
    for i in range(n):
        for j in range(n):
            if p[i] == 0: p[i] = abs(p[i])
            if j == 0: rows += f'{p[i]:>{max_len}.4g}\t'
            elif j == 1: rows += f'{q[i]:>{max_len}.4g}\t'
            elif i == j: rows += f'{b[i]:>{max_len}.4g}\t'
            elif j == i + 1:
                if c[i] == 0:
                    c[i] = abs(c[i])
                rows += f'{c[i]:>{max_len}.4g}\t'
            elif j == i - 1:
                if a[i-1] == 0: a[i-1] = abs(a[i-1])
                rows += f'{a[i-1]:>{max_len}.4g}\t'
            else:
                rows += f'{0:>{max_len}.4g}\t'
        if f:
            rows += f'| {f[i]:>{max_len}.4g}\t'
        rows += '\n'
    print(rows)

def extract_from_file(file: str, a: list, b: list, c: list, p: list, q: list, ans: list):
    with open(file) as f:
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

def divide_by_diagonal_elem(i, a, b, c, p, q, f, f_):
    temp = b[i]
    a[i - 1] /= temp
    b[i] = 1
    f[i] /= temp
    f_[i] /= temp
    p[i] /= temp
    try:
        c[i] /= temp
    except IndexError: pass
    if i == 1:
        q[i] = 1
        p[i - 1] = 1
        f[i - 1] /= b[i - 1]
        f_[i - 1] /= b[i - 1]
        b[i - 1] = 1
        print()
    else:
        q[i] /= temp



def sub_to_diagonal_elem_up(i, a, b, c, p, q, f, f_):
    if c[i - 1] != 0:
        coef = c[i - 1] / b[i]
        print(f'Coef: {c[i - 1]} / {b[i]} : {coef}', end='\t')
        print(f'Обнуляется {c[i - 1]}', end='; ')
        f[i - 1] -= f[i] * coef
        f_[i - 1] -= f_[i] * coef
        print(f'b: {b[i-1]} - {a[i - 1] * coef} = {b[i - 1] - a[i - 1] * coef}', end='; ')
        b[i - 1] -= a[i - 1] * coef
        print(f'p: {p[i - 1]} - {p[i] * coef} = {p[i - 1] - p[i] * coef}', end='; ')
        p[i - 1] -= p[i] * coef
        print(f'q: {q[i - 1]} - {q[i] * coef} = {q[i - 1] - q[i] * coef}')
        q[i - 1] -= q[i] * coef
        c[i - 1] = 0
        if i == 2:
            a[0] -= p[i] * coef
        elif i == 3:
            a[1] -= q[i] * coef


def to_null_on_p(n, p, f, a, f_):
    for i in range(1, n):
        print_like_matrix(a, b, c, p, q, n, f)
        coef = p[i]
        print(f'Coef: {p[i]}', end='\t')
        print(f'Обнуляется p: {p[i]}', end='\t')
        p[i] = 0
        if i == 1:
            print(f'Обнуляется a: {a[i - 1]}', end='\t')
            a[i - 1] = 0
        print(f'f: {f[i]} - {f[0]} * {coef}) = {f[i] - f[0] * coef}')
        f[i] -= f[0] * coef
        f_[i] -= f_[0] * coef

def to_null_on_q(n, a, q, f, f_):
    for i in range(2, n):
        print_like_matrix(a, b, c, p, q, n, f)
        if i == 2: a[i - 1] = 0
        coef = q[i]
        print(f'Обнуляется q: {q[i]}')
        q[i] = 0
        print(f'Coef: {coef}')
        print(f'f: {f[i]} - {f[1]} * {coef}) = {f[i] - f[1] * coef}')
        f[i] -= f[1] * coef
        f_[i] -= f_[1] * coef

def to_null_on_another(n, a, f, f_):
    for i in range(2, n - 1):
        if a[i] != 0:
            coef = a[i]
            print(f'i={i} Обнуляется p: {a[i]}')
            a[i] = 0
            print(f'Coef: {coef}', end='\t')
            print(f'f: {f[i+1]} - {f[i]} * {coef}) = {f[i + 1] - f[i] * coef}')
            f[i + 1] -= f[i] * coef
            f_[i + 1] -= f_[i] * coef

def fill_f_(a, b, c, p, q, n):
    for i in range(n-1, -1, -1):
        print(f'to_f_{i+1} = {b[i]} + {a[i-1]} = {b[i] + a[i-1]}')
        to_f_ = b[i]
        if i > 0:
            to_f_ += a[i-1]
        if i >= 3:
            to_f_ += p[i] + q[i]
        elif i >= 2:
            to_f_ += p[i]
        if i != n - 1:
            to_f_ += c[i]
        f_.append(to_f_)

def go_up(a, b, c, p, q, f, n, f_):
    print('-' * 50 + 'GO UP' + '-' * 50)
    for i in range(n-1, 0, -1):
        print_like_matrix(a, b, c, p, q, n, f)
        print_like_matrix(a, b, c, p, q, n, f_)
        divide_by_diagonal_elem(i, a, b, c, p, q, f, f_)
        sub_to_diagonal_elem_up(i, a, b, c, p, q, f, f_)
    print_like_matrix(a, b, c, p, q, n, f)
    print('\n' + '-' * 50 + 'GO DOWN' + '-' * 50, end='\n\n')
    to_null_on_p(n, p, f, a, f_)
    print_like_matrix(a, b, c, p, q, n, f)
    to_null_on_q(n, a, q, f, f_)
    print_like_matrix(a, b, c, p, q, n, f)
    to_null_on_another(n, a, f, f_)
    print_like_matrix(a, b, c, p, q, n, f)

if __name__ == '__main__':
    a, b, c, p, q, f, f_ = list(), list(), list(), list(), list(), list(), list()
    n = 10
    file = "data.txt"
    extract_from_file(file, a, b, c, p, q, f)
    fill_f_(a, b, c, p, q, n)
    f_ = f_[::-1]
    print(f'f~:{f_}', end='\n\n')
    print(p, q, sep='\n', end='\n\n')
    print(a, b, c, f, sep='\n', end='\n\n')
    print_like_matrix(a, b, c, p, q, n, f)
    go_up(a, b, c, p, q, f, n, f_)
    print(f, f_, sep='\n')
    for i in range(1, n+1):
        print(f'x{i}: {f[i-1]:.4g}')
    print()
    for i in range(1, n + 1):
        print(f'x~{i}: {f_[i-1]:.4g}')
    d, d_ = None, None
    d = max((abs(-1 - i) for i in f))
    d_ = max((abs(1 - i) for i in f_))
    print(f'погрешность для x: {d}, для x~: {d_}')
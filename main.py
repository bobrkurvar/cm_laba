import math

n, k, l = int(input('Введите n: ')), int(input('Введите k: ')), int(input('Введите l: '))

def print_matrix(matrix: list):
    for row in matrix:
        for i in row:
            print(i, end='\t')
        print('\t')

rows = []
for i in range(n):
    row = []
    for j in range(n):
        elem = float(input(f'введите элемент {j} для строки {i}: '))
        row.append(elem)
    rows.append(row)

# #1 под диагональю
# for i in range(k):
#     to_divide = rows[i][i-1] if i != 0 else rows[i][i]
#     print(f'to_divide: {to_divide}')
#     for j in range(n):
#         rows[i][j] /= to_divide

for i in range(1, k):
    to_divide = rows[i-1][i-1]
    print(f'to_divide {to_divide}')
    for j in range(n):
        rows[i-1][j] /= to_divide
        rows[i][j] -= rows[i][j]




print_matrix(rows)
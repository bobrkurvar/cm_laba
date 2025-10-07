import numpy as np
import os


def generate_nice_solution(n):
    """Генерация 'красивого' решения"""
    # Расширенный список красивых чисел
    nice_numbers = []

    # Целые числа от -8 до 8
    for i in range(-8, 9):
        nice_numbers.append(i)

    # Простые дроби с знаменателями 2, 3, 4
    for denom in [2, 3, 4]:
        for num in range(-4 * denom, 4 * denom + 1):
            if num % denom != 0 and abs(num / denom) <= 8:
                nice_numbers.append(num / denom)

    # Убираем дубликаты и сортируем
    nice_numbers = sorted(list(set(nice_numbers)))

    # Выбираем n случайных красивых чисел
    x_exact = np.random.choice(nice_numbers, n, replace=True)
    return x_exact


def generate_tridiagonal_system(n, coef_range):
    """Генерация системы с красивым решением"""
    min_coef, max_coef = coef_range

    # Генерация красивого решения
    x_exact = generate_nice_solution(n)

    # Генерация компонентов матрицы как целых чисел
    b = np.random.randint(min_coef, max_coef + 1, n)  # главная диагональ
    a = np.random.randint(min_coef, max_coef + 1, n - 1)  # под главной диагональю
    c = np.random.randint(min_coef, max_coef + 1, n - 1)  # над главной диагональю
    p = np.random.randint(min_coef, max_coef + 1, n)  # первый столбец
    q = np.random.randint(min_coef, max_coef + 1, n)  # второй столбец

    # Создание полной матрицы
    A = np.zeros((n, n))
    for i in range(n):
        A[i, i] = b[i]  # главная диагональ
        A[i, 0] = p[i]  # первый столбец
        A[i, 1] = q[i]  # второй столбец
        if i < n - 1:
            A[i + 1, i] = a[i]  # под диагональю
        if i < n - 1:
            A[i, i + 1] = c[i]  # над диагональю

    # Вычисление правой части
    f = A @ x_exact

    return b, a, c, p, q, f, x_exact


def save_system(b, a, c, p, q, f, x_exact, filename):
    """Сохранение данных массивов в файл"""
    with open(filename, 'w') as file:

        # Записываем векторы (каждый с новой строки)
        file.write(" ".join(f"{int(val)}" for val in b) + "\n")
        file.write(" ".join(f"{int(val)}" for val in a) + "\n")
        file.write(" ".join(f"{int(val)}" for val in c) + "\n")
        file.write(" ".join(f"{int(val)}" for val in p) + "\n")
        file.write(" ".join(f"{int(val)}" for val in q) + "\n")
        file.write(" ".join(f"{val:.6f}" for val in f) + "\n")
        file.write(" ".join(f"{val:.6f}" for val in x_exact) + "\n")


# Основная программа
orders = [10, 100, 1000]
ranges = [(-10, 10), (-100, 100), (-1000, 1000)]
repetitions = 1

os.makedirs("nice_matrices", exist_ok=True)

print("Генерация 45 систем с красивыми решениями...")
file_count = 0

for n in orders:
    for coef_range in ranges:
        for rep in range(repetitions):
            file_count += 1

            # Генерация системы
            b, a, c, p, q, f, x_exact = generate_tridiagonal_system(n, coef_range)

            # Сохранение системы
            filename = f"system_{file_count:02d}_n{n}_range{coef_range[0]}_{coef_range[1]}_rep{rep + 1}.txt"
            full_path = f"nice_matrices/{filename}"
            save_system(b, a, c, p, q, f, x_exact, full_path)

            # Показываем примеры решений для первых нескольких систем каждого типа
            if rep == 0:  # только первый повтор каждого типа
                print(f"Файл {file_count:02d}: n={n}, диапазон={coef_range}")
                print(f"  Пример решения (первые 5 элементов): {[f'{val:g}' for val in x_exact[:5]]}")

print(f"\nСоздано {file_count} файлов в папке 'nice_matrices'")
print("Информация о всех системах сохранена в 'nice_matrices/systems_info.txt'")

# Покажем полные примеры нескольких решений
print("\nПолные примеры красивых решений:")
print("=" * 50)

# Пример для n=10
b, a, c, p, q, f, x_exact = generate_tridiagonal_system(10, (-10, 10))
print(f"Пример решения (n=10): {[f'{val:g}' for val in x_exact]}")

# Пример для n=100 (первые 10 элементов)
b, a, c, p, q, f, x_exact = generate_tridiagonal_system(100, (-100, 100))
print(f"Пример решения (n=100, первые 10): {[f'{val:g}' for val in x_exact[:10]]}")

# Пример для n=1000 (первые 5 элементов)
b, a, c, p, q, f, x_exact = generate_tridiagonal_system(1000, (-1000, 1000))
print(f"Пример решения (n=1000, первые 5): {[f'{val:g}' for val in x_exact[:5]]}")
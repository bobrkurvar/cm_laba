import pandas as pd

# Предположим, что у тебя есть списки с результатами
test_numbers = list(range(1, 10))
sizes = [10, 10, 10, 100, 100, 100, 1000, 1000, 1000]
coef_ranges = [(-10, 10), (-100, 100), (-1000, 1000),
               (-10, 10), (-100, 100), (-1000, 1000),
               (-10, 10), (-100, 100), (-1000, 1000)]
avg_delta = [6.2311e-16, 4.2653e-15, 6.3758e-16,
             1.2037e-15, 4.2304e-15, 2.2443e-15,
             4.3771e-16, 1.2304e-14, 2.9542e-15]
avg_precision = [2.6897e-15, 2.6488e-14, 2.5037e-15,
                 3.0198e-14, 2.1177e-13, 6.4495e-14,
                 2.7356e-14, 6.9917e-13, 5.5049e-13]

# Создаём DataFrame
df = pd.DataFrame({
    "№ теста": test_numbers,
    "Размерность системы": sizes,
    "Диапазон элементов матрицы": coef_ranges,
    "Средняя относительная погрешность системы": avg_delta,
    "Среднее значение оценки точности": avg_precision
})


latex_table = df.to_latex(index=False, float_format="%.4e")
with open(r"C:\Users\user\Desktop\test_results.tex", "w") as f:
    f.write(latex_table)

print("LaTeX таблица успешно созданы!")

import math

def newton_interpolation(x0, h, N, Y, XX, m):
    # иначе не хватит узлов
    if N < m + 1:
        return 0.0, 1
    x_last = x0 + (N - 1) * h
    # Проверяем, что точка лежит внутри отрезка интерполирования
    if XX < x0 or XX > x_last:
        return 0.0, 2
    # Если m = 1 (линейная интерполяция), мы берём два ближайших к XX узла и проводим
    # через них прямую. По ней и находим значение в XX.
    # Если m = 2 (квадратичная интерполяция), берём три ближайших узла и строим параболу.

    # Выбор начального индекса p так, чтобы интервал [x_p, x_{p+m}] был ближе всего к XX
    # Идеальный p, при котором середина интервала совпадает с XX
    ideal_p = (XX - x0) / h - m / 2.0
    p = int(round(ideal_p))
    print(p)
    #Ближайшими к XX будут те, которые окружают её слева и справа.
    # Корректировка границ
    # if p < 0:
    #     p = 0
    # if p > N - 1 - m:
    #     p = N - 1 - m
    # замена этого условия
    p = max(0, min(p, N - 1 - m))
    # Предвычисление факториалов до m
    # fact = [1] * (m + 1)
    # for i in range(1, m + 1):
    #     fact[i] = fact[i-1] * i

    # Вычисление коэффициентов b_k
    b = [0.0] * (m + 1)
    for k in range(m + 1):
        s = 0.0
        for i in range(k + 1):
            sign = (-1) ** (k - i)
            #term = sign * Y[p + i] / (fact[i] * fact[k - i] * (h ** k))
            term = sign * Y[p + i] / (math.factorial(i) * math.factorial(k - i) * (h ** k))
            s += term
        b[k] = s

    # Вычисление значения многочлена в точке
    result = 0.0
    for k in range(m + 1):
        prod = 1.0
        # Вычисляем произведение (XX - t_0)(XX - t_1)...(XX - t_{k-1})
        for j in range(k):
            tj = x0 + (p + j) * h   # узел t_j
            prod *= (XX - tj)
        result += b[k] * prod

    return result, 0

# Интерполяция функции sin(x) на [0, π] с шагом π/4
x0 = 0.0
h = math.pi / 4
N = 5
Y = [math.sin(x0 + i*h) for i in range(N)]
XX = 1.0
m = 3

yy, ier = newton_interpolation(x0, h, N, Y, XX, m)
if ier == 0:
    print(f"Приближённое значение: {yy}")
    print(f"Точное значение sin(1): {math.sin(1)}")
else:
    print(f"Ошибка: {ier}")
def caching_fibonacci():
    # створюємо порожній словник для збереження вже обчислених значень
    cache = {}

    def fibonacci(n):
        # базові випадки
        if n <= 0:
            return 0
        if n == 1:
            return 1

        # якщо значення вже є в кеші — повертаємо його
        if n in cache:
            return cache[n]

        # якщо немає — обчислюємо рекурсивно
        result = fibonacci(n - 1) + fibonacci(n - 2)

        # зберігаємо результат у кеш
        cache[n] = result

        return result

    # повертаємо внутрішню функцію
    return fibonacci


# використання
fib = caching_fibonacci()

print(fib(10))  # 55
print(fib(15))  # 610
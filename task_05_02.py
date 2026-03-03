import re
from typing import Callable, Generator


def generator_numbers(text: str) -> Generator[float, None, None]:
    """
    Шукає у тексті всі дійсні числа, які:
    - записані у форматі 123.45
    - чітко відокремлені пробілами з обох боків
    Повертає їх по одному через yield.
    """
    # Пояснення шаблону:
    # (?<=\s)  - перед числом має бути пробіл (lookbehind)
    # \d+\.\d+ - саме число: одна або більше цифр, крапка, одна або більше цифр
    # (?=\s)   - після числа має бути пробіл (lookahead)
    pattern = r"(?<=\s)\d+\.\d+(?=\s)"

    for match in re.finditer(pattern, text):
        yield float(match.group())


def sum_profit(text: str, func: Callable[[str], Generator[float, None, None]]) -> float:
    """
    Використовує генератор func(text), щоб підсумувати всі числа в тексті.
    """
    total = 0.0
    for number in func(text):
        total += number
    return total


# Приклад використання:
text = (
    "Загальний дохід працівника складається з декількох частин: "
    "1000.01 як основний дохід, доповнений додатковими надходженнями "
    "27.45 і 324.00 доларів."
)

total_income = sum_profit(text, generator_numbers)
print(f"Загальний дохід: {total_income:.2f}")
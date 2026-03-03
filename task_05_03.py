import sys
from typing import Dict, List, Optional


def parse_log_line(line: str) -> Optional[Dict[str, str]]:
    """
    Парсить один рядок логу у словник:
    {
        'date': '2024-01-22',
        'time': '08:30:01',
        'level': 'INFO',
        'message': 'User logged in successfully.'
    }
    Якщо формат не підходить — повертає None.
    """
    line = line.strip()
    if not line:
        return None

    # Очікуємо мінімум 4 частини: дата, час, рівень, повідомлення
    parts = line.split(" ", 3)
    if len(parts) < 4:
        return None

    date, time, level, message = parts
    return {"date": date, "time": time, "level": level, "message": message}


def load_logs(file_path: str) -> List[Dict[str, str]]:
    """
    Завантажує логи з файлу та повертає список розпарсених записів.
    """
    logs: List[Dict[str, str]] = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                parsed = parse_log_line(line)
                if parsed is not None:
                    logs.append(parsed)
    except FileNotFoundError:
        print(f"Помилка: файл не знайдено -> {file_path}")
        sys.exit(1)
    except OSError as e:
        print(f"Помилка читання файлу: {e}")
        sys.exit(1)

    return logs


def filter_logs_by_level(logs: List[Dict[str, str]], level: str) -> List[Dict[str, str]]:
    """
    Фільтрує логи за рівнем (наприклад, ERROR).
    """
    level = level.upper()

    # елемент функціонального програмування: filter + lambda
    return list(filter(lambda log: log.get("level") == level, logs))


def count_logs_by_level(logs: List[Dict[str, str]]) -> Dict[str, int]:
    """
    Рахує кількість записів для кожного рівня логування.
    """
    counts: Dict[str, int] = {}
    for log in logs:
        level = log.get("level", "UNKNOWN")
        counts[level] = counts.get(level, 0) + 1
    return counts


def display_log_counts(counts: Dict[str, int]) -> None:
    """
    Виводить статистику у вигляді таблиці.
    """
    print("Рівень логування | Кількість")
    print("-----------------|----------")

    # щоб порядок був красивий і стабільний
    preferred_order = ["INFO", "DEBUG", "ERROR", "WARNING"]
    for level in preferred_order:
        if level in counts:
            print(f"{level:<15} | {counts[level]}")

    # якщо раптом є інші рівні — теж покажемо
    for level in sorted(counts.keys()):
        if level not in preferred_order:
            print(f"{level:<15} | {counts[level]}")


def display_logs(logs: List[Dict[str, str]], level: str) -> None:
    """
    Виводить деталі логів обраного рівня.
    """
    level = level.upper()
    print(f"\nДеталі логів для рівня '{level}':")

    if not logs:
        print("Нічого не знайдено.")
        return

    for log in logs:
        print(f"{log['date']} {log['time']} - {log['message']}")


def main() -> None:
    if len(sys.argv) < 2:
        print("Використання:")
        print("  python main.py /path/to/logfile.log")
        print("  python main.py /path/to/logfile.log error")
        sys.exit(1)

    file_path = sys.argv[1]
    level_arg = sys.argv[2] if len(sys.argv) >= 3 else None

    logs = load_logs(file_path)
    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    if level_arg:
        filtered = filter_logs_by_level(logs, level_arg)
        display_logs(filtered, level_arg)


if __name__ == "__main__":
    main()
    
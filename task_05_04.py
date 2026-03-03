from typing import Dict, List, Tuple, Callable


def parse_input(user_input: str) -> Tuple[str, List[str]]:
    """
    Розбиває введений рядок на команду та аргументи.
    Напр.: "add Bob 050..." -> ("add", ["Bob", "050..."])
    """
    user_input = user_input.strip()
    if not user_input:
        return "", []
    parts = user_input.split()
    cmd = parts[0].lower()
    args = parts[1:]
    return cmd, args


def input_error(func: Callable) -> Callable:
    """
    Декоратор, який перехоплює типові помилки введення користувача
    та повертає зрозуміле повідомлення замість падіння програми.
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            # не вистачає аргументів (наприклад: add Bob)
            return "Enter the argument for the command"
        except ValueError:
            # неправильна кількість/формат аргументів
            return "Give me name and phone please."
        except KeyError:
            # звернення до контакту, якого немає
            return "Contact not found."
    return inner


@input_error
def add_contact(args: List[str], contacts: Dict[str, str]) -> str:
    # очікуємо рівно 2 аргументи
    if len(args) != 2:
        raise ValueError
    name, phone = args
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args: List[str], contacts: Dict[str, str]) -> str:
    if len(args) != 2:
        raise ValueError
    name, phone = args
    if name not in contacts:
        raise KeyError
    contacts[name] = phone
    return "Contact updated."


@input_error
def show_phone(args: List[str], contacts: Dict[str, str]) -> str:
    # тут достатньо 1 аргументу — ім'я
    name = args[0]  # якщо args порожній -> IndexError (обробить декоратор)
    if name not in contacts:
        raise KeyError
    return contacts[name]


@input_error
def show_all(args: List[str], contacts: Dict[str, str]) -> str:
    # args не потрібні
    if not contacts:
        return "No contacts yet."
    lines = [f"{name}: {phone}" for name, phone in contacts.items()]  # list comprehension (ФП елемент)
    return "\n".join(lines)


def main() -> None:
    contacts: Dict[str, str] = {}
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        cmd, args = parse_input(user_input)

        if cmd in ("exit", "close"):
            print("Good bye!")
            break
        elif cmd == "hello":
            print("How can I help you?")
        elif cmd == "add":
            print(add_contact(args, contacts))
        elif cmd == "change":
            print(change_contact(args, contacts))
        elif cmd == "phone":
            print(show_phone(args, contacts))
        elif cmd == "all":
            print(show_all(args, contacts))
        elif cmd == "":
            # якщо користувач просто натиснув Enter
            continue
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
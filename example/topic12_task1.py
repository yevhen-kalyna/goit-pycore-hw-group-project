"""Тема 12: Серіалізація та копіювання об'єктів — адресна книга з pickle."""

import pickle
import signal
from collections import UserDict
from collections.abc import Callable
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


class Field:
    """Базовий клас для полів запису."""

    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    """Клас для зберігання імені контакту."""


class Phone(Field):
    """Клас для зберігання номера телефону з валідацією (10 цифр)."""

    def __init__(self, value: str) -> None:
        if not (len(value) == 10 and value.isdigit()):
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)


class Birthday(Field):
    """Клас для зберігання дня народження з валідацією формату DD.MM.YYYY."""

    def __init__(self, value: str) -> None:
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    """Клас для зберігання даних одного контакту."""

    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Birthday | None = None

    def add_phone(self, phone: str) -> None:
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        phone_obj = self.find_phone(phone)
        if phone_obj is None:
            raise ValueError(f"Phone {phone} not found.")
        self.phones.remove(phone_obj)

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        phone_obj = self.find_phone(old_phone)
        if phone_obj is None:
            raise ValueError(f"Phone {old_phone} not found.")
        self.phones[self.phones.index(phone_obj)] = Phone(new_phone)

    def find_phone(self, phone: str) -> Phone | None:
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                return phone_obj
        return None

    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def __str__(self) -> str:
        phones = "; ".join(p.value for p in self.phones)
        birthday = (
            f", birthday: {self.birthday.value.strftime('%d.%m.%Y')}"
            if self.birthday
            else ""
        )
        return f"Contact name: {self.name.value}, phones: {phones}{birthday}"


class AddressBook(UserDict):
    """Клас для зберігання та керування записами контактів."""

    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self) -> list[dict[str, str]]:
        """Повертає список контактів, яких потрібно привітати протягом наступних 7 днів."""
        today = datetime.today().date()
        upcoming: list[dict[str, str]] = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            try:
                birthday_this_year = record.birthday.value.replace(year=today.year)
            except ValueError:
                birthday_this_year = record.birthday.value.replace(
                    year=today.year, month=3, day=1
                )

            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            delta_days = (birthday_this_year - today).days

            if delta_days <= 7:
                congratulation_date = birthday_this_year

                if congratulation_date.weekday() == 5:
                    congratulation_date += timedelta(days=2)
                elif congratulation_date.weekday() == 6:
                    congratulation_date += timedelta(days=1)

                upcoming.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime("%d.%m.%Y"),
                })

        return upcoming


def input_error(func: Callable[..., str]) -> Callable[..., str]:
    """Декоратор для обробки помилок введення користувача."""

    def inner(*args: Any, **kwargs: Any) -> str:
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Enter the argument for the command."

    return inner


@input_error
def add_contact(args: list[str], book: AddressBook) -> str:
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args: list[str], book: AddressBook) -> str:
    name, old_phone, new_phone = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."


@input_error
def show_phone(args: list[str], book: AddressBook) -> str:
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError
    return "; ".join(p.value for p in record.phones)


@input_error
def show_all(book: AddressBook) -> str:
    if not book.data:
        return "No contacts saved."
    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args: list[str], book: AddressBook) -> str:
    name, birthday, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args: list[str], book: AddressBook) -> str:
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError
    if record.birthday is None:
        return "Birthday not set."
    return record.birthday.value.strftime("%d.%m.%Y")


@input_error
def birthdays(book: AddressBook) -> str:
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays."
    return "\n".join(
        f"{entry['name']}: {entry['congratulation_date']}" for entry in upcoming
    )


def parse_input(user_input: str) -> tuple[str, list[str]]:
    parts = user_input.strip().split()
    if not parts:
        return "", []
    command = parts[0].lower()
    args = parts[1:]
    return command, args


def save_data(book: AddressBook, filename: str = "addressbook.pkl") -> None:
    """Зберігає адресну книгу у файл за допомогою pickle."""
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename: str = "addressbook.pkl") -> AddressBook:
    """Завантажує адресну книгу з файлу. Повертає нову книгу, якщо файл не знайдено."""
    if Path(filename).exists():
        with open(filename, "rb") as f:
            return pickle.load(f)
    return AddressBook()


def main() -> None:
    book = load_data()

    def handle_signal(signum: int, frame: Any) -> None:
        save_data(book)
        print("\nGood bye!")
        raise SystemExit(0)

    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGHUP, handle_signal)

    print("Welcome to the assistant bot!")

    try:
        while True:
            user_input = input("Enter a command: ")
            command, args = parse_input(user_input)

            if command in ["close", "exit"]:
                print("Good bye!")
                break

            elif command == "hello":
                print("How can I help you?")

            elif command == "add":
                print(add_contact(args, book))

            elif command == "change":
                print(change_contact(args, book))

            elif command == "phone":
                print(show_phone(args, book))

            elif command == "all":
                print(show_all(book))

            elif command == "add-birthday":
                print(add_birthday(args, book))

            elif command == "show-birthday":
                print(show_birthday(args, book))

            elif command == "birthdays":
                print(birthdays(book))

            else:
                print("Invalid command.")
    except KeyboardInterrupt:
        print("\nGood bye!")
    finally:
        save_data(book)


if __name__ == "__main__":
    main()
import re
from datetime import date, datetime


class Field:
    """Базовий клас для полів запису."""

    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return self.value


class Name(Field):
    """Клас для зберігання імені контакту."""


class Phone(Field):
    """Клас для зберігання номера телефону з валідацією (10 цифр)."""

    def __init__(self, value: str) -> None:
        if not re.fullmatch(r"\d{10}", value):
            raise ValueError(f"Phone number must contain exactly 10 digits, got: '{value}'")
        super().__init__(value)


class Email(Field):
    """Клас для зберігання email з валідацією."""

    def __init__(self, value: str) -> None:
        if not re.fullmatch(r"[a-zA-Z0-9.+_-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,}", value):
            raise ValueError(f"Invalid email address: '{value}'")
        self.value = value


class Address(Field):
    """Клас для зберігання адреси."""


class Birthday(Field):
    """Клас для зберігання дня народження з валідацією формату DD.MM.YYYY."""

    value: date  # type: ignore[assignment]

    def __init__(self, value: str) -> None:
        try:
            parsed = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError(f"Birthday must be in DD.MM.YYYY format, got: '{value}'")
        if parsed.year > date.today().year:
            raise ValueError("Birthday must be a date in the past.")
        self.value = parsed

    def __str__(self) -> str:
        return self.value.strftime("%d.%m.%Y")

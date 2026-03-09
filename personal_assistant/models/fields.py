from datetime import date


class Field:
    """Базовий клас для полів запису."""

    def __init__(self, value: str) -> None:
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError


class Name(Field):
    """Клас для зберігання імені контакту."""


class Phone(Field):
    """Клас для зберігання номера телефону з валідацією (10 цифр)."""

    def __init__(self, value: str) -> None:
        raise NotImplementedError


class Email(Field):
    """Клас для зберігання email з валідацією."""

    def __init__(self, value: str) -> None:
        raise NotImplementedError


class Address(Field):
    """Клас для зберігання адреси."""


class Birthday(Field):
    """Клас для зберігання дня народження з валідацією формату DD.MM.YYYY."""

    value: date  # type: ignore[assignment]

    def __init__(self, value: str) -> None:
        raise NotImplementedError

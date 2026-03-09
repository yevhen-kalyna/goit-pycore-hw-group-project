from personal_assistant.models.address_book import AddressBook
from personal_assistant.utils import input_error


@input_error
def add_contact(args: list[str], book: AddressBook) -> str:
    """Додає контакт або телефон до існуючого контакту."""
    raise NotImplementedError


@input_error
def change_contact(args: list[str], book: AddressBook) -> str:
    """Змінює телефон контакту."""
    raise NotImplementedError


@input_error
def show_phone(args: list[str], book: AddressBook) -> str:
    """Показує телефони контакту."""
    raise NotImplementedError


@input_error
def show_all(book: AddressBook) -> str:
    """Показує всі контакти."""
    raise NotImplementedError


@input_error
def add_birthday_handler(args: list[str], book: AddressBook) -> str:
    """Додає день народження контакту."""
    raise NotImplementedError


@input_error
def show_birthday_handler(args: list[str], book: AddressBook) -> str:
    """Показує день народження контакту."""
    raise NotImplementedError


@input_error
def birthdays_handler(args: list[str], book: AddressBook) -> str:
    """Показує дні народження за найближчі N днів."""
    raise NotImplementedError


@input_error
def search_contact(args: list[str], book: AddressBook) -> str:
    """Пошук контактів за будь-яким полем."""
    raise NotImplementedError


@input_error
def delete_contact(args: list[str], book: AddressBook) -> str:
    """Видаляє контакт."""
    raise NotImplementedError


@input_error
def add_email_handler(args: list[str], book: AddressBook) -> str:
    """Додає email контакту."""
    raise NotImplementedError


@input_error
def add_address_handler(args: list[str], book: AddressBook) -> str:
    """Додає адресу контакту."""
    raise NotImplementedError

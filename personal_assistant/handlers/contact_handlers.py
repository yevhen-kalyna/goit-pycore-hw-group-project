from personal_assistant.models.address_book import AddressBook
from personal_assistant.models.record import Record
from personal_assistant.utils import input_error


def _format_records(records: list[Record]) -> str:
    return "\n".join(str(record) for record in records)


@input_error
def add_contact(args: list[str], book: AddressBook) -> str:
    """Додає контакт або телефон до існуючого контакту."""
    name = args[0]
    phone = args[1]

    record = book.find(name)
    if record is None:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return "Contact added."

    record.add_phone(phone)
    return "Contact updated."


@input_error
def change_contact(args: list[str], book: AddressBook) -> str:
    """Змінює телефон контакту."""
    name = args[0]
    old_phone = args[1]
    new_phone = args[2]

    record = book.find(name)
    if record is None:
        raise KeyError(name)

    record.edit_phone(old_phone, new_phone)
    return "Contact updated."


@input_error
def show_phone(args: list[str], book: AddressBook) -> str:
    """Показує телефони контакту."""
    name = args[0]

    record = book.find(name)
    if record is None:
        raise KeyError(name)

    return "; ".join(phone.value for phone in record.phones)


@input_error
def show_all(book: AddressBook) -> str:
    """Показує всі контакти."""
    if not book.data:
        return "No contacts saved."

    return _format_records(list(book.data.values()))


@input_error
def add_birthday_handler(args: list[str], book: AddressBook) -> str:
    """Додає день народження контакту."""
    name = args[0]
    birthday = args[1]

    record = book.find(name)
    if record is None:
        raise KeyError(name)

    record.add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday_handler(args: list[str], book: AddressBook) -> str:
    """Показує день народження контакту."""
    name = args[0]

    record = book.find(name)
    if record is None:
        raise KeyError(name)

    if record.birthday is None:
        return "Birthday not set."

    return record.birthday.value.strftime("%d.%m.%Y")


@input_error
def birthdays_handler(args: list[str], book: AddressBook) -> str:
    """Показує дні народження за найближчі N днів."""
    if args:
        try:
            days = int(args[0])
        except ValueError:
            raise ValueError("Days argument must be a number.")
    else:
        days = 7
    upcoming = book.get_upcoming_birthdays(days)

    if not upcoming:
        return "No upcoming birthdays."

    return "\n".join(f"{item['name']}: {item['congratulation_date']}" for item in upcoming)


@input_error
def search_contact(args: list[str], book: AddressBook) -> str:
    """Пошук контактів за будь-яким полем."""
    query = args[0]
    results = book.search(query)

    if not results:
        return "No contacts found."

    return _format_records(results)


@input_error
def delete_contact(args: list[str], book: AddressBook) -> str:
    """Видаляє контакт."""
    name = args[0]

    record = book.find(name)
    if record is None:
        raise KeyError(name)

    book.delete(name)
    return "Contact deleted."


@input_error
def add_email_handler(args: list[str], book: AddressBook) -> str:
    """Додає email контакту."""
    name = args[0]
    email = args[1]

    record = book.find(name)
    if record is None:
        raise KeyError(name)

    if record.email is not None:
        old = str(record.email)
        record.add_email(email)
        return f"Email updated (was: {old})."
    record.add_email(email)
    return "Email added."


@input_error
def add_address_handler(args: list[str], book: AddressBook) -> str:
    """Додає адресу контакту."""
    name = args[0]
    address = args[1]

    record = book.find(name)
    if record is None:
        raise KeyError(name)

    if record.address is not None:
        old = str(record.address)
        record.add_address(address)
        return f"Address updated (was: {old})."
    record.add_address(address)
    return "Address added."

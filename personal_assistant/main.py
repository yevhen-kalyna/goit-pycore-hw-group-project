import signal
from types import FrameType

from personal_assistant.handlers.contact_handlers import (
    add_address_handler,
    add_birthday_handler,
    add_contact,
    add_email_handler,
    birthdays_handler,
    change_contact,
    delete_contact,
    search_contact,
    show_all,
    show_birthday_handler,
    show_phone,
)
from personal_assistant.handlers.note_handlers import (
    add_note_handler,
    add_tag_handler,
    all_notes_handler,
    delete_note_handler,
    edit_note_handler,
    find_by_tag_handler,
    find_note_handler,
    sort_notes_by_tag_handler,
)
from personal_assistant.storage import load_data, save_data


def parse_input(user_input: str) -> tuple[str, list[str]]:
    parts = user_input.strip().split()
    if not parts:
        return "", []
    return parts[0].lower(), parts[1:]


def _help_text() -> str:
    contacts = [
        ("add <name> <phone>", "Додає контакт або телефон до існуючого"),
        ("change <name> <old> <new>", "Змінює телефон контакту"),
        ("phone <name>", "Показує телефони контакту"),
        ("all", "Показує всі контакти"),
        ("delete-contact <name>", "Видаляє контакт"),
        ("add-birthday <name> <DD.MM.YYYY>", "Додає день народження"),
        ("show-birthday <name>", "Показує день народження"),
        ("birthdays [days]", "Найближчі дні народження (за замовч. 7 днів)"),
        ("add-email <name> <email>", "Додає email контакту"),
        ("add-address <name> <address>", "Додає адресу контакту"),
        ("search <query>", "Пошук контактів за ім'ям/телефоном/email"),
    ]
    notes = [
        ("add-note <title>", "Додає нову нотатку"),
        ("all-notes", "Показує всі нотатки"),
        ("delete-note <note_id>", "Видаляє нотатку"),
        ("edit-note <note_id>", "Редагує нотатку"),
        ("add-tag <note_id> <tag>", "Додає тег до нотатки"),
        ("find-note <query>", "Пошук нотаток за текстом"),
        ("find-by-tag <tag>", "Пошук нотаток за тегом"),
        ("sort-notes", "Сортує нотатки за тегами"),
    ]
    general = [
        ("hello", "Привітання"),
        ("help", "Показує цю довідку"),
        ("close | exit", "Вихід з програми"),
    ]

    all_rows = contacts + notes + general
    col_width = max(len(cmd) for cmd, _ in all_rows) + 2

    def format_section(title: str, rows: list[tuple[str, str]]) -> str:
        lines = [f"\n{title}:"]
        for cmd, desc in rows:
            lines.append(f"  {cmd:<{col_width}}{desc}")
        return "\n".join(lines)

    return (
        "Available commands:"
        + format_section("Контакти", contacts)
        + format_section("Нотатки", notes)
        + format_section("Загальні", general)
    )


def _is_successful_mutation(result: str) -> bool:
    return result in {
        "Contact added.",
        "Contact updated.",
        "Contact deleted.",
        "Birthday added.",
        "Email added.",
        "Address added.",
        "Note added.",
        "Note deleted.",
        "Note updated.",
        "Tag added.",
    }


def main() -> None:
    book, notebook = load_data()

    def handle_exit_signal(_signum: int, _frame: FrameType | None) -> None:
        save_data(book, notebook)
        print("\nGood bye!")
        raise SystemExit(0)

    signal.signal(signal.SIGTERM, handle_exit_signal)
    if hasattr(signal, "SIGHUP"):
        signal.signal(signal.SIGHUP, handle_exit_signal)

    print("Welcome to the assistant bot!")
    print("Type 'help' to see available commands.")

    try:
        while True:
            user_input = input("Enter a command: ").strip()

            command, args = parse_input(user_input)

            if not command:
                continue

            if command in {"close", "exit"}:
                print("Good bye!")
                break

            if command == "hello":
                print("How can I help you?")
                continue

            if command == "help":
                print(_help_text())
                continue

            result = "Invalid command."
            should_save = False

            if command == "add":
                result = add_contact(args, book)
                should_save = _is_successful_mutation(result)
            elif command == "change":
                result = change_contact(args, book)
                should_save = _is_successful_mutation(result)
            elif command == "phone":
                result = show_phone(args, book)
            elif command == "all":
                result = show_all(book)
            elif command == "delete-contact":
                result = delete_contact(args, book)
                should_save = _is_successful_mutation(result)
            elif command == "add-birthday":
                result = add_birthday_handler(args, book)
                should_save = _is_successful_mutation(result)
            elif command == "show-birthday":
                result = show_birthday_handler(args, book)
            elif command == "birthdays":
                result = birthdays_handler(args, book)
            elif command == "add-email":
                result = add_email_handler(args, book)
                should_save = _is_successful_mutation(result)
            elif command == "add-address":
                if len(args) >= 2:
                    result = add_address_handler([args[0], " ".join(args[1:])], book)
                else:
                    result = add_address_handler(args, book)
                should_save = _is_successful_mutation(result)
            elif command == "search":
                query_args = [" ".join(args)] if args else []
                result = search_contact(query_args, book)
            elif command == "add-note":
                title_args = [" ".join(args)] if args else []
                result = add_note_handler(title_args, notebook)
                should_save = _is_successful_mutation(result)
            elif command == "all-notes":
                result = all_notes_handler(notebook)
            elif command == "delete-note":
                result = delete_note_handler(args, notebook)
                should_save = _is_successful_mutation(result)
            elif command == "edit-note":
                result = edit_note_handler(args, notebook)
                should_save = _is_successful_mutation(result)
            elif command == "add-tag":
                result = add_tag_handler(args, notebook)
                should_save = _is_successful_mutation(result)
            elif command == "find-note":
                query_args = [" ".join(args)] if args else []
                result = find_note_handler(query_args, notebook)
            elif command == "find-by-tag":
                result = find_by_tag_handler(args, notebook)
            elif command in {"sort-notes", "sort-notes-by-tag"}:
                result = sort_notes_by_tag_handler(notebook)

            print(result)

            if should_save:
                save_data(book, notebook)
    except (KeyboardInterrupt, EOFError):
        print("\nGood bye!")
    finally:
        save_data(book, notebook)


if __name__ == "__main__":
    main()

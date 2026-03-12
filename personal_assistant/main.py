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
    return (
        "Available commands:\n"
        "  hello\n"
        "  add <name> <phone>\n"
        "  change <name> <old_phone> <new_phone>\n"
        "  phone <name>\n"
        "  all\n"
        "  delete-contact <name>\n"
        "  add-birthday <name> <dd.mm.yyyy>\n"
        "  show-birthday <name>\n"
        "  birthdays [days]\n"
        "  add-email <name> <email>\n"
        "  add-address <name> <address>\n"
        "  search <query>\n"
        "  add-note <title>\n"
        "  all-notes\n"
        "  delete-note <note_id>\n"
        "  edit-note <note_id>\n"
        "  add-tag <note_id> <tag>\n"
        "  find-note <query>\n"
        "  find-by-tag <tag>\n"
        "  sort-notes | sort-notes-by-tag\n"
        "  help\n"
        "  close | exit"
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

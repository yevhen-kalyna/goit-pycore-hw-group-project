from personal_assistant.models.address_book import AddressBook  # noqa: F401
from personal_assistant.models.note_book import NoteBook  # noqa: F401
from personal_assistant.storage import load_data, save_data  # noqa: F401


def parse_input(user_input: str) -> tuple[str, list[str]]:
    """Парсить введення користувача на команду та аргументи."""
    raise NotImplementedError


def main() -> None:
    """Головний цикл CLI-застосунку."""
    raise NotImplementedError


if __name__ == "__main__":
    main()

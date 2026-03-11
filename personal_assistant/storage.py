import pickle
from pathlib import Path

from personal_assistant.models.address_book import AddressBook
from personal_assistant.models.note_book import NoteBook


def save_data(book: AddressBook, notebook: NoteBook, filename: str = "assistant_data.pkl") -> None:
    """Зберігає AddressBook та NoteBook у файл за допомогою pickle."""
    data = {"book": book, "notebook": notebook}
    with open(filename, "wb") as file:
        pickle.dump(data, file)


def load_data(filename: str = "assistant_data.pkl") -> tuple[AddressBook, NoteBook]:
    """Завантажує AddressBook та NoteBook з файлу. Повертає порожні екземпляри, якщо файл не знайдено."""
    path = Path(filename)
    if not path.exists():
        return AddressBook(), NoteBook()

    try:
        with open(path, "rb") as file:
            data = pickle.load(file)
    except(OSError, EOFError,pickle.UnpicklingError):
        return AddressBook(), NoteBook()

    loaded_book = data.get("book") if isinstance(data, dict) else None
    loaded_notebook = data.get("notebook") if isinstance(data, dict) else None

    if not isinstance(loaded_book, AddressBook):
        loaded_book = AddressBook()

    if not isinstance(loaded_notebook, NoteBook):
        loaded_notebook = NoteBook()

    return loaded_book, loaded_notebook

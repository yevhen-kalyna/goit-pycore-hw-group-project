from personal_assistant.models.address_book import AddressBook
from personal_assistant.models.note_book import NoteBook


def save_data(book: AddressBook, notebook: NoteBook, filename: str = "assistant_data.pkl") -> None:
    """Зберігає AddressBook та NoteBook у файл за допомогою pickle."""
    raise NotImplementedError


def load_data(filename: str = "assistant_data.pkl") -> tuple[AddressBook, NoteBook]:
    """Завантажує AddressBook та NoteBook з файлу. Повертає порожні екземпляри, якщо файл не знайдено."""
    raise NotImplementedError

from personal_assistant.models.note_book import NoteBook
from personal_assistant.utils import input_error


@input_error
def add_note_handler(args: list[str], notebook: NoteBook) -> str:
    """Додає нову нотатку."""
    raise NotImplementedError


@input_error
def find_note_handler(args: list[str], notebook: NoteBook) -> str:
    """Пошук нотаток за текстом."""
    raise NotImplementedError


@input_error
def edit_note_handler(args: list[str], notebook: NoteBook) -> str:
    """Редагує нотатку."""
    raise NotImplementedError


@input_error
def delete_note_handler(args: list[str], notebook: NoteBook) -> str:
    """Видаляє нотатку."""
    raise NotImplementedError


@input_error
def all_notes_handler(notebook: NoteBook) -> str:
    """Показує всі нотатки."""
    raise NotImplementedError


@input_error
def add_tag_handler(args: list[str], notebook: NoteBook) -> str:
    """Додає тег до нотатки."""
    raise NotImplementedError


@input_error
def find_by_tag_handler(args: list[str], notebook: NoteBook) -> str:
    """Пошук нотаток за тегом."""
    raise NotImplementedError


@input_error
def sort_notes_by_tag_handler(notebook: NoteBook) -> str:
    """Сортує нотатки за тегами."""
    raise NotImplementedError

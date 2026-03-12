from personal_assistant.models.note import Note
from personal_assistant.models.note_book import NoteBook
from personal_assistant.utils import input_error

_NOTE_NOT_FOUND = "Note not found."


def _format_note(note: Note) -> str:
    return f"ID: {note.id}\n{note}"


@input_error
def add_note_handler(args: list[str], notebook: NoteBook) -> str:
    """Додає нову нотатку."""
    if not args:
        raise IndexError
    title = args[0]
    body = input("Enter note body: ")
    note = Note(title, body)
    notebook.add_note(note)
    return "Note added."


@input_error
def find_note_handler(args: list[str], notebook: NoteBook) -> str:
    """Пошук нотаток за текстом."""
    if not args:
        raise IndexError
    query = args[0]
    results = notebook.find_by_text(query)
    if not results:
        return "No notes found."
    return "\n".join(_format_note(note) for note in results)


@input_error
def edit_note_handler(args: list[str], notebook: NoteBook) -> str:
    """Редагує нотатку."""
    if not args:
        raise IndexError
    note_id = args[0]
    note = notebook.find(note_id)
    if note is None:
        return _NOTE_NOT_FOUND
    new_body = input("Enter new note body: ")
    notebook.edit_note(note_id, new_body)
    return "Note updated."


@input_error
def delete_note_handler(args: list[str], notebook: NoteBook) -> str:
    """Видаляє нотатку."""
    if not args:
        raise IndexError
    note_id = args[0]
    note = notebook.find(note_id)
    if note is None:
        return _NOTE_NOT_FOUND
    notebook.delete(note_id)
    return "Note deleted."


@input_error
def all_notes_handler(notebook: NoteBook) -> str:
    """Показує всі нотатки."""
    if not notebook.data:
        return "No notes saved."
    return "\n".join(_format_note(note) for note in notebook.data.values())


@input_error
def add_tag_handler(args: list[str], notebook: NoteBook) -> str:
    """Додає тег до нотатки."""
    if len(args) < 2:
        raise IndexError
    note_id, tag = args[0], args[1]
    note = notebook.find(note_id)
    if note is None:
        return _NOTE_NOT_FOUND
    note.add_tag(tag)
    return "Tag added."


@input_error
def find_by_tag_handler(args: list[str], notebook: NoteBook) -> str:
    """Пошук нотаток за тегом."""
    if not args:
        raise IndexError
    tag = args[0]
    results = notebook.find_by_tag(tag)
    if not results:
        return "No notes found."
    return "\n".join(_format_note(note) for note in results)


@input_error
def sort_notes_by_tag_handler(notebook: NoteBook) -> str:
    """Сортує нотатки за тегами."""
    if not notebook.data:
        return "No notes saved."
    sorted_notes = notebook.sort_by_tags()
    return "\n".join(_format_note(note) for note in sorted_notes)

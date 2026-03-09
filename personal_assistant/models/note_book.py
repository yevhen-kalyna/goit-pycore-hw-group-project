from collections import UserDict

from personal_assistant.models.note import Note


class NoteBook(UserDict[str, Note]):
    """Клас для зберігання та керування нотатками."""

    def add_note(self, note: Note) -> None:
        raise NotImplementedError

    def find(self, note_id: str) -> Note | None:
        raise NotImplementedError

    def delete(self, note_id: str) -> None:
        raise NotImplementedError

    def edit_note(self, note_id: str, new_body: str) -> None:
        raise NotImplementedError

    def find_by_text(self, query: str) -> list[Note]:
        raise NotImplementedError

    def find_by_tag(self, tag: str) -> list[Note]:
        raise NotImplementedError

    def sort_by_tags(self) -> list[Note]:
        raise NotImplementedError

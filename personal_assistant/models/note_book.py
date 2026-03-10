from collections import UserDict

from personal_assistant.models.note import Note


class NoteBook(UserDict[str, Note]):
    """Клас для зберігання та керування нотатками."""

    def add_note(self, note: Note) -> None:
        self.data[note.id] = note

    def find(self, note_id: str) -> Note | None:
        return self.data.get(note_id)

    def delete(self, note_id: str) -> None:
        self.data.pop(note_id, None)

    def edit_note(self, note_id: str, new_body: str) -> None:
        note = self.find(note_id)
        if note is None:
            raise KeyError(note_id)
        note.body = new_body

    def find_by_text(self, query: str) -> list[Note]:
        query_lower = query.casefold()
        return [note for note in self.data.values() if query_lower in f"{note.title} {note.body}".casefold()]

    def find_by_tag(self, tag: str) -> list[Note]:
        return [note for note in self.data.values() if tag in note.tags]

    def sort_by_tags(self) -> list[Note]:
        return sorted(
            self.data.values(),
            key=lambda note: (not note.tags, note.tags[0].lower() if note.tags else ""),
        )

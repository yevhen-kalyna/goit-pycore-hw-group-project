from collections import UserDict

from personal_assistant.models.record import Record


class AddressBook(UserDict[str, Record]):
    """Клас для зберігання та керування записами контактів."""

    def add_record(self, record: Record) -> None:
        raise NotImplementedError

    def find(self, name: str) -> Record | None:
        raise NotImplementedError

    def delete(self, name: str) -> None:
        raise NotImplementedError

    def search(self, query: str) -> list[Record]:
        raise NotImplementedError

    def get_upcoming_birthdays(self, days: int = 7) -> list[dict[str, str]]:
        raise NotImplementedError

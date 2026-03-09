import uuid
from datetime import datetime


class Note:
    """Клас для зберігання нотатки з тегами."""

    def __init__(self, title: str, body: str) -> None:
        self.title: str
        self.body: str
        self.tags: list[str]
        self.created_at: datetime
        self.id: str
        raise NotImplementedError

    def add_tag(self, tag: str) -> None:
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError

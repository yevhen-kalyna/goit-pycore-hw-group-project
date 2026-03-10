from datetime import datetime
from uuid import uuid4


class Note:
    """Клас для зберігання нотатки з тегами."""

    def __init__(self, title: str, body: str) -> None:
        self.title: str = title
        self.body: str = body
        self.tags: list[str] = []
        self.created_at: datetime = datetime.now()
        self.id: str = uuid4().hex

    def add_tag(self, tag: str) -> None:
        self.tags.append(tag)

    def __str__(self) -> str:
        tags_text = ", ".join(self.tags) if self.tags else "-"
        return f"[{self.id}] {self.title}: {self.body} | tags: {tags_text}"

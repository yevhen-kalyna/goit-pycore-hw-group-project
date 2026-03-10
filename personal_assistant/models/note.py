from datetime import datetime
from uuid import uuid4


class Note:
    """Клас для зберігання нотатки з тегами."""

    def __init__(self, title: str, body: str) -> None:
        # Зберігаємо заголовок нотатки
        self.title: str = title

        # Зберігаємо основний текст нотатки
        self.body: str = body

        # На старті нотатки немає тегів
        self.tags: list[str] = []

        # Фіксуємо дату і час створення нотатки
        self.created_at: datetime = datetime.now()

        # Генеруємо унікальний ідентифікатор для нотатки
        self.id: str = uuid4().hex

    def add_tag(self, tag: str) -> None:
        # Додаємо новий тег до списку тегів
        self.tags.append(tag)

    def __str__(self) -> str:
        # Якщо тегів немає, показуємо текст "без тегів"
        tags_text = ", ".join(self.tags) if self.tags else "без тегів"

        # Формуємо зручне текстове представлення нотатки
        return f"[{self.id}] {self.title}: {self.body} | tags: {tags_text}"

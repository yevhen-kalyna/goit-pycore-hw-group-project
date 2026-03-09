from personal_assistant.models.fields import Address, Birthday, Email, Name, Phone


class Record:
    """Клас для зберігання даних одного контакту."""

    def __init__(self, name: str) -> None:
        self.name: Name
        self.phones: list[Phone]
        self.birthday: Birthday | None
        self.email: Email | None
        self.address: Address | None
        raise NotImplementedError

    def add_phone(self, phone: str) -> None:
        raise NotImplementedError

    def remove_phone(self, phone: str) -> None:
        raise NotImplementedError

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        raise NotImplementedError

    def find_phone(self, phone: str) -> Phone | None:
        raise NotImplementedError

    def add_birthday(self, birthday: str) -> None:
        raise NotImplementedError

    def add_email(self, email: str) -> None:
        raise NotImplementedError

    def add_address(self, address: str) -> None:
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError

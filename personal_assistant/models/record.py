from personal_assistant.models.fields import Address, Birthday, Email, Name, Phone


class Record:
    """Клас для зберігання даних одного контакту."""

    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Birthday | None = None
        self.email: Email | None = None
        self.address: Address | None = None

    def add_phone(self, phone: str) -> None:
        new_phone = Phone(phone)
        if self.find_phone(new_phone.value) is not None:
            raise ValueError(f"Phone {phone} already exists.")
        self.phones.append(new_phone)

    def remove_phone(self, phone: str) -> None:
        target = self.find_phone(phone)
        if target is None:
            raise ValueError(f"Phone {phone} not found.")
        self.phones.remove(target)

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        target = self.find_phone(old_phone)
        if target is None:
            raise ValueError(f"Phone {old_phone} not found.")
        index = self.phones.index(target)
        self.phones[index] = Phone(new_phone)

    def find_phone(self, phone: str) -> Phone | None:
        return next((p for p in self.phones if p.value == phone), None)

    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def add_email(self, email: str) -> None:
        self.email = Email(email)

    def add_address(self, address: str) -> None:
        self.address = Address(address)

    def __str__(self) -> str:
        phones = ", ".join(str(p) for p in self.phones) if self.phones else "—"
        birthday = str(self.birthday) if self.birthday else "—"
        email = str(self.email) if self.email else "—"
        address = str(self.address) if self.address else "—"
        return f"Name: {self.name} | Phones: {phones} | Birthday: {birthday} | Email: {email} | Address: {address}"

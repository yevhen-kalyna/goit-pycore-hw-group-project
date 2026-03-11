from collections import UserDict
from datetime import date, datetime, timedelta

from personal_assistant.models.record import Record


class AddressBook(UserDict[str, Record]):
    """Клас для зберігання та керування записами контактів."""

    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        self.data.pop(name, None)

    def search(self, query: str) -> list[Record]:
        q = query.lower()
        results: list[Record] = []
        for record in self.data.values():
            if (
                q in record.name.value.lower()
                or any(q in phone.value.lower() for phone in record.phones)
                or (record.email and q in record.email.value.lower())
            ):
                results.append(record)
        return results

    def get_upcoming_birthdays(self, days: int = 7) -> list[dict[str, str]]:
        today = datetime.today().date()
        upcoming: list[dict[str, str]] = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            bday: date = record.birthday.value  # type: ignore[assignment]
            # Feb 29 birthdays are always celebrated on March 1
            if bday.month == 2 and bday.day == 29:
                bday_this_year = date(today.year, 3, 1)
            else:
                bday_this_year = bday.replace(year=today.year)

            if bday_this_year < today:
                if bday.month == 2 and bday.day == 29:
                    bday_this_year = date(today.year + 1, 3, 1)
                else:
                    bday_this_year = bday.replace(year=today.year + 1)

            delta = (bday_this_year - today).days
            if 0 <= delta <= days:
                congratulation_date = bday_this_year
                weekday = congratulation_date.weekday()
                if weekday == 5:  # Saturday
                    congratulation_date += timedelta(days=2)
                elif weekday == 6:  # Sunday
                    congratulation_date += timedelta(days=1)

                upcoming.append(
                    {
                        "name": record.name.value,
                        "congratulation_date": congratulation_date.strftime("%d.%m.%Y"),
                    }
                )

        return upcoming

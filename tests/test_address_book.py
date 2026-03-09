import pytest
from datetime import datetime, timedelta

from personal_assistant.models.address_book import AddressBook
from personal_assistant.models.record import Record


# --- Fixtures ---


@pytest.fixture
def book() -> AddressBook:
    return AddressBook()


@pytest.fixture
def sample_record() -> Record:
    record = Record("Alice")
    record.add_phone("1234567890")
    return record


# --- add_record ---


def test_add_record_stores_in_book(book: AddressBook, sample_record: Record) -> None:
    book.add_record(sample_record)
    assert "Alice" in book.data


def test_add_record_retrievable_by_name(book: AddressBook, sample_record: Record) -> None:
    book.add_record(sample_record)
    assert book.data["Alice"] is sample_record


def test_add_record_same_name_overwrites(book: AddressBook) -> None:
    first = Record("Alice")
    first.add_phone("1111111111")
    book.add_record(first)

    second = Record("Alice")
    second.add_phone("2222222222")
    book.add_record(second)

    assert book.data["Alice"] is second


# --- find ---


def test_find_existing_returns_record(book: AddressBook, sample_record: Record) -> None:
    book.add_record(sample_record)
    result = book.find("Alice")
    assert isinstance(result, Record)


def test_find_existing_name_matches(book: AddressBook, sample_record: Record) -> None:
    book.add_record(sample_record)
    result = book.find("Alice")
    assert result is not None
    assert result.name.value == "Alice"


def test_find_nonexistent_returns_none(book: AddressBook) -> None:
    result = book.find("Nobody")
    assert result is None


# --- delete ---


def test_delete_existing_removes_record(book: AddressBook, sample_record: Record) -> None:
    book.add_record(sample_record)
    book.delete("Alice")
    assert book.find("Alice") is None


def test_delete_nonexistent_does_not_raise(book: AddressBook) -> None:
    book.delete("Nobody")  # should not raise


# --- search ---


def test_search_by_name_partial_match(book: AddressBook, sample_record: Record) -> None:
    book.add_record(sample_record)
    results = book.search("Ali")
    assert len(results) == 1
    assert results[0].name.value == "Alice"


def test_search_by_phone_partial_match(book: AddressBook, sample_record: Record) -> None:
    book.add_record(sample_record)
    results = book.search("1234")
    assert len(results) == 1
    assert results[0].name.value == "Alice"


def test_search_by_email_partial_match(book: AddressBook) -> None:
    record = Record("Alice")
    record.add_email("alice@example.com")
    book.add_record(record)
    results = book.search("alice@ex")
    assert len(results) == 1
    assert results[0].name.value == "Alice"


def test_search_is_case_insensitive(book: AddressBook, sample_record: Record) -> None:
    book.add_record(sample_record)
    results = book.search("alice")
    assert len(results) == 1
    assert results[0].name.value == "Alice"


def test_search_returns_empty_when_no_match(book: AddressBook, sample_record: Record) -> None:
    book.add_record(sample_record)
    results = book.search("zzz_no_match")
    assert results == []


def test_search_returns_multiple_matches(book: AddressBook) -> None:
    alice = Record("Alice")
    alice.add_phone("1234567890")
    alina = Record("Alina")
    alina.add_phone("0987654321")
    book.add_record(alice)
    book.add_record(alina)
    results = book.search("Ali")
    assert len(results) == 2


# --- get_upcoming_birthdays ---


def test_upcoming_birthdays_empty_when_no_birthdays(book: AddressBook) -> None:
    record = Record("Alice")
    book.add_record(record)
    result = book.get_upcoming_birthdays()
    assert result == []


def test_upcoming_birthdays_includes_birthday_within_7_days(book: AddressBook) -> None:
    today = datetime.today()
    upcoming_date = today + timedelta(days=3)
    birthday_str = upcoming_date.strftime("%d.%m.%Y")

    record = Record("Alice")
    record.add_birthday(birthday_str)
    book.add_record(record)

    result = book.get_upcoming_birthdays()
    assert len(result) == 1
    assert result[0]["name"] == "Alice"


def test_upcoming_birthdays_excludes_birthday_beyond_7_days(book: AddressBook) -> None:
    today = datetime.today()
    far_date = today + timedelta(days=10)
    birthday_str = far_date.strftime("%d.%m.%Y")

    record = Record("Alice")
    record.add_birthday(birthday_str)
    book.add_record(record)

    result = book.get_upcoming_birthdays()
    assert result == []


def test_upcoming_birthdays_custom_days_parameter(book: AddressBook) -> None:
    today = datetime.today()
    future_date = today + timedelta(days=20)
    birthday_str = future_date.strftime("%d.%m.%Y")

    record = Record("Alice")
    record.add_birthday(birthday_str)
    book.add_record(record)

    result = book.get_upcoming_birthdays(days=30)
    assert len(result) == 1
    assert result[0]["name"] == "Alice"


def test_upcoming_birthdays_result_has_required_keys(book: AddressBook) -> None:
    today = datetime.today()
    upcoming_date = today + timedelta(days=2)
    birthday_str = upcoming_date.strftime("%d.%m.%Y")

    record = Record("Alice")
    record.add_birthday(birthday_str)
    book.add_record(record)

    result = book.get_upcoming_birthdays()
    assert len(result) == 1
    assert "name" in result[0]
    assert "congratulation_date" in result[0]


def test_upcoming_birthdays_saturday_shifts_to_monday(book: AddressBook) -> None:
    today = datetime.today()
    # Find the next Saturday within 7 days
    days_until_saturday = (5 - today.weekday()) % 7
    if days_until_saturday == 0:
        days_until_saturday = 7
    # If Saturday is beyond 7 days, we need a different approach:
    # use a Saturday that is within range by choosing days=14 if needed
    saturday_date = today + timedelta(days=days_until_saturday)

    record = Record("Alice")
    record.add_birthday(saturday_date.strftime("%d.%m.%Y"))
    book.add_record(record)

    result = book.get_upcoming_birthdays(days=days_until_saturday + 1)
    assert len(result) == 1

    congratulation = datetime.strptime(result[0]["congratulation_date"], "%d.%m.%Y")
    # Saturday birthday should shift to Monday
    assert congratulation.weekday() == 0  # Monday


def test_upcoming_birthdays_sunday_shifts_to_monday(book: AddressBook) -> None:
    today = datetime.today()
    # Find the next Sunday within reach
    days_until_sunday = (6 - today.weekday()) % 7
    if days_until_sunday == 0:
        days_until_sunday = 7
    sunday_date = today + timedelta(days=days_until_sunday)

    record = Record("Alice")
    record.add_birthday(sunday_date.strftime("%d.%m.%Y"))
    book.add_record(record)

    result = book.get_upcoming_birthdays(days=days_until_sunday + 1)
    assert len(result) == 1

    congratulation = datetime.strptime(result[0]["congratulation_date"], "%d.%m.%Y")
    # Sunday birthday should shift to Monday
    assert congratulation.weekday() == 0  # Monday


def test_upcoming_birthdays_feb29_in_non_leap_year(
    book: AddressBook, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Feb 29 birthday should be treated as March 1 in non-leap years."""
    import personal_assistant.models.address_book as ab_module

    class FakeDatetime(datetime):
        @classmethod
        def today(cls) -> "FakeDatetime":  # type: ignore[override]
            return cls(2024, 2, 27)

    if hasattr(ab_module, "datetime"):
        monkeypatch.setattr(ab_module, "datetime", FakeDatetime)

    record = Record("Alice")
    record.add_birthday("29.02.2000")
    book.add_record(record)

    result = book.get_upcoming_birthdays()
    assert len(result) == 1
    assert result[0]["name"] == "Alice"
    assert result[0]["congratulation_date"] == "01.03.2024"

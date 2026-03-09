import datetime

import pytest

from personal_assistant.models.record import Record

# --- Constructor ---


def test_record_creates_name() -> None:
    record = Record("Alice")
    assert record.name.value == "Alice"


def test_record_phones_initially_empty() -> None:
    record = Record("Alice")
    assert record.phones == []


def test_record_birthday_initially_none() -> None:
    record = Record("Alice")
    assert record.birthday is None


def test_record_email_initially_none() -> None:
    record = Record("Alice")
    assert record.email is None


def test_record_address_initially_none() -> None:
    record = Record("Alice")
    assert record.address is None


# --- add_phone ---


def test_add_phone_increases_count_to_one() -> None:
    record = Record("Alice")
    record.add_phone("1234567890")
    assert len(record.phones) == 1


def test_add_two_phones_increases_count_to_two() -> None:
    record = Record("Alice")
    record.add_phone("1234567890")
    record.add_phone("0987654321")
    assert len(record.phones) == 2


def test_add_phone_stores_value_correctly() -> None:
    record = Record("Alice")
    record.add_phone("1234567890")
    assert record.phones[0].value == "1234567890"


def test_add_phone_invalid_raises_value_error() -> None:
    record = Record("Alice")
    with pytest.raises(ValueError):
        record.add_phone("invalid")


# --- remove_phone ---


def test_remove_phone_existing_makes_list_empty() -> None:
    record = Record("Alice")
    record.add_phone("1234567890")
    record.remove_phone("1234567890")
    assert len(record.phones) == 0


def test_remove_phone_non_existing_raises_value_error() -> None:
    record = Record("Alice")
    with pytest.raises(ValueError):
        record.remove_phone("1234567890")


# --- edit_phone ---


def test_edit_phone_replaces_old_with_new() -> None:
    record = Record("Alice")
    record.add_phone("1234567890")
    record.edit_phone("1234567890", "0987654321")
    assert record.find_phone("0987654321") is not None


def test_edit_phone_old_value_no_longer_present() -> None:
    record = Record("Alice")
    record.add_phone("1234567890")
    record.edit_phone("1234567890", "0987654321")
    assert record.find_phone("1234567890") is None


def test_edit_phone_non_existing_raises_value_error() -> None:
    record = Record("Alice")
    with pytest.raises(ValueError):
        record.edit_phone("1234567890", "0987654321")


def test_edit_phone_invalid_new_value_raises_value_error() -> None:
    record = Record("Alice")
    record.add_phone("1234567890")
    with pytest.raises(ValueError):
        record.edit_phone("1234567890", "invalid")


# --- find_phone ---


def test_find_phone_existing_returns_phone_object() -> None:
    record = Record("Alice")
    record.add_phone("1234567890")
    phone = record.find_phone("1234567890")
    assert phone is not None
    assert phone.value == "1234567890"


def test_find_phone_non_existing_returns_none() -> None:
    record = Record("Alice")
    assert record.find_phone("1234567890") is None


# --- add_birthday ---


def test_add_birthday_sets_birthday() -> None:
    record = Record("Alice")
    record.add_birthday("15.06.1990")
    assert record.birthday is not None


def test_add_birthday_value_is_date_type() -> None:
    record = Record("Alice")
    record.add_birthday("15.06.1990")
    assert isinstance(record.birthday.value, datetime.date)


def test_add_birthday_stores_correct_date() -> None:
    record = Record("Alice")
    record.add_birthday("15.06.1990")
    assert record.birthday.value == datetime.date(1990, 6, 15)


def test_add_birthday_invalid_raises_value_error() -> None:
    record = Record("Alice")
    with pytest.raises(ValueError):
        record.add_birthday("not-a-date")


# --- add_email ---


def test_add_email_sets_email() -> None:
    record = Record("Alice")
    record.add_email("alice@example.com")
    assert record.email is not None


def test_add_email_stores_value_correctly() -> None:
    record = Record("Alice")
    record.add_email("alice@example.com")
    assert record.email.value == "alice@example.com"


def test_add_email_invalid_raises_value_error() -> None:
    record = Record("Alice")
    with pytest.raises(ValueError):
        record.add_email("not-an-email")


# --- add_address ---


def test_add_address_sets_address() -> None:
    record = Record("Alice")
    record.add_address("123 Main St, Kyiv, Ukraine")
    assert record.address is not None


def test_add_address_stores_value_correctly() -> None:
    record = Record("Alice")
    record.add_address("123 Main St, Kyiv, Ukraine")
    assert record.address.value == "123 Main St, Kyiv, Ukraine"


# --- __str__ ---


def test_str_contains_name() -> None:
    record = Record("Alice")
    assert "Alice" in str(record)


def test_str_contains_phone_when_present() -> None:
    record = Record("Alice")
    record.add_phone("1234567890")
    assert "1234567890" in str(record)


def test_str_contains_birthday_when_set() -> None:
    record = Record("Alice")
    record.add_birthday("15.06.1990")
    result = str(record)
    assert "15.06.1990" in result or "1990" in result

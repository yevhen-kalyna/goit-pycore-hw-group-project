from datetime import date

import pytest

from personal_assistant.models.fields import Address, Birthday, Email, Field, Name, Phone

# --- Field ---


def test_field_stores_value() -> None:
    field = Field("test")
    assert field.value == "test"


def test_field_str_returns_string_representation() -> None:
    field = Field("hello")
    assert str(field) == "hello"


# --- Name ---


def test_name_valid_creation() -> None:
    name = Name("Alice")
    assert isinstance(name, Field)


def test_name_stores_value() -> None:
    name = Name("Bob")
    assert name.value == "Bob"


# --- Phone ---


def test_phone_valid_ten_digits() -> None:
    phone = Phone("1234567890")
    assert phone.value == "1234567890"


def test_phone_value_stored_correctly() -> None:
    phone = Phone("0987654321")
    assert str(phone) == "0987654321"


def test_phone_invalid_too_short() -> None:
    with pytest.raises(ValueError):
        Phone("12345")


def test_phone_invalid_too_long() -> None:
    with pytest.raises(ValueError):
        Phone("123456789012")


def test_phone_invalid_contains_letters() -> None:
    with pytest.raises(ValueError):
        Phone("12345abcde")


def test_phone_invalid_contains_special_chars() -> None:
    with pytest.raises(ValueError):
        Phone("123-456-78")


def test_phone_invalid_empty_string() -> None:
    with pytest.raises(ValueError):
        Phone("")


# --- Email ---


def test_email_valid_simple() -> None:
    email = Email("user@example.com")
    assert email.value == "user@example.com"


def test_email_valid_with_dots_and_subdomain() -> None:
    email = Email("user.name@domain.co.uk")
    assert email.value == "user.name@domain.co.uk"


def test_email_valid_with_plus_tag() -> None:
    email = Email("user+tag@example.org")
    assert email.value == "user+tag@example.org"


def test_email_invalid_no_at_sign() -> None:
    with pytest.raises(ValueError):
        Email("not-an-email")


def test_email_invalid_no_local_part() -> None:
    with pytest.raises(ValueError):
        Email("@domain.com")


def test_email_invalid_no_domain() -> None:
    with pytest.raises(ValueError):
        Email("user@")


def test_email_invalid_dot_after_at() -> None:
    with pytest.raises(ValueError):
        Email("user@.com")


def test_email_invalid_empty_string() -> None:
    with pytest.raises(ValueError):
        Email("")


# --- Address ---


def test_address_stores_value() -> None:
    address = Address("123 Main St, Kyiv, Ukraine")
    assert address.value == "123 Main St, Kyiv, Ukraine"


def test_address_str_works_correctly() -> None:
    address = Address("456 Oak Ave")
    assert str(address) == "456 Oak Ave"


# --- Birthday ---


def test_birthday_valid_date() -> None:
    birthday = Birthday("15.06.1990")
    assert birthday.value is not None


def test_birthday_stored_value_is_date_type() -> None:
    birthday = Birthday("15.06.1990")
    assert isinstance(birthday.value, date)


def test_birthday_stored_value_matches_expected_date() -> None:
    birthday = Birthday("15.06.1990")
    assert birthday.value == date(1990, 6, 15)


def test_birthday_invalid_wrong_format_iso() -> None:
    with pytest.raises(ValueError):
        Birthday("1990-06-15")


def test_birthday_invalid_impossible_date() -> None:
    with pytest.raises(ValueError):
        Birthday("32.13.2000")


def test_birthday_invalid_not_a_date() -> None:
    with pytest.raises(ValueError):
        Birthday("not-a-date")

from unittest.mock import patch

import pytest

from personal_assistant.handlers.contact_handlers import (
    add_address_handler,
    add_birthday_handler,
    add_contact,
    add_email_handler,
    birthdays_handler,
    change_contact,
    delete_contact,
    search_contact,
    show_all,
    show_birthday_handler,
    show_phone,
)
from personal_assistant.handlers.note_handlers import (
    add_note_handler,
    add_tag_handler,
    all_notes_handler,
    delete_note_handler,
    edit_note_handler,
    find_by_tag_handler,
    find_note_handler,
    sort_notes_by_tag_handler,
)
from personal_assistant.models.address_book import AddressBook
from personal_assistant.models.note_book import NoteBook
from personal_assistant.models.record import Record
from personal_assistant.utils import input_error

# ==================== Fixtures ====================


@pytest.fixture
def book() -> AddressBook:
    return AddressBook()


@pytest.fixture
def notebook() -> NoteBook:
    return NoteBook()


@pytest.fixture
def book_with_contact() -> AddressBook:
    book = AddressBook()
    record = Record("Alice")
    record.add_phone("1234567890")
    book.add_record(record)
    return book


# ==================== input_error decorator ====================


def test_input_error_catches_value_error() -> None:
    @input_error
    def raise_value_error(args: list[str], book: AddressBook) -> str:
        raise ValueError("invalid value")

    result = raise_value_error([], AddressBook())
    assert result == "invalid value"


def test_input_error_catches_key_error() -> None:
    @input_error
    def raise_key_error(args: list[str], book: AddressBook) -> str:
        raise KeyError("Alice")

    result = raise_key_error([], AddressBook())
    assert result == "Contact not found."


def test_input_error_catches_index_error() -> None:
    @input_error
    def raise_index_error(args: list[str], book: AddressBook) -> str:
        raise IndexError()

    result = raise_index_error([], AddressBook())
    assert result == "Enter the argument for the command."


# ==================== Contact Handlers ====================

# --- add_contact ---


def test_add_contact_new_contact(book: AddressBook) -> None:
    result = add_contact(["Alice", "1234567890"], book)
    assert result == "Contact added."


def test_add_contact_existing_contact_adds_phone(book_with_contact: AddressBook) -> None:
    result = add_contact(["Alice", "0987654321"], book_with_contact)
    assert result == "Contact updated."


def test_add_contact_missing_args(book: AddressBook) -> None:
    result = add_contact([], book)
    assert result == "Enter the argument for the command."


# --- change_contact ---


def test_change_contact_existing_phone(book_with_contact: AddressBook) -> None:
    result = change_contact(["Alice", "1234567890", "0987654321"], book_with_contact)
    assert result == "Contact updated."


def test_change_contact_not_found(book: AddressBook) -> None:
    result = change_contact(["Bob", "1234567890", "0987654321"], book)
    assert result == "Contact not found."


# --- show_phone ---


def test_show_phone_existing_contact(book_with_contact: AddressBook) -> None:
    result = show_phone(["Alice"], book_with_contact)
    assert "1234567890" in result


def test_show_phone_contact_not_found(book: AddressBook) -> None:
    result = show_phone(["NonExistent"], book)
    assert result == "Contact not found."


# --- show_all ---


def test_show_all_empty_book(book: AddressBook) -> None:
    result = show_all(book)
    assert result == "No contacts saved."


def test_show_all_with_contacts(book_with_contact: AddressBook) -> None:
    result = show_all(book_with_contact)
    assert "Alice" in result


# --- delete_contact ---


def test_delete_contact_existing(book_with_contact: AddressBook) -> None:
    result = delete_contact(["Alice"], book_with_contact)
    assert result == "Contact deleted."


# --- add_birthday_handler ---


def test_add_birthday_handler_success(book_with_contact: AddressBook) -> None:
    result = add_birthday_handler(["Alice", "15.06.1990"], book_with_contact)
    assert result == "Birthday added."


def test_add_birthday_handler_contact_not_found(book: AddressBook) -> None:
    result = add_birthday_handler(["NonExistent", "15.06.1990"], book)
    assert result == "Contact not found."


# --- show_birthday_handler ---


def test_show_birthday_handler_with_birthday(book_with_contact: AddressBook) -> None:
    add_birthday_handler(["Alice", "15.06.1990"], book_with_contact)
    result = show_birthday_handler(["Alice"], book_with_contact)
    assert "15.06.1990" in result


def test_show_birthday_handler_no_birthday(book_with_contact: AddressBook) -> None:
    result = show_birthday_handler(["Alice"], book_with_contact)
    assert result == "Birthday not set."


def test_show_birthday_handler_contact_not_found(book: AddressBook) -> None:
    result = show_birthday_handler(["NonExistent"], book)
    assert result == "Contact not found."


# --- birthdays_handler ---


def test_birthdays_handler_no_upcoming(book: AddressBook) -> None:
    result = birthdays_handler([], book)
    assert result == "No upcoming birthdays."


# --- add_email_handler ---


def test_add_email_handler_success(book_with_contact: AddressBook) -> None:
    result = add_email_handler(["Alice", "alice@example.com"], book_with_contact)
    assert result == "Email added."


def test_add_email_handler_contact_not_found(book: AddressBook) -> None:
    result = add_email_handler(["NonExistent", "test@example.com"], book)
    assert result == "Contact not found."


# --- add_address_handler ---


def test_add_address_handler_success(book_with_contact: AddressBook) -> None:
    result = add_address_handler(["Alice", "123 Main St, Kyiv"], book_with_contact)
    assert result == "Address added."


def test_add_address_handler_contact_not_found(book: AddressBook) -> None:
    result = add_address_handler(["NonExistent", "123 Main St"], book)
    assert result == "Contact not found."


# --- search_contact ---


def test_search_contact_found(book_with_contact: AddressBook) -> None:
    result = search_contact(["Alice"], book_with_contact)
    assert "Alice" in result


def test_search_contact_no_match(book_with_contact: AddressBook) -> None:
    result = search_contact(["ZZZ"], book_with_contact)
    assert result == "No contacts found."


# ==================== Note Handlers ====================

# --- add_note_handler ---


def test_add_note_handler_success(notebook: NoteBook) -> None:
    with patch("builtins.input", return_value="Note body text"):
        result = add_note_handler(["Shopping"], notebook)
    assert result == "Note added."


# --- all_notes_handler ---


def test_all_notes_handler_empty(notebook: NoteBook) -> None:
    result = all_notes_handler(notebook)
    assert result == "No notes saved."


def test_all_notes_handler_with_notes(notebook: NoteBook) -> None:
    with patch("builtins.input", return_value="Buy milk"):
        add_note_handler(["Shopping"], notebook)
    result = all_notes_handler(notebook)
    assert "Shopping" in result


# --- delete_note_handler ---


def test_delete_note_handler_success(notebook: NoteBook) -> None:
    with patch("builtins.input", return_value="Buy milk"):
        add_note_handler(["Shopping"], notebook)
    notes_str = all_notes_handler(notebook)
    note_id = _extract_note_id(notes_str)
    result = delete_note_handler([note_id], notebook)
    assert result == "Note deleted."


# --- edit_note_handler ---


def test_edit_note_handler_success(notebook: NoteBook) -> None:
    with patch("builtins.input", return_value="Buy milk"):
        add_note_handler(["Shopping"], notebook)
    notes_str = all_notes_handler(notebook)
    note_id = _extract_note_id(notes_str)
    with patch("builtins.input", return_value="Buy eggs instead"):
        result = edit_note_handler([note_id], notebook)
    assert result == "Note updated."


def test_edit_note_handler_not_found(notebook: NoteBook) -> None:
    with patch("builtins.input", return_value="New body"):
        result = edit_note_handler(["nonexistent-id"], notebook)
    assert result == "Note not found."


# --- add_tag_handler ---


def test_add_tag_handler_success(notebook: NoteBook) -> None:
    with patch("builtins.input", return_value="Buy milk"):
        add_note_handler(["Shopping"], notebook)
    notes_str = all_notes_handler(notebook)
    note_id = _extract_note_id(notes_str)
    result = add_tag_handler([note_id, "groceries"], notebook)
    assert result == "Tag added."


def test_add_tag_handler_note_not_found(notebook: NoteBook) -> None:
    result = add_tag_handler(["nonexistent-id", "groceries"], notebook)
    assert result == "Note not found."


# --- find_note_handler ---


def test_find_note_handler_found(notebook: NoteBook) -> None:
    with patch("builtins.input", return_value="Buy milk"):
        add_note_handler(["Shopping"], notebook)
    result = find_note_handler(["Shopping"], notebook)
    assert "Shopping" in result


def test_find_note_handler_no_match(notebook: NoteBook) -> None:
    result = find_note_handler(["NonExistent"], notebook)
    assert result == "No notes found."


# --- find_by_tag_handler ---


def test_find_by_tag_handler_found(notebook: NoteBook) -> None:
    with patch("builtins.input", return_value="Buy milk"):
        add_note_handler(["Shopping"], notebook)
    notes_str = all_notes_handler(notebook)
    note_id = _extract_note_id(notes_str)
    add_tag_handler([note_id, "groceries"], notebook)
    result = find_by_tag_handler(["groceries"], notebook)
    assert "Shopping" in result


def test_find_by_tag_handler_no_match(notebook: NoteBook) -> None:
    result = find_by_tag_handler(["nonexistent"], notebook)
    assert result == "No notes found."


# --- sort_notes_by_tag_handler ---


def test_sort_notes_by_tag_handler_empty(notebook: NoteBook) -> None:
    result = sort_notes_by_tag_handler(notebook)
    assert result == "No notes saved."


def test_sort_notes_by_tag_handler_with_notes(notebook: NoteBook) -> None:
    with patch("builtins.input", return_value="Buy milk"):
        add_note_handler(["Shopping"], notebook)
    result = sort_notes_by_tag_handler(notebook)
    assert "Shopping" in result


# ==================== Helpers ====================


def _extract_note_id(notes_str: str) -> str:
    """Extract the first note ID from a formatted notes string.

    Assumes the ID appears after 'ID: ' prefix on a line or as the first
    token in a structured output. Falls back to the first 8+ char hex-like
    token found in the string.
    """
    for line in notes_str.splitlines():
        stripped = line.strip()
        if stripped.lower().startswith("id:"):
            return stripped.split(":", 1)[1].strip()
    # Fallback: find first token that looks like a UUID or short-id
    for token in notes_str.replace("|", " ").replace(",", " ").split():
        cleaned = token.strip(":")
        if len(cleaned) >= 8 and not cleaned.isalpha():
            return cleaned
    raise ValueError(f"Could not extract note ID from output:\n{notes_str}")

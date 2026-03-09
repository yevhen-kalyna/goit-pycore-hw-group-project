from pathlib import Path

import pytest

from personal_assistant.models.address_book import AddressBook
from personal_assistant.models.note import Note
from personal_assistant.models.note_book import NoteBook
from personal_assistant.models.record import Record
from personal_assistant.storage import load_data, save_data

# --- Fixtures ---


@pytest.fixture()
def populated_address_book() -> AddressBook:
    book = AddressBook()
    record = Record("Alice")
    record.add_phone("1234567890")
    record.add_birthday("15.06.1990")
    book.add_record(record)
    return book


@pytest.fixture()
def populated_notebook() -> NoteBook:
    notebook = NoteBook()
    note = Note("Shopping", "Buy milk and eggs")
    note.add_tag("groceries")
    note.add_tag("urgent")
    notebook.add_note(note)
    return notebook


# --- save_data + load_data round-trip: empty data ---


def test_round_trip_empty_address_book_is_valid_instance(tmp_path: Path) -> None:
    filepath = str(tmp_path / "test_data.pkl")
    save_data(AddressBook(), NoteBook(), filepath)
    loaded_book, _ = load_data(filepath)
    assert isinstance(loaded_book, AddressBook)


def test_round_trip_empty_notebook_is_valid_instance(tmp_path: Path) -> None:
    filepath = str(tmp_path / "test_data.pkl")
    save_data(AddressBook(), NoteBook(), filepath)
    _, loaded_notebook = load_data(filepath)
    assert isinstance(loaded_notebook, NoteBook)


def test_round_trip_empty_address_book_has_no_records(tmp_path: Path) -> None:
    filepath = str(tmp_path / "test_data.pkl")
    save_data(AddressBook(), NoteBook(), filepath)
    loaded_book, _ = load_data(filepath)
    assert len(loaded_book) == 0


def test_round_trip_empty_notebook_has_no_notes(tmp_path: Path) -> None:
    filepath = str(tmp_path / "test_data.pkl")
    save_data(AddressBook(), NoteBook(), filepath)
    _, loaded_notebook = load_data(filepath)
    assert len(loaded_notebook) == 0


# --- save_data + load_data round-trip: populated AddressBook ---


def test_round_trip_address_book_preserves_contact_name(
    tmp_path: Path, populated_address_book: AddressBook, populated_notebook: NoteBook
) -> None:
    filepath = str(tmp_path / "test_data.pkl")
    save_data(populated_address_book, populated_notebook, filepath)
    loaded_book, _ = load_data(filepath)
    record = loaded_book.find("Alice")
    assert record is not None
    assert record.name.value == "Alice"


def test_round_trip_address_book_preserves_phones(
    tmp_path: Path, populated_address_book: AddressBook, populated_notebook: NoteBook
) -> None:
    filepath = str(tmp_path / "test_data.pkl")
    save_data(populated_address_book, populated_notebook, filepath)
    loaded_book, _ = load_data(filepath)
    record = loaded_book.find("Alice")
    assert record is not None
    assert record.phones[0].value == "1234567890"


def test_round_trip_address_book_preserves_birthday(
    tmp_path: Path, populated_address_book: AddressBook, populated_notebook: NoteBook
) -> None:
    filepath = str(tmp_path / "test_data.pkl")
    save_data(populated_address_book, populated_notebook, filepath)
    loaded_book, _ = load_data(filepath)
    record = loaded_book.find("Alice")
    assert record is not None
    assert record.birthday is not None
    assert record.birthday.value.year == 1990
    assert record.birthday.value.month == 6
    assert record.birthday.value.day == 15


# --- save_data + load_data round-trip: populated NoteBook ---


def test_round_trip_notebook_preserves_note_title(
    tmp_path: Path, populated_address_book: AddressBook, populated_notebook: NoteBook
) -> None:
    filepath = str(tmp_path / "test_data.pkl")
    save_data(populated_address_book, populated_notebook, filepath)
    _, loaded_notebook = load_data(filepath)
    notes = list(loaded_notebook.data.values())
    assert len(notes) == 1
    assert notes[0].title == "Shopping"


def test_round_trip_notebook_preserves_note_body(
    tmp_path: Path, populated_address_book: AddressBook, populated_notebook: NoteBook
) -> None:
    filepath = str(tmp_path / "test_data.pkl")
    save_data(populated_address_book, populated_notebook, filepath)
    _, loaded_notebook = load_data(filepath)
    notes = list(loaded_notebook.data.values())
    assert notes[0].body == "Buy milk and eggs"


def test_round_trip_notebook_preserves_tags(
    tmp_path: Path, populated_address_book: AddressBook, populated_notebook: NoteBook
) -> None:
    filepath = str(tmp_path / "test_data.pkl")
    save_data(populated_address_book, populated_notebook, filepath)
    _, loaded_notebook = load_data(filepath)
    notes = list(loaded_notebook.data.values())
    assert notes[0].tags == ["groceries", "urgent"]


# --- load_data with missing file ---


def test_load_missing_file_returns_address_book_instance(tmp_path: Path) -> None:
    filepath = str(tmp_path / "nonexistent.pkl")
    loaded_book, _ = load_data(filepath)
    assert isinstance(loaded_book, AddressBook)


def test_load_missing_file_returns_notebook_instance(tmp_path: Path) -> None:
    filepath = str(tmp_path / "nonexistent.pkl")
    _, loaded_notebook = load_data(filepath)
    assert isinstance(loaded_notebook, NoteBook)


def test_load_missing_file_returns_empty_address_book(tmp_path: Path) -> None:
    filepath = str(tmp_path / "nonexistent.pkl")
    loaded_book, _ = load_data(filepath)
    assert len(loaded_book) == 0


def test_load_missing_file_returns_empty_notebook(tmp_path: Path) -> None:
    filepath = str(tmp_path / "nonexistent.pkl")
    _, loaded_notebook = load_data(filepath)
    assert len(loaded_notebook) == 0


# --- Custom filename ---


def test_save_and_load_with_custom_filename(
    tmp_path: Path, populated_address_book: AddressBook, populated_notebook: NoteBook
) -> None:
    filepath = str(tmp_path / "custom_backup.pkl")
    save_data(populated_address_book, populated_notebook, filepath)
    loaded_book, loaded_notebook = load_data(filepath)
    assert loaded_book.find("Alice") is not None
    notes = list(loaded_notebook.data.values())
    assert len(notes) == 1
    assert notes[0].title == "Shopping"

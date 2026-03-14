"""End-to-end tests for the personal assistant CLI.

Each test launches the actual CLI via subprocess, feeds commands through
stdin, and verifies stdout output.  Tests are isolated via ``tmp_path``
so the data storage file does not leak between tests.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

# ==================== Helpers ====================


def run_cli(
    commands: list[str],
    cwd: Path,
    timeout: int = 10,
) -> subprocess.CompletedProcess[str]:
    """Run the CLI with the given commands fed via stdin."""
    stdin_text = "\n".join(commands) + "\n"
    return subprocess.run(
        [sys.executable, "-m", "personal_assistant.main"],
        input=stdin_text,
        capture_output=True,
        text=True,
        cwd=cwd,
        timeout=timeout,
    )


def extract_note_id(stdout: str) -> str:
    """Extract the first note ID (hex string) from CLI output."""
    match = re.search(r"ID:\s*([0-9a-f]+)", stdout)
    if match is None:
        raise ValueError(f"Could not extract note ID from output:\n{stdout}")
    return match.group(1)


@pytest.fixture()
def cli_dir(tmp_path: Path) -> Path:
    """Isolated working directory for each test."""
    return tmp_path


# ==================== A. Startup & Exit ====================


class TestStartupAndExit:
    def test_welcome_banner(self, cli_dir: Path) -> None:
        result = run_cli(["close"], cli_dir)
        assert "Welcome to the assistant bot!" in result.stdout
        assert "Type 'help' to see available commands." in result.stdout

    def test_exit_close(self, cli_dir: Path) -> None:
        result = run_cli(["close"], cli_dir)
        assert "Good bye!" in result.stdout
        assert result.returncode == 0

    def test_exit_exit(self, cli_dir: Path) -> None:
        result = run_cli(["exit"], cli_dir)
        assert "Good bye!" in result.stdout
        assert result.returncode == 0

    def test_exit_eof(self, cli_dir: Path) -> None:
        """Empty stdin triggers EOFError in the main loop."""
        result = subprocess.run(
            [sys.executable, "-m", "personal_assistant.main"],
            input="",
            capture_output=True,
            text=True,
            cwd=cli_dir,
            timeout=10,
        )
        assert "Good bye!" in result.stdout


# ==================== B. Utility Commands ====================


class TestUtility:
    def test_hello(self, cli_dir: Path) -> None:
        result = run_cli(["hello", "close"], cli_dir)
        assert "How can I help you?" in result.stdout

    def test_help(self, cli_dir: Path) -> None:
        result = run_cli(["help", "close"], cli_dir)
        assert "Available commands:" in result.stdout
        assert "add <name> <phone>" in result.stdout
        assert "add-note <title>" in result.stdout
        assert "close | exit" in result.stdout

    def test_invalid_command(self, cli_dir: Path) -> None:
        result = run_cli(["foobar", "close"], cli_dir)
        assert "Invalid command." in result.stdout


# ==================== C. Contact CRUD ====================


class TestContactCRUD:
    def test_add_contact(self, cli_dir: Path) -> None:
        result = run_cli(["add Alice 1234567890", "close"], cli_dir)
        assert "Contact added." in result.stdout

    def test_add_contact_missing_args(self, cli_dir: Path) -> None:
        result = run_cli(["add", "close"], cli_dir)
        assert "Enter the argument for the command." in result.stdout

    def test_add_contact_invalid_phone(self, cli_dir: Path) -> None:
        result = run_cli(["add Alice 123", "close"], cli_dir)
        assert "Phone number must contain exactly 10 digits" in result.stdout

    def test_add_contact_existing_adds_phone(self, cli_dir: Path) -> None:
        result = run_cli(
            ["add Alice 1234567890", "add Alice 0987654321", "close"],
            cli_dir,
        )
        assert "Contact added." in result.stdout
        assert "Contact updated." in result.stdout

    def test_phone_lookup(self, cli_dir: Path) -> None:
        result = run_cli(["add Alice 1234567890", "phone Alice", "close"], cli_dir)
        assert "1234567890" in result.stdout

    def test_phone_not_found(self, cli_dir: Path) -> None:
        result = run_cli(["phone Ghost", "close"], cli_dir)
        assert "Contact not found." in result.stdout

    def test_show_all_empty(self, cli_dir: Path) -> None:
        result = run_cli(["all", "close"], cli_dir)
        assert "No contacts saved." in result.stdout

    def test_show_all_with_contacts(self, cli_dir: Path) -> None:
        result = run_cli(["add Alice 1234567890", "all", "close"], cli_dir)
        assert "Alice" in result.stdout
        assert "1234567890" in result.stdout

    def test_change_contact(self, cli_dir: Path) -> None:
        result = run_cli(
            [
                "add Alice 1234567890",
                "change Alice 1234567890 0987654321",
                "phone Alice",
                "close",
            ],
            cli_dir,
        )
        assert "Contact updated." in result.stdout
        assert "0987654321" in result.stdout

    def test_change_contact_not_found(self, cli_dir: Path) -> None:
        result = run_cli(["change Ghost 1234567890 0987654321", "close"], cli_dir)
        assert "Contact not found." in result.stdout

    def test_delete_contact(self, cli_dir: Path) -> None:
        result = run_cli(
            ["add Alice 1234567890", "delete-contact Alice", "phone Alice", "close"],
            cli_dir,
        )
        assert "Contact deleted." in result.stdout
        assert "Contact not found." in result.stdout

    def test_delete_contact_not_found(self, cli_dir: Path) -> None:
        result = run_cli(["delete-contact Ghost", "close"], cli_dir)
        assert "Contact not found." in result.stdout


# ==================== D. Contact Extended Fields ====================


class TestContactExtendedFields:
    def test_add_birthday(self, cli_dir: Path) -> None:
        result = run_cli(
            ["add Alice 1234567890", "add-birthday Alice 15.06.1990", "close"],
            cli_dir,
        )
        assert "Birthday added." in result.stdout

    def test_add_birthday_invalid_format(self, cli_dir: Path) -> None:
        result = run_cli(
            ["add Alice 1234567890", "add-birthday Alice 1990-06-15", "close"],
            cli_dir,
        )
        assert "Birthday must be in DD.MM.YYYY format" in result.stdout

    def test_show_birthday(self, cli_dir: Path) -> None:
        result = run_cli(
            [
                "add Alice 1234567890",
                "add-birthday Alice 15.06.1990",
                "show-birthday Alice",
                "close",
            ],
            cli_dir,
        )
        assert "15.06.1990" in result.stdout

    def test_show_birthday_not_set(self, cli_dir: Path) -> None:
        result = run_cli(
            ["add Alice 1234567890", "show-birthday Alice", "close"],
            cli_dir,
        )
        assert "Birthday not set." in result.stdout

    def test_birthdays_no_upcoming(self, cli_dir: Path) -> None:
        result = run_cli(["birthdays", "close"], cli_dir)
        assert "No upcoming birthdays." in result.stdout

    def test_add_email(self, cli_dir: Path) -> None:
        result = run_cli(
            ["add Alice 1234567890", "add-email Alice alice@example.com", "close"],
            cli_dir,
        )
        assert "Email added." in result.stdout

    def test_add_email_invalid(self, cli_dir: Path) -> None:
        result = run_cli(
            ["add Alice 1234567890", "add-email Alice not-an-email", "close"],
            cli_dir,
        )
        assert "Invalid email address" in result.stdout

    def test_add_address(self, cli_dir: Path) -> None:
        result = run_cli(
            [
                "add Alice 1234567890",
                "add-address Alice 123 Main St Kyiv",
                "all",
                "close",
            ],
            cli_dir,
        )
        assert "Address added." in result.stdout
        assert "123 Main St Kyiv" in result.stdout


# ==================== E. Search ====================


class TestSearch:
    def test_search_by_name(self, cli_dir: Path) -> None:
        result = run_cli(["add Alice 1234567890", "search Alice", "close"], cli_dir)
        assert "Alice" in result.stdout
        assert "1234567890" in result.stdout

    def test_search_by_phone(self, cli_dir: Path) -> None:
        result = run_cli(["add Alice 1234567890", "search 1234567890", "close"], cli_dir)
        assert "Alice" in result.stdout

    def test_search_no_match(self, cli_dir: Path) -> None:
        result = run_cli(["add Alice 1234567890", "search ZZZ", "close"], cli_dir)
        assert "No contacts found." in result.stdout


# ==================== F. Notes CRUD ====================


class TestNotesCRUD:
    def test_add_note(self, cli_dir: Path) -> None:
        result = run_cli(["add-note Shopping", "Buy milk", "close"], cli_dir)
        assert "Note added." in result.stdout

    def test_add_note_missing_title(self, cli_dir: Path) -> None:
        result = run_cli(["add-note", "close"], cli_dir)
        assert "Enter the argument for the command." in result.stdout

    def test_all_notes_empty(self, cli_dir: Path) -> None:
        result = run_cli(["all-notes", "close"], cli_dir)
        assert "No notes saved." in result.stdout

    def test_all_notes_with_data(self, cli_dir: Path) -> None:
        result = run_cli(
            ["add-note Shopping", "Buy milk", "all-notes", "close"],
            cli_dir,
        )
        assert "Shopping" in result.stdout
        assert "Buy milk" in result.stdout

    def test_delete_note(self, cli_dir: Path) -> None:
        # Session 1: add note and get its ID
        r1 = run_cli(["add-note Shopping", "Buy milk", "all-notes", "close"], cli_dir)
        note_id = extract_note_id(r1.stdout)

        # Session 2: delete and verify
        r2 = run_cli([f"delete-note {note_id}", "all-notes", "close"], cli_dir)
        assert "Note deleted." in r2.stdout
        assert "No notes saved." in r2.stdout

    def test_delete_note_not_found(self, cli_dir: Path) -> None:
        result = run_cli(["delete-note nonexistent", "close"], cli_dir)
        assert "Note not found." in result.stdout

    def test_edit_note(self, cli_dir: Path) -> None:
        # Session 1: add note and get its ID
        r1 = run_cli(["add-note Shopping", "Buy milk", "all-notes", "close"], cli_dir)
        note_id = extract_note_id(r1.stdout)

        # Session 2: edit and verify
        r2 = run_cli(
            [f"edit-note {note_id}", "Buy eggs instead", "all-notes", "close"],
            cli_dir,
        )
        assert "Note updated." in r2.stdout
        assert "Buy eggs instead" in r2.stdout


# ==================== G. Notes Tags & Search ====================


class TestNotesTagsAndSearch:
    def test_add_tag(self, cli_dir: Path) -> None:
        # Session 1: add note
        r1 = run_cli(["add-note Shopping", "Buy milk", "all-notes", "close"], cli_dir)
        note_id = extract_note_id(r1.stdout)

        # Session 2: add tag
        r2 = run_cli([f"add-tag {note_id} groceries", "close"], cli_dir)
        assert "Tag added." in r2.stdout

    def test_add_tag_not_found(self, cli_dir: Path) -> None:
        result = run_cli(["add-tag nonexistent groceries", "close"], cli_dir)
        assert "Note not found." in result.stdout

    def test_find_note(self, cli_dir: Path) -> None:
        # Session 1: add note
        run_cli(["add-note Shopping", "Buy milk", "close"], cli_dir)

        # Session 2: search
        r2 = run_cli(["find-note Shopping", "close"], cli_dir)
        assert "Shopping" in r2.stdout
        assert "Buy milk" in r2.stdout

    def test_find_note_no_match(self, cli_dir: Path) -> None:
        result = run_cli(["find-note NonExistent", "close"], cli_dir)
        assert "No notes found." in result.stdout

    def test_find_by_tag(self, cli_dir: Path) -> None:
        # Session 1: add note and get ID
        r1 = run_cli(["add-note Shopping", "Buy milk", "all-notes", "close"], cli_dir)
        note_id = extract_note_id(r1.stdout)

        # Session 2: tag the note
        run_cli([f"add-tag {note_id} groceries", "close"], cli_dir)

        # Session 3: search by tag
        r3 = run_cli(["find-by-tag groceries", "close"], cli_dir)
        assert "Shopping" in r3.stdout

    def test_find_by_tag_no_match(self, cli_dir: Path) -> None:
        result = run_cli(["find-by-tag nonexistent", "close"], cli_dir)
        assert "No notes found." in result.stdout


# ==================== H. Sort Notes ====================


class TestSortNotes:
    def test_sort_notes_empty(self, cli_dir: Path) -> None:
        result = run_cli(["sort-notes", "close"], cli_dir)
        assert "No notes saved." in result.stdout

    def test_sort_notes_by_tag_alias(self, cli_dir: Path) -> None:
        result = run_cli(["sort-notes-by-tag", "close"], cli_dir)
        assert "No notes saved." in result.stdout

    def test_sort_notes_with_tagged_data(self, cli_dir: Path) -> None:
        # Session 1: add two notes, get IDs
        r1 = run_cli(
            [
                "add-note Zebra",
                "Z body",
                "add-note Alpha",
                "A body",
                "all-notes",
                "close",
            ],
            cli_dir,
        )
        ids = re.findall(r"ID:\s*([0-9a-f]+)", r1.stdout)
        assert len(ids) >= 2

        # Session 2: tag the first note
        run_cli([f"add-tag {ids[0]} ztag", "close"], cli_dir)

        # Session 3: sort -- tagged notes come first
        r3 = run_cli(["sort-notes-by-tag", "close"], cli_dir)
        assert "Zebra" in r3.stdout
        assert "Alpha" in r3.stdout


# ==================== I. Data Persistence ====================


class TestPersistence:
    def test_contact_persists_across_sessions(self, cli_dir: Path) -> None:
        run_cli(["add Alice 1234567890", "close"], cli_dir)
        r2 = run_cli(["phone Alice", "close"], cli_dir)
        assert "1234567890" in r2.stdout

    def test_note_persists_across_sessions(self, cli_dir: Path) -> None:
        run_cli(["add-note Shopping", "Buy milk", "close"], cli_dir)
        r2 = run_cli(["all-notes", "close"], cli_dir)
        assert "Shopping" in r2.stdout
        assert "Buy milk" in r2.stdout

    def test_data_file_created(self, cli_dir: Path) -> None:
        run_cli(["add Alice 1234567890", "close"], cli_dir)
        assert (cli_dir / "assistant_data.pkl").exists()


# ==================== J. Edge Cases ====================


class TestEdgeCases:
    def test_empty_input_ignored(self, cli_dir: Path) -> None:
        result = run_cli(["", "hello", "close"], cli_dir)
        assert "How can I help you?" in result.stdout

    def test_multiple_mutations_same_session(self, cli_dir: Path) -> None:
        result = run_cli(
            ["add Alice 1234567890", "add Bob 0987654321", "all", "close"],
            cli_dir,
        )
        assert "Alice" in result.stdout
        assert "Bob" in result.stdout

    def test_add_note_eof_during_body(self, cli_dir: Path) -> None:
        """EOF during note body input cancels note creation."""
        result = run_cli(["add-note Shopping"], cli_dir)
        assert "Note creation cancelled." in result.stdout
        assert "Good bye!" in result.stdout

    def test_edit_note_eof_during_body(self, cli_dir: Path) -> None:
        """EOF during note edit cancels the edit."""
        # Session 1: add note
        r1 = run_cli(["add-note Shopping", "Buy milk", "all-notes", "close"], cli_dir)
        note_id = extract_note_id(r1.stdout)

        # Session 2: edit with EOF (no body line after edit-note)
        r2 = run_cli([f"edit-note {note_id}"], cli_dir)
        assert "Note editing cancelled." in r2.stdout

    def test_case_insensitive_commands(self, cli_dir: Path) -> None:
        """Commands are case-insensitive (lowered by parse_input)."""
        result = run_cli(["HELLO", "Hello", "close"], cli_dir)
        assert result.stdout.count("How can I help you?") == 2

    def test_search_missing_query(self, cli_dir: Path) -> None:
        result = run_cli(["search", "close"], cli_dir)
        assert "Enter the argument for the command." in result.stdout

    def test_add_birthday_contact_not_found(self, cli_dir: Path) -> None:
        result = run_cli(["add-birthday Ghost 15.06.1990", "close"], cli_dir)
        assert "Contact not found." in result.stdout

    def test_add_email_contact_not_found(self, cli_dir: Path) -> None:
        result = run_cli(["add-email Ghost ghost@mail.com", "close"], cli_dir)
        assert "Contact not found." in result.stdout

    def test_add_address_contact_not_found(self, cli_dir: Path) -> None:
        result = run_cli(["add-address Ghost 123 Main St", "close"], cli_dir)
        assert "Contact not found." in result.stdout

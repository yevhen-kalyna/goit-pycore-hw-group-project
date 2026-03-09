# Copilot Instructions

## Project Overview

This is a "Personal Assistant" CLI application — an address book + notes manager built with Python 3.12. It uses stdlib only (no runtime dependencies). The project follows TDD with all tests pre-written.

## Architecture

```
personal_assistant/
├── models/          # Data classes (Field, Record, AddressBook, Note, NoteBook)
├── handlers/        # CLI command handlers (contact_handlers, note_handlers)
├── utils.py         # input_error decorator (already implemented)
├── storage.py       # Pickle serialization (save/load)
└── main.py          # CLI loop, command parsing, routing
```

## Key Patterns

### Field hierarchy

- `Field` is the base class with `.value` attribute
- `Name`, `Phone`, `Email`, `Address`, `Birthday` extend `Field`
- Each field validates in `__init__`, raising `ValueError` on invalid input
- `Birthday.value` is `datetime.date`, all others are `str`

### Collections

- `AddressBook(UserDict[str, Record])` — keyed by `record.name.value`
- `NoteBook(UserDict[str, Note])` — keyed by `note.id` (UUID string)

### Handlers

- All handlers are decorated with `@input_error` from `utils.py`
- Contact handlers signature: `(args: list[str], book: AddressBook) -> str`
- Note handlers signature: `(args: list[str], notebook: NoteBook) -> str`
- Exception-only handlers (`show_all`, `all_notes_handler`, `sort_notes_by_tag_handler`) take only the collection

### Error handling

- `input_error` decorator catches `ValueError`, `KeyError`, `IndexError`
- Handlers should raise these exceptions; the decorator converts them to user-friendly strings

## Code Style

- Python 3.12, type hints on all function signatures
- Line length: 120 characters max
- Linter: ruff (rules: E, F, I, N, W)
- Type checker: mypy (strict, disallow_untyped_defs)
- Formatter: ruff format
- Use `X | None` syntax, not `Optional[X]`
- Use `list[str]`, `dict[str, int]` syntax, not `typing.List`

## TDD Rules

- Tests are pre-written in `tests/` directory
- Implementation should make existing tests pass
- Do NOT modify test files
- Do NOT change method signatures (parameter types and return types)
- Replace `raise NotImplementedError` with real logic
- Run `pytest tests/<relevant_file>.py -v` to check progress

## Validation Rules

- Phone: exactly 10 digits
- Email: regex validation (user@domain.tld format)
- Birthday: DD.MM.YYYY format, stored as `datetime.date`
- Address: free text, no specific validation

## Storage

- Uses pickle serialization
- `save_data(book, notebook, filename)` saves both collections
- `load_data(filename)` returns `tuple[AddressBook, NoteBook]`
- Returns empty instances if file doesn't exist

## Git Workflow

- Branch naming: `feature/<scope>` (e.g., `feature/fields-and-record`)
- Target branch for PRs: `develop` (never `main` directly)
- Squash merge into develop
- CI must pass: ruff check + ruff format --check + mypy + pytest

## Project Board (Kanban)

Project board: https://github.com/users/yevhen-kalyna/projects/5

### Status columns

- **Backlog** — depends on other tasks, not yet actionable
- **Todo** — ready to be picked up
- **In Progress** — someone is actively working on it
- **In Review** — PR created, awaiting code review
- **Done** — merged and closed

### Custom fields

- **Priority**: Critical / High / Medium / Low
- **Size**: XS / S / M / L / XL (relative effort)

### Workflow

1. Pick a task from **Todo** → move to **In Progress**
2. Create `feature/<scope>` branch from `develop`
3. Implement code, make tests pass
4. Create Draft PR, reference issues with `Closes #N`
5. Move task to **In Review**
6. After merge → task auto-moves to **Done**

### WIP limit

Max 1-2 tasks in "In Progress" per person at a time.

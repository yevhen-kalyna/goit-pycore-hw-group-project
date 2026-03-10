# AGENTS.md

## Project Overview

Personal Assistant CLI — an address book + notes manager. Python 3.12, stdlib only (no runtime dependencies). The project follows TDD: all tests are pre-written, implementation replaces `NotImplementedError` stubs.

## Architecture

```
personal_assistant/
├── models/
│   ├── fields.py          # Field, Name, Phone, Email, Address, Birthday
│   ├── record.py          # Record (contact with CRUD for fields)
│   ├── address_book.py    # AddressBook(UserDict[str, Record])
│   ├── note.py            # Note (text + tags, UUID id)
│   └── note_book.py       # NoteBook(UserDict[str, Note])
├── handlers/
│   ├── contact_handlers.py  # Contact command handlers
│   └── note_handlers.py     # Note command handlers
├── utils.py               # @input_error decorator
├── storage.py             # Serialization save/load
└── main.py                # CLI loop, command parsing
```

## TDD Rules

- Tests live in `tests/` — one `test_*.py` per module
- Do NOT modify test files
- Do NOT change method signatures (parameter types, return types)
- Replace `raise NotImplementedError` with real logic
- `tests/conftest.py` auto-xfails tests that hit `NotImplementedError` — CI stays green for unimplemented stubs
- Run `pytest tests/<relevant_file>.py -v` to check progress

## Code Style

- Python 3.12, type hints on all function signatures
- Line length: 120 characters max
- Linter/formatter: ruff (rules: E, F, I, N, W)
- Type checker: mypy strict (`disallow_untyped_defs = true`)
- Use `X | None`, not `Optional[X]`
- Use `list[str]`, `dict[str, int]`, not `typing.List`, `typing.Dict`

## Key Patterns

### Field hierarchy

- `Field` is the base class with `.value` attribute
- `Name`, `Phone`, `Email`, `Address`, `Birthday` extend `Field`
- Each field validates in `__init__`, raising `ValueError` on invalid input
- `Birthday.value` is `datetime.date`, all others are `str`

### Validation rules

- Phone: exactly 10 digits
- Email: regex `user@domain.tld` format
- Birthday: `DD.MM.YYYY` format, stored as `datetime.date`
- Address: free text, no validation

### Collections

- `AddressBook(UserDict[str, Record])` — keyed by `record.name.value`
- `NoteBook(UserDict[str, Note])` — keyed by `note.id` (UUID string)

### Handlers

- All handlers decorated with `@input_error` from `utils.py`
- Contact handlers: `(args: list[str], book: AddressBook) -> str`
- Note handlers: `(args: list[str], notebook: NoteBook) -> str`
- Some handlers take only the collection (no `args`): `show_all`, `all_notes_handler`, `sort_notes_by_tag_handler`
- `@input_error` catches `ValueError`, `KeyError`, `IndexError` and returns user-friendly strings

### Storage

- `save_data(book, notebook, filename)` saves both collections
- `load_data(filename)` returns `tuple[AddressBook, NoteBook]`
- Returns empty instances if file doesn't exist

## Quality Commands

```bash
make lint         # ruff check + format check
make fix          # auto-fix lint + format
make type-check   # mypy strict
make test         # pytest
make check        # fix + type-check + test (run before committing)
```

## Git Workflow

- Branch naming: `feature/<scope>` or `fix/<scope>`
- PR target: `develop` (never `main` directly)
- Squash merge into develop
- Reference issues in PRs with `Closes #N`

## CI Pipeline

1. **Lint & Type Check** — ruff check, ruff format --check, mypy
2. **Tests** (7 parallel matrix jobs, one per module) — runs after lint passes
3. **Test Summary** (PR only) — posts per-module results table as PR comment

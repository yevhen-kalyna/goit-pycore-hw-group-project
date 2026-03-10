# Персональний помічник — План проєкту (v2)

## Структура проєкту

```
goit-pycore-hw-group-project/
├── personal_assistant/
│   ├── __init__.py
│   ├── main.py              # CLI-цикл, парсинг, маршрутизація команд
│   ├── models/
│   │   ├── __init__.py
│   │   ├── fields.py        # Field, Name, Phone, Email, Address, Birthday
│   │   ├── record.py        # Record (контакт)
│   │   ├── address_book.py  # AddressBook (UserDict)
│   │   ├── note.py          # Note (нотатка з тегами)
│   │   └── note_book.py     # NoteBook (UserDict)
│   ├── storage.py            # Серіалізація pickle (save/load)
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── contact_handlers.py  # Обробники команд контактів
│   │   └── note_handlers.py     # Обробники команд нотаток
│   └── utils.py              # Декоратор input_error, допоміжне
├── tests/
│   ├── __init__.py
│   ├── conftest.py         # Auto-xfail хук для NotImplementedError
│   ├── test_fields.py
│   ├── test_record.py
│   ├── test_address_book.py
│   ├── test_note.py
│   ├── test_note_book.py
│   ├── test_storage.py
│   └── test_handlers.py
├── pyproject.toml             # Пакетування + конфіг ruff/mypy/pytest
├── README.md
├── .gitignore
└── .github/
    └── workflows/
        └── ci.yml             # GitHub Actions: ruff + mypy + pytest
```


---

## CI Pipeline (GitHub Actions)

Файл `.github/workflows/ci.yml` запускається на кожен push та PR у `develop` і `main`.

### Два jobs:

**Job 1: Lint & Type Check**
```
Ruff check → Ruff format --check → mypy
```

**Job 2: Tests** (запускається після lint)
```
Tests: fields (27) → Tests: record (29) → Tests: note (11) →
Tests: note_book (19) → Tests: address_book (22) → Tests: handlers (39) →
Tests: storage (15)
```

Кожен модуль — окремий collapsible крок у GitHub Actions UI. Усі кроки виконуються навіть якщо попередній впав (`if: always()`).

### Auto-xfail

`tests/conftest.py` містить pytest-хук, який автоматично конвертує `NotImplementedError` (заглушки) у `xfail`. CI залишається зеленим, доки реалізований код працює коректно.

### Конфігурація у `pyproject.toml`:

```toml
[tool.ruff]
line-length = 120
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W"]

[tool.mypy]
python_version = "3.12"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
```

**Правило**: PR не мержиться, поки CI не зелений.


---

## TDD-підхід

### Як це працює в нашому проєкті:

1. **Lead (день 1)** — пише заглушки інтерфейсів і тести для них
2. **Команда (дні 2-5)** — імплементує код так, щоб тести проходили
3. **CI** — автоматично перевіряє кожен PR

### Приклад TDD-циклу:

Lead створює `tests/test_fields.py`:
```python
def test_phone_valid():
    phone = Phone("1234567890")
    assert phone.value == "1234567890"

def test_phone_invalid_short():
    with pytest.raises(ValueError):
        Phone("12345")

def test_email_valid():
    email = Email("user@example.com")
    assert email.value == "user@example.com"

def test_email_invalid():
    with pytest.raises(ValueError):
        Email("not-an-email")
```

Lead створює заглушку `models/fields.py`:
```python
class Email(Field):
    """Email з валідацією. TODO: реалізувати."""
    def __init__(self, value: str) -> None:
        raise NotImplementedError
```

Учасник 2 бере задачу → імплементує → тести зеленіють → PR.


---

## Розподіл ролей (v2)

### Lead (Ти) — Архітектура, CI, тести, рев'ю
**Зона:** Каркас проєкту, CI, тестові файли, PR review, документація

Задачі:
- Ініціалізація проєкту (структура, pyproject.toml, .gitignore)
- CI: GitHub Actions (ruff + mypy + pytest)
- Написати тести для ВСІХ модулів (TDD — тести ДО імплементації)
- Написати заглушки (інтерфейси) для всіх класів
- Branch protection rules на `develop` і `main`
- PR review для всіх merge
- README.md
- Фінальне пакетування та перевірка `pip install`

### Учасник 2 — Поля + Record
**Зона:** `models/fields.py`, `models/record.py`
**Тести для проходження:** `test_fields.py`, `test_record.py`

Задачі:
- Імплементація Field, Name, Phone, Email, Address, Birthday
- Валідація Email (regex), Phone (10 цифр), Birthday (DD.MM.YYYY)
- Клас Record — CRUD для всіх полів контакту
- Довести всі тести до зеленого стану

### Учасник 3 — AddressBook + CLI + Storage
**Зона:** `models/address_book.py`, `main.py`, `storage.py`, `handlers/contact_handlers.py`
**Тести для проходження:** `test_address_book.py`, `test_storage.py`, `test_handlers.py` (контакти)

Задачі:
- AddressBook(UserDict) — add_record, find, delete, search, get_upcoming_birthdays(days)
- Пошук контактів за будь-яким полем (часткове співпадіння)
- Обробники команд контактів + декоратор input_error
- main.py — CLI-цикл, парсинг команд, маршрутизація
- storage.py — pickle save/load для AddressBook та NoteBook
- Команда help (список усіх команд)

### Учасник 4 — Нотатки + теги
**Зона:** `models/note.py`, `models/note_book.py`, `handlers/note_handlers.py`
**Тести для проходження:** `test_note.py`, `test_note_book.py`, `test_handlers.py` (нотатки)

Задачі:
- Note — title, body, tags: list[str], created_at, id
- NoteBook(UserDict) — CRUD нотаток
- Пошук за текстом і за тегами, сортування за тегами
- Обробники команд нотаток

### Учасник 5 (якщо є) — UX + додаткові тести + демо
**Зона:** Покращення CLI, edge-кейси, підготовка до демо

Задачі:
- Кольоровий вивід (colorama)
- Підказки при неправильній команді
- Розширені тести: edge-кейси, інтеграційні тести
- Підготовка тестових даних і сценарію для демо

> Якщо 4 особи — задачі У5 розділити: UX → У3, додаткові тести → всі.


---

## Таймлайн (v2, з TDD)

| День          | Lead (Ти)                                                         | Учасник 2                  | Учасник 3                    | Учасник 4                  |
| ------------- | ----------------------------------------------------------------- | -------------------------- | ---------------------------- | -------------------------- |
| **1**         | Init проєкту, CI, pyproject.toml, заглушки всіх класів, ВСІ тести | —                          | —                            | —                          |
| **1** (вечір) | PR review                                                         | Fork → гілка, вивчає тести | Fork → гілка, вивчає тести   | Fork → гілка, вивчає тести |
| **2-3**       | PR review, допомога                                               | fields.py, record.py       | address_book.py, storage.py  | note.py, note_book.py      |
| **3-4**       | PR review, merge, фікси CI                                        | Фікси по рев'ю             | contact_handlers.py, main.py | note_handlers.py           |
| **4-5**       | Merge всіх гілок у develop                                        | Допомога з інтеграцією     | Допомога з інтеграцією       | Допомога з інтеграцією     |
| **5-6**       | README.md, pip install тест                                       | Баг-фікси, edge-кейси      | Баг-фікси, help команда      | Баг-фікси, UX              |
| **7**         | Фінальний merge main, тег v1.0                                    | Демо-підготовка            | Демо-підготовка              | Демо-підготовка            |


---

## GitHub Issues (v2)

### Milestone 0: Інфраструктура (День 1) — Lead

**Issue #1** — Ініціалізація проєкту
- Labels: `setup`, `priority: critical`
- Assignee: Lead
- Опис: Структура папок, __init__.py, .gitignore, гілка develop, branch protection

**Issue #2** — pyproject.toml: пакетування + інструменти
- Labels: `setup`, `priority: critical`
- Assignee: Lead
- Опис: entry_points (консольна команда), залежності, конфіг ruff/mypy/pytest

**Issue #3** — CI: GitHub Actions pipeline
- Labels: `ci`, `priority: critical`
- Assignee: Lead
- Опис: Workflow ci.yml — ruff check → mypy → pytest. Запуск на push/PR до develop і main

**Issue #4** — Заглушки інтерфейсів усіх класів
- Labels: `setup`, `tdd`
- Assignee: Lead
- Опис: Створити всі файли моделей із заглушками (raise NotImplementedError), визначити сигнатури методів, типізацію

**Issue #5** — Тести: fields + record
- Labels: `testing`, `tdd`
- Assignee: Lead
- Опис: test_fields.py (валідація Phone, Email, Birthday — позитивні та негативні кейси), test_record.py (CRUD полів)

**Issue #6** — Тести: address_book + storage
- Labels: `testing`, `tdd`
- Assignee: Lead
- Опис: test_address_book.py (add, find, delete, search, birthdays), test_storage.py (save/load цикл)

**Issue #7** — Тести: note + note_book
- Labels: `testing`, `tdd`
- Assignee: Lead
- Опис: test_note.py (створення, теги), test_note_book.py (CRUD, пошук за тегами, сортування)

**Issue #8** — Тести: handlers
- Labels: `testing`, `tdd`
- Assignee: Lead
- Опис: test_handlers.py — тести обробників команд (контакти + нотатки), перевірка input_error

### Milestone 1: Моделі (Дні 2-3)

**Issue #9** — Реалізація полів: Field, Name, Phone, Birthday
- Labels: `feature`, `models`
- Assignee: Учасник 2
- Тести: `test_fields.py` (Phone, Birthday секції)
- Опис: Перенести з task1.py, адаптувати під нову структуру

**Issue #10** — Нове поле Email з валідацією
- Labels: `feature`, `models`
- Assignee: Учасник 2
- Тести: `test_fields.py` (Email секція)
- Опис: Regex валідація, формат user@domain.tld

**Issue #11** — Нове поле Address
- Labels: `feature`, `models`
- Assignee: Учасник 2
- Тести: `test_fields.py` (Address секція)
- Опис: Текстове поле, без специфічної валідації

**Issue #12** — Клас Record з підтримкою всіх полів
- Labels: `feature`, `models`
- Assignee: Учасник 2
- Тести: `test_record.py`
- Опис: add/remove/edit/find для Phone, Email; set для Address, Birthday

**Issue #13** — AddressBook: CRUD + пошук
- Labels: `feature`, `core`
- Assignee: Учасник 3
- Тести: `test_address_book.py`
- Опис: add_record, find, delete, search (часткове співпадіння по будь-якому полю), get_upcoming_birthdays(days)

**Issue #14** — Storage: серіалізація pickle
- Labels: `feature`, `core`
- Assignee: Учасник 3
- Тести: `test_storage.py`
- Опис: save_data / load_data для AddressBook + NoteBook, шлях у домашній папці користувача

**Issue #15** — Note з тегами
- Labels: `feature`, `models`, `bonus`
- Assignee: Учасник 4
- Тести: `test_note.py`
- Опис: title, body, tags: list[str], created_at (auto), id (auto-increment або uuid)

**Issue #16** — NoteBook: CRUD + пошук + сортування за тегами
- Labels: `feature`, `core`, `bonus`
- Assignee: Учасник 4
- Тести: `test_note_book.py`
- Опис: add, find_by_text, find_by_tag, edit, delete, sort_by_tags

### Milestone 2: Handlers + CLI (Дні 3-4)

**Issue #17** — Обробники команд контактів
- Labels: `feature`, `handlers`
- Assignee: Учасник 3
- Тести: `test_handlers.py` (contact секція)
- Опис: add, change, phone, all, search, delete, add-birthday, show-birthday, birthdays, add-email, add-address. Декоратор input_error

**Issue #18** — Обробники команд нотаток
- Labels: `feature`, `handlers`
- Assignee: Учасник 4
- Тести: `test_handlers.py` (notes секція)
- Опис: add-note, find-note, edit-note, delete-note, all-notes, add-tag, find-by-tag, sort-notes-by-tag

**Issue #19** — main.py: CLI-цикл
- Labels: `feature`, `core`
- Assignee: Учасник 3
- Опис: Парсинг введення, маршрутизація команд, hello/help/close/exit

### Milestone 3: Інтеграція та полірування (Дні 5-7)

**Issue #20** — Інтеграція всіх модулів
- Labels: `integration`, `priority: high`
- Assignee: Lead + всі
- Опис: Merge всіх feature-гілок у develop, вирішення конфліктів, перевірка що всі тести зелені

**Issue #21** — Команда help
- Labels: `enhancement`
- Assignee: Учасник 3
- Опис: Форматований вивід списку всіх команд з описом

**Issue #22** — README.md
- Labels: `docs`, `priority: high`
- Assignee: Lead
- Опис: Опис проєкту, встановлення (pip install), список команд, приклади

**Issue #23** — Фінальне тестування та баг-фікси
- Labels: `testing`, `priority: high`
- Assignee: Всі
- Опис: Ручне тестування всіх команд, edge-кейси, перевірка збереження даних після перезапуску

**Issue #24** — Підготовка до демо
- Labels: `demo`
- Assignee: Всі
- Опис: Тестові дані, сценарій демо, розподіл презентації


---

## Git-стратегія

```
main (стабільний реліз, tag v1.0)
 └── develop (інтеграційна гілка, branch protection)
      ├── feature/project-setup        (Lead — день 1)
      ├── feature/fields-and-record    (Учасник 2)
      ├── feature/address-book-cli     (Учасник 3)
      └── feature/notes                (Учасник 4)
```

**Branch protection на develop:**
- Require PR review (від Lead)
- Require CI to pass (ruff + mypy + pytest)
- No direct push

**Branch protection на main:**
- Require PR from develop only
- Require all checks to pass


---

## Список команд CLI

### Контакти
| Команда         | Аргументи                | Опис                                    |
| --------------- | ------------------------ | --------------------------------------- |
| `add`           | name phone               | Додати контакт або телефон              |
| `change`        | name old_phone new_phone | Змінити телефон                         |
| `phone`         | name                     | Показати телефони контакту              |
| `all`           | —                        | Показати всі контакти                   |
| `search`        | query                    | Пошук контактів за будь-яким полем      |
| `delete`        | name                     | Видалити контакт                        |
| `add-birthday`  | name DD.MM.YYYY          | Додати день народження                  |
| `show-birthday` | name                     | Показати день народження                |
| `birthdays`     | [days]                   | Дні народження за N днів (за замовч. 7) |
| `add-email`     | name email               | Додати email                            |
| `add-address`   | name address             | Додати адресу                           |

### Нотатки
| Команда             | Аргументи | Опис                                  |
| ------------------- | --------- | ------------------------------------- |
| `add-note`          | title     | Додати нотатку (текст вводиться далі) |
| `find-note`         | query     | Пошук нотаток за текстом              |
| `edit-note`         | id        | Редагувати нотатку                    |
| `delete-note`       | id        | Видалити нотатку                      |
| `all-notes`         | —         | Показати всі нотатки                  |
| `add-tag`           | id tag    | Додати тег до нотатки                 |
| `find-by-tag`       | tag       | Пошук нотаток за тегом                |
| `sort-notes-by-tag` | —         | Сортувати нотатки за тегами           |

### Загальні
| Команда          | Опис          |
| ---------------- | ------------- |
| `hello`          | Привітання    |
| `help`           | Список команд |
| `close` / `exit` | Вихід         |

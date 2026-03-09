# Персональний помічник

CLI-застосунок для керування контактами та нотатками (адресна книга + нотатки з тегами).

## Вимоги

- Python 3.12+

## Встановлення

1. Клонувати репозиторій:

```bash
git clone git@github.com:yevhen-kalyna/goit-pycore-hw-group-project.git
cd goit-pycore-hw-group-project
```

2. Створити та активувати віртуальне середовище:

```bash
python -m venv .venv
```

- Linux / macOS:

```bash
source .venv/bin/activate
```

- Windows:

```powershell
.venv\Scripts\activate
```

3. Встановити пакет у режимі розробки:

```bash
pip install -e ".[dev]"
```

4. Перевірити встановлення:

```bash
assistant
```

Команда `assistant` має запустити CLI-застосунок.

## Запуск

Після встановлення достатньо виконати:

```bash
assistant
```

Або запустити напряму через модуль:

```bash
python -m personal_assistant.main
```

## Розробка

### Лінтер

```bash
ruff check .
ruff format --check .
```

### Форматування

```bash
ruff format .
```

### Перевірка типів

```bash
mypy personal_assistant/
```

### Тести

```bash
pytest
pytest -v          # детальний вивід
pytest --tb=short  # скорочений traceback
```

### Запуск усіх перевірок

```bash
ruff check . && ruff format --check . && mypy personal_assistant/ && pytest
```

## Команди CLI

### Контакти

| Команда | Аргументи | Опис |
|---------|-----------|------|
| `add` | name phone | Додати контакт або телефон |
| `change` | name old_phone new_phone | Змінити телефон |
| `phone` | name | Показати телефони контакту |
| `all` | — | Показати всі контакти |
| `search` | query | Пошук контактів за будь-яким полем |
| `delete` | name | Видалити контакт |
| `add-birthday` | name DD.MM.YYYY | Додати день народження |
| `show-birthday` | name | Показати день народження |
| `birthdays` | [days] | Дні народження за N днів (за замовч. 7) |
| `add-email` | name email | Додати email |
| `add-address` | name address | Додати адресу |

### Нотатки

| Команда | Аргументи | Опис |
|---------|-----------|------|
| `add-note` | title | Додати нотатку (текст вводиться далі) |
| `find-note` | query | Пошук нотаток за текстом |
| `edit-note` | id | Редагувати нотатку |
| `delete-note` | id | Видалити нотатку |
| `all-notes` | — | Показати всі нотатки |
| `add-tag` | id tag | Додати тег до нотатки |
| `find-by-tag` | tag | Пошук нотаток за тегом |
| `sort-notes-by-tag` | — | Сортувати нотатки за тегами |

### Загальні

| Команда | Опис |
|---------|------|
| `hello` | Привітання |
| `help` | Список команд |
| `close` / `exit` | Вихід |

## Структура проєкту

```
personal_assistant/
├── __init__.py
├── main.py
├── storage.py
├── utils.py
├── models/
│   ├── __init__.py
│   ├── fields.py
│   ├── record.py
│   ├── address_book.py
│   ├── note.py
│   └── note_book.py
└── handlers/
    ├── __init__.py
    ├── contact_handlers.py
    └── note_handlers.py
```

## Ліцензія

MIT

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

Усі команди для розробки доступні через `make`:

| Команда | Опис |
|---------|------|
| `make check` | Запустити всі перевірки (fix + type-check + test) |
| `make lint` | Перевірка стилю коду (ruff check + format check) |
| `make fix` | Автоматичне виправлення стилю та форматування |
| `make type-check` | Перевірка типів (mypy) |
| `make test` | Запуск тестів (pytest) |

### Швидкий старт

```bash
# Запустити всі перевірки перед комітом
make check
```

### Додаткові опції pytest

```bash
pytest -v          # детальний вивід
pytest --tb=short  # скорочений traceback
```

### Auto-xfail для незреалізованих модулів

`tests/conftest.py` містить pytest-хук, який автоматично позначає тести як **xfail** (expected failure), якщо вони потрапляють на `NotImplementedError` у заглушках. Це означає:

- Реалізований код → тести показують `PASSED`
- Заглушки → тести показують `XFAIL` (жовті), а не `FAILED` (червоні)
- CI залишається зеленим, доки реалізований код працює коректно

## Робочий процес

### 📋 Project Board

Відстеження прогресу — на [Kanban-дошці проєкту](https://github.com/users/yevhen-kalyna/projects/5).

| Колонка | Опис |
|---------|------|
| **Backlog** | Задача залежить від інших — ще не можна починати |
| **Todo** | Готова до виконання — бери в роботу |
| **In Progress** | Активно працюєш над задачею |
| **In Review** | PR створений, чекає рев'ю |
| **Done** | Замержено ✅ |

> Детальніше про роботу з дошкою — див. [CONTRIBUTING.md](.github/CONTRIBUTING.md)

### Git-стратегія

Проєкт використовує наступну модель гілкування:

```
main (стабільний реліз)
 └── develop (інтеграційна гілка)
       ├── feature/fields-and-record
       ├── feature/address-book-cli
       └── feature/notes
```

- `main` — стабільний реліз, тільки через PR із `develop`
- `develop` — інтеграційна гілка, усі feature-гілки мержаться сюди
- `feature/<scope>` — робочі гілки для конкретних задач

### Як працювати з задачею

1. Переконатися, що `develop` актуальний:

```bash
git checkout develop
git pull origin develop
```

2. Створити feature-гілку:

```bash
git checkout -b feature/<scope>
```

Приклади: `feature/fields-and-record`, `feature/notes`, `feature/address-book-cli`

3. Написати код, щоб тести проходили:

```bash
pytest tests/test_fields.py -v
```

4. Перед комітом — запустити всі перевірки:

```bash
make check
```

5. Закомітити та запушити:

```bash
git add <files>
git commit -m "Implement Phone and Email validation"
git push origin feature/<scope>
```

6. Створити Pull Request у `develop` на GitHub

### Правила PR

- PR створюється в гілку `develop` (не в `main`)
- PR створюється як **Draft**, поки тести для feature не проходять (зелені)
- Коли тести зелені — натисніть **"Ready for review"** на GitHub
- Заголовок PR — короткий опис змін
- В описі PR вказати які Issues закриває (напр. `Closes #9, #10`)
- PR має пройти CI (lint: ruff check + ruff format --check + mypy → tests: 7 модулів окремо)
- PR потребує review від Lead
- Використовується **Squash merge** — один чистий коміт на feature
- Оновіть задачу на [дошці](https://github.com/users/yevhen-kalyna/projects/5): перетягніть в **In Review**

### Як запустити тести для своєї задачі

```bash
# Тести для полів
pytest tests/test_fields.py -v

# Тести для Record
pytest tests/test_record.py -v

# Тести для AddressBook
pytest tests/test_address_book.py -v

# Тести для нотаток
pytest tests/test_note.py tests/test_note_book.py -v

# Тести для storage
pytest tests/test_storage.py -v

# Тести для handlers
pytest tests/test_handlers.py -v

# Усі тести
pytest -v
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
goit-pycore-hw-group-project/
├── personal_assistant/
│   ├── __init__.py
│   ├── main.py
│   ├── storage.py
│   ├── utils.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── fields.py
│   │   ├── record.py
│   │   ├── address_book.py
│   │   ├── note.py
│   │   └── note_book.py
│   └── handlers/
│       ├── __init__.py
│       ├── contact_handlers.py
│       └── note_handlers.py
└── tests/
    ├── conftest.py          # Auto-xfail хук для NotImplementedError
    ├── test_fields.py
    ├── test_record.py
    ├── test_address_book.py
    ├── test_note.py
    ├── test_note_book.py
    ├── test_storage.py
    └── test_handlers.py
```

## Ліцензія

MIT

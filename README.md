# Персональний помічник

CLI-застосунок для керування контактами та нотатками — адресна книга з телефонами, email, адресами, днями народження + нотатки з тегами.

## Можливості

- Керування контактами: додавання, редагування, пошук, видалення
- Зберігання телефонів (з валідацією), email, адрес та днів народження
- Нагадування про дні народження на найближчі N днів (з урахуванням вихідних)
- Нотатки з тегами: створення, пошук, сортування за тегами
- Автоматичне збереження даних у файл
- Коректна обробка помилок введення

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

При запуску бот привітає вас:

```
Welcome to the assistant bot!
Type 'help' to see available commands.
Enter a command:
```

## Команди CLI

### Контакти

| Команда | Аргументи | Опис |
|---------|-----------|------|
| `add` | `<name> <phone>` | Додати контакт або телефон до існуючого |
| `change` | `<name> <old_phone> <new_phone>` | Змінити телефон контакту |
| `phone` | `<name>` | Показати телефони контакту |
| `all` | — | Показати всі контакти |
| `search` | `<query>` | Пошук контактів за ім'ям, телефоном або email |
| `delete-contact` | `<name>` | Видалити контакт |
| `add-birthday` | `<name> <DD.MM.YYYY>` | Додати день народження |
| `show-birthday` | `<name>` | Показати день народження контакту |
| `birthdays` | `[days]` | Дні народження за N днів (за замовч. 7) |
| `add-email` | `<name> <email>` | Додати email контакту |
| `add-address` | `<name> <address>` | Додати адресу контакту |

### Нотатки

| Команда | Аргументи | Опис |
|---------|-----------|------|
| `add-note` | `<title>` | Додати нотатку (текст вводиться далі) |
| `all-notes` | — | Показати всі нотатки |
| `find-note` | `<query>` | Пошук нотаток за текстом у заголовку або тілі |
| `edit-note` | `<note_id>` | Редагувати текст нотатки |
| `delete-note` | `<note_id>` | Видалити нотатку |
| `add-tag` | `<note_id> <tag>` | Додати тег до нотатки |
| `find-by-tag` | `<tag>` | Пошук нотаток за тегом |
| `sort-notes` | — | Сортувати нотатки за тегами |
| `sort-notes-by-tag` | — | Те саме, що `sort-notes` |

### Загальні

| Команда | Опис |
|---------|------|
| `hello` | Привітання |
| `help` | Список усіх доступних команд |
| `close` / `exit` | Зберегти дані та вийти |

## Приклади використання

### Робота з контактами

```
Enter a command: add John 0501234567
Contact added.

Enter a command: add John 0509876543
Contact updated.

Enter a command: phone John
0501234567; 0509876543

Enter a command: change John 0501234567 0507777777
Contact updated.

Enter a command: add-email John john@example.com
Email added.

Enter a command: add-address John Kyiv, Khreshchatyk 1
Address added.

Enter a command: add-birthday John 15.06.1990
Birthday added.

Enter a command: show-birthday John
15.06.1990

Enter a command: all
Name: John | Phones: 0507777777; 0509876543 | Birthday: 15.06.1990 | Email: john@example.com | Address: Kyiv, Khreshchatyk 1

Enter a command: search John
Name: John | Phones: 0507777777; 0509876543 | Birthday: 15.06.1990 | Email: john@example.com | Address: Kyiv, Khreshchatyk 1

Enter a command: birthdays 30
John: 15.06.1990

Enter a command: delete-contact John
Contact deleted.
```

### Робота з нотатками

```
Enter a command: add-note Список покупок
Enter note body: Молоко, хліб, яйця
Note added.

Enter a command: add-note Ідеї для проєкту
Enter note body: Написати CLI-бота для керування задачами
Note added.

Enter a command: all-notes
ID: a1b2c3d4e5f6...
[a1b2c3d4e5f6...] Список покупок: Молоко, хліб, яйця | tags: -
ID: f6e5d4c3b2a1...
[f6e5d4c3b2a1...] Ідеї для проєкту: Написати CLI-бота для керування задачами | tags: -

Enter a command: add-tag a1b2c3d4e5f6 shopping
Tag added.

Enter a command: add-tag a1b2c3d4e5f6 grocery
Tag added.

Enter a command: find-note покупок
[a1b2c3d4e5f6...] Список покупок: Молоко, хліб, яйця | tags: shopping, grocery

Enter a command: find-by-tag shopping
[a1b2c3d4e5f6...] Список покупок: Молоко, хліб, яйця | tags: shopping, grocery

Enter a command: edit-note a1b2c3d4e5f6
Enter new note body: Молоко, хліб, яйця, масло
Note updated.

Enter a command: sort-notes
[a1b2c3d4e5f6...] Список покупок: Молоко, хліб, яйця, масло | tags: grocery, shopping
[f6e5d4c3b2a1...] Ідеї для проєкту: Написати CLI-бота для керування задачами | tags: -

Enter a command: delete-note f6e5d4c3b2a1
Note deleted.

Enter a command: close
Good bye!
```

## Валідація даних

| Поле | Формат | Приклад |
|------|--------|---------|
| Телефон | Рівно 10 цифр | `0501234567` |
| Email | Стандартний формат email | `user@example.com` |
| День народження | `DD.MM.YYYY` | `31.12.1999` |
| Адреса | Довільний текст | `Kyiv, Khreshchatyk 1` |

При некоректному введенні бот повідомить про помилку:

```
Enter a command: add John 12345
Invalid phone number: must be 10 digits.

Enter a command: add-email John not-an-email
Invalid email format.

Enter a command: add-birthday John 2000-01-01
Invalid date format. Use DD.MM.YYYY
```

## Збереження даних

Дані зберігаються автоматично у файл `assistant_data.pkl` у поточній директорії:

- Після кожної успішної зміни (додавання, редагування, видалення)
- При виході з програми (`close`, `exit`, Ctrl+C)
- При отриманні сигналів завершення (SIGTERM, SIGHUP)

При наступному запуску дані завантажуються автоматично. Якщо файл пошкоджений або відсутній — створюється порожня адресна книга та порожній блокнот.

## Структура проєкту

```
goit-pycore-hw-group-project/
├── personal_assistant/
│   ├── __init__.py
│   ├── main.py               # Точка входу, CLI-цикл, диспетчер команд
│   ├── storage.py             # Серіалізація/десеріалізація даних
│   ├── utils.py               # Декоратор обробки помилок
│   ├── models/
│   │   ├── __init__.py
│   │   ├── fields.py          # Поля: Name, Phone, Email, Address, Birthday
│   │   ├── record.py          # Запис контакту (Record)
│   │   ├── address_book.py    # Адресна книга (AddressBook)
│   │   ├── note.py            # Нотатка (Note)
│   │   └── note_book.py       # Блокнот (NoteBook)
│   └── handlers/
│       ├── __init__.py
│       ├── contact_handlers.py  # Обробники команд контактів
│       └── note_handlers.py     # Обробники команд нотаток
└── tests/
    ├── conftest.py              # Auto-xfail хук для NotImplementedError
    ├── test_fields.py
    ├── test_record.py
    ├── test_address_book.py
    ├── test_e2e.py              # E2E-тести для CLI
    ├── test_note.py
    ├── test_note_book.py
    ├── test_storage.py
    └── test_handlers.py
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

### Auto-xfail для незреалізованих модулів

`tests/conftest.py` містить pytest-хук, який автоматично позначає тести як **xfail** (expected failure), якщо вони потрапляють на `NotImplementedError` у заглушках. Це означає:

- Реалізований код → тести показують `PASSED`
- Заглушки → тести показують `XFAIL` (жовті), а не `FAILED` (червоні)
- CI залишається зеленим, доки реалізований код працює коректно

## Робочий процес

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
- PR має пройти CI (lint + type-check + tests)
- Використовується **Squash merge** — один чистий коміт на feature

## Ліцензія

MIT

# Як зробити внесок

## Перед початком роботи

1. Клонувати репозиторій та встановити залежності (див. README.md)
2. Ознайомитися зі своєю задачею в GitHub Issues
3. Вивчити тести, які потрібно зробити зеленими (файли в `tests/`)

## TDD — тести вже написані

Цей проєкт використовує підхід Test-Driven Development:

- Усі тести вже написані Lead'ом
- Ваша задача — написати код, щоб тести проходили
- НЕ змінюйте тести без погодження з Lead'ом

Перевірте свої тести:

```bash
pytest tests/test_fields.py -v
```

Тести мають показувати `FAILED` (NotImplementedError) до вашої імплементації та `PASSED` після.

## Робочий процес

### 1. Оновити develop

```bash
git checkout develop
git pull origin develop
```

### 2. Створити feature-гілку

Формат: `feature/<scope>`

```bash
git checkout -b feature/fields-and-record
```

Не використовуйте пробіли, великі літери чи спецсимволи в назвах гілок.

### 3. Імплементувати код

- Замініть `raise NotImplementedError` на реальну логіку
- Зберігайте сигнатури методів (типи параметрів та повернення) без змін
- Запускайте тести після кожної зміни

### 4. Перевірити якість коду

Перед комітом запустіть усі перевірки:

```bash
ruff check .                  # лінтер
ruff format --check .         # перевірка форматування
mypy personal_assistant/      # перевірка типів
pytest                        # тести
```

Якщо `ruff format` скаржиться — виправте форматування:

```bash
ruff format .
```

### 5. Закомітити зміни

```bash
git add personal_assistant/models/fields.py personal_assistant/models/record.py
git commit -m "Implement Field, Name, Phone, Email, Address, Birthday"
```

Правила комітів:

- Комітьте тільки файли своєї задачі
- Повідомлення англійською, починається з дієслова: `feat`, `chore`, `fix`, `refactor` (дивіться [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/#summary) для прикладів)
- Не комітьте `.pkl` файли, `.venv`, `__pycache__`

### 6. Запушити та створити PR

```bash
git push origin feature/fields-and-record
```

Потім створіть Pull Request на GitHub:

- Base: `develop` (не `main`!)
- Заповніть шаблон PR
- Вкажіть які Issues закриває: `Closes #9, #10`

## Вимоги до коду

### Стиль

- Рядок до 120 символів
- Python 3.12+ синтаксис (напр. `str | None` замість `Optional[str]`)
- Type hints на всіх сигнатурах функцій
- Імена змінних та функцій — `snake_case`
- Імена класів — `PascalCase`

### Що НЕ робити

- Не змінюйте тести
- Не змінюйте `pyproject.toml`
- Не змінюйте `utils.py` (декоратор вже реалізований)
- Не додавайте нові залежності без погодження
- Не пушіть напряму в `develop` або `main`
- Не змінюйте сигнатури методів (типи параметрів та повернення)

## Якщо щось не працює

1. Перечитайте тест — він показує очікувану поведінку
2. Перевірте імпорти — усі шляхи абсолютні (`from personal_assistant.models.fields import ...`)
3. Запустіть конкретний тест з `-v` для деталей:
   ```bash
   pytest tests/test_fields.py::test_phone_valid_ten_digits -v
   ```
4. Зверніться до Lead'а через PR коментар або чат

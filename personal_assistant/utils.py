from collections.abc import Callable
from typing import Any


def input_error(func: Callable[..., str]) -> Callable[..., str]:
    """Декоратор для обробки помилок введення користувача."""

    def inner(*args: Any, **kwargs: Any) -> str:
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Enter the argument for the command."

    return inner

.PHONY: lint format type-check test check fix

## Run ruff linter and format check
lint:
	ruff check .
	ruff format --check .

## Auto-fix linting issues and format code
fix:
	ruff check --fix .
	ruff format .

## Run mypy type checking
type-check:
	mypy personal_assistant/

## Run pytest
test:
	pytest

## Run all checks (lint + type-check + test)
check: fix type-check test

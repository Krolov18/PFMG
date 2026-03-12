# PFMG – targets run via uv (lint, format, type-check, test)
UV ?= uv run
export PYTHONDONTWRITEBYTECODE := 1

.PHONY: install lint format format-check type test check clean help

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  install      Sync dependencies (uv sync --all-groups)"
	@echo "  lint        Run Ruff linter"
	@echo "  format      Run Ruff formatter"
	@echo "  format-check Run Ruff formatter in check-only mode"
	@echo "  type       Run ty type checker"
	@echo "  test       Run pytest with coverage"
	@echo "  check      Run lint + format-check + type + test"
	@echo "  clean      Remove __pycache__ dirs and .pyc files"

install:
	uv sync --all-groups

lint:
	$(UV) pylint pfmg
	$(UV) ruff check

format:
	$(UV) ruff format

format-check:
	$(UV) ruff format --check

type:
	$(UV) ty check

test:
	$(UV) pytest --cov=pfmg --cov-report=term-missing

check: lint format-check type test

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete 2>/dev/null || true
	find . -type f -name '*.pyo' -delete 2>/dev/null || true

.DEFAULT_GOAL := help

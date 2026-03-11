# PFMG – targets run via uv (lint, format, type-check, test)
UV ?= uv run

.PHONY: install lint format format-check type test check help

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

.DEFAULT_GOAL := help

# PFMG – targets run via uv (lint, format, type-check, test)
UV ?= uv run
export PYTHONDONTWRITEBYTECODE := 1

.PHONY: install lint format format-check type test check clean docs docs-preview docker-test docker-check help

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
	@echo "  docs       Build Antora site via Docker (doc/build/site)"
	@echo "  docs-preview  Build site and serve on http://localhost:8787 (Docker)"
	@echo "  docker-test  Run the test suite inside the Python Docker image"
	@echo "  docker-check Run lint + format-check + type + test inside Docker"
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

docs:
	docker compose run --rm docs

docs-preview:
	docker compose run --rm --service-ports docs-preview

docker-test:
	docker compose run --rm lib

docker-check:
	docker compose run --rm lib sh -c "uv sync --all-groups --frozen && uv run ruff check && uv run ruff format --check && uv run ty check && uv run pytest"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete 2>/dev/null || true
	find . -type f -name '*.pyo' -delete 2>/dev/null || true

.DEFAULT_GOAL := help

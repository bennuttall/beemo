PIP := pip
POETRY := poetry
HTML_DOCS := docs/_build/html

develop:
	$(PIP) install -U pip
	$(PIP) install "poetry>2"
	$(POETRY) install --all-extras --with dev
	$(POETRY) run beemo --install-completion

lint:
	$(POETRY) run isort . --check-only
	$(POETRY) run black . --check

format:
	$(POETRY) run isort .
	$(POETRY) run black .

build:
	rm -rf dist
	$(POETRY) build

release: build
	$(POETRY) publish

docs:
	$(POETRY) run sphinx-build -b html docs $(HTML_DOCS)

docs-serve: docs
	$(POETRY) run python -m http.server -d $(HTML_DOCS)

.PHONY: develop lint format build release docs docs-serve
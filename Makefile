PIP := pip
POETRY := poetry


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
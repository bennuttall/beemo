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
	$(POETRY) run twine upload dist/*

doc:
	$(POETRY) run sphinx-build -b html docs $(HTML_DOCS)

doc-serve: doc
	$(POETRY) run python -m http.server -d $(HTML_DOCS)

freeze-rtd-requirements:
	echo "." > rtd_requirements.txt
	$(POETRY) run pip freeze | grep -i sphinx >> rtd_requirements.txt

.PHONY: develop lint format build release doc doc-serve freeze-rtd-requirements
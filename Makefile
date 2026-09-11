PIP := pip
PYTHON := python
HTML_DOCS := docs/_build/html

develop:
	$(PIP) install -U pip
	$(PIP) install -e ".[logs]" --group dev
	beemo --install-completion

lint:
	isort . --check-only
	black . --check

format:
	isort .
	black .

build:
	rm -rf dist
	$(PYTHON) -m build

release: build
	twine upload dist/*

doc:
	sphinx-build -b html docs $(HTML_DOCS)

doc-serve: doc
	$(PYTHON) -m http.server -d $(HTML_DOCS)

freeze-rtd-requirements:
	echo "." > rtd_requirements.txt
	$(PIP) freeze | grep -iE "sphinx|autodoc" >> rtd_requirements.txt

.PHONY: develop lint format build release doc doc-serve freeze-rtd-requirements

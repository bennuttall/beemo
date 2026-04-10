develop:
	pip install -U pip
	pip install "poetry>2"
	poetry install --all-extras --with dev
	poetry run beemo --install-completion

lint:
	isort . --check-only
	black . --check

format:
	isort .
	black .

build:
	rm -rf dist
	poetry build

release: build
	twine upload dist/*
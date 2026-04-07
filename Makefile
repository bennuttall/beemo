develop:
	pip install "poetry>2"
	poetry install --all-extras --with dev
	beemo --install-completion

format:
	isort .
	black .

build:
	rm -rf dist
	poetry build

release: build
	twine upload dist/*
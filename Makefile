develop:
	pip install "poetry>2"
	poetry install --all-extras --with dev

serve:
	python -m http.server -d www &
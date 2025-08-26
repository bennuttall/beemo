develop:
	pip install "poetry>2"
	$(MAKE) -C beemo develop

serve:
	python -m http.server -d www &
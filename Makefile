develop:
	pip install "poetry>2"
	$(MAKE) -C blogbuild develop

serve:
	python -m http.server -d www &
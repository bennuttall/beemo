develop:
	$(MAKE) -C blogbuild develop

build:
	blog-build

serve:
	python -m http.server 8000 -d www
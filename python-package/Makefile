build:
	rm -rf advik/sections/
	poetry run python build.py ../resume.yaml advik/sections
	poetry build

install: build
	poetry install

publish: build install
	poetry publish

.PHONY: build install publish

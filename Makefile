VENV_NAME := .venv
PYTHON := $(VENV_NAME)/bin/python
VERSION := $(shell $(PYTHON) -c "import pytitle;print(pytitle.__version__)")

RM := rm -rf


clean:
	find . -name '*.pyc' -exec $(RM) {} +
	find . -name '*.pyo' -exec $(RM) {} +
	find . -name '*~' -exec $(RM)  {} +
	find . -name '__pycache__' -exec $(RM) {} +
	$(RM) build/ dist/ docs/build/ .tox/ .cache/ .pytest_cache/ *.egg-info coverage.xml .coverage

tag:
	@echo "Add tag: '$(VERSION)'"
	git tag v$(VERSION)

build:
	poetry build

publish:
	poetry publish

release:
	make clean
	make test
	make build
	make tag
	@echo "Released $(VERSION)"


full-release:
	make release
	make publish

install:
	poetry install

test:
	tox

summary:
	cloc pytitle/ tests/ docs/

docs: docs/source/*
	cd docs && make html
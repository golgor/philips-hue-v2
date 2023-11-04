.PHONY: all dev ruff lint check_style test clean

SHELL:=/bin/bash
RUN=poetry run
PYTHON=${RUN} python

all:
	@echo "make dev"
	@echo "    Create dev environment."
	@echo "make ruff"
	@echo "    Run 'ruff' to lint project."
	@echo "make mypy"
	@echo "    Run mypy type checking on project."
	@echo "make check_style"
	@echo "    Check code-style"
	@echo "make style"
	@echo "    Reformat the code to match the style"
	@echo "make check"
	@echo "    Check code-style, run linters, run tests"
	@echo "make coverage"
	@echo "    Run code coverage check."
	@echo "make test"
	@echo "    Run tests on project."
	@echo "make clean"
	@echo "    Remove python artifacts and virtualenv"

dev:
	poetry install --with dev

ruff:
	${RUN} ruff check .

lint: dev ruff
	${RUN} mypy .

check_style: dev
	${RUN} ruff format --check --diff .

style: dev
	${RUN} ruff format .

check: check_style lint test

test: dev
	${RUN} pytest .

clean:
	poetry env remove --all
	find -type d | grep __pycache__ | xargs rm -rf
	find -type d | grep .*_cache | xargs rm -rf
	rm -rf *.eggs *.egg-info dist build docs/_build .cache .mypy_cache coverage/* .pytest_cache/ .ruff_cache/

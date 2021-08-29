.PHONY: lint test check

lint:
	@isort .
	@black .

check:
	@black --check .

test:
	pip install -e .
	pytest tests --cov=giru --cov-report=term-missing:skip-covered -xv --maxfail=0
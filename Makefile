.PHONY: check test validate site

check: test validate

test:
	uv run pytest -q

validate:
	uv run python scripts/validate.py

site:
	uv run python scripts/build_site.py

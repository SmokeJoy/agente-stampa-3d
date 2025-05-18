.PHONY: hooks test
hooks:
	poetry run pre-commit run --all-files --show-diff-on-failure
test:
	poetry run pytest -q 

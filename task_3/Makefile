test:
	poetry install
	poetry run pytest

freeze:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

freeze_dev:
	poetry export -f requirements.txt --dev --output requirements.txt --without-hashes

update:
	poetry update

.PHONY: format

ALL: format run requirements.txt

requirements.txt: pyproject.toml
	poetry export -o requirements.txt

database.db:
	touch database.db

format:
	isort app
	ruff format app

run: database.db
	docker compose up --build -d
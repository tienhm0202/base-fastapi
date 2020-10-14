pyclean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

buildclean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf htmlcov/
	rm -rf .pytest_cache/

migrate:
	alembic upgrade head

downgrade:
	alembic downgrade -1

miggen:
	python cli.py $(name)

lint:
	flake8 zogapp/

test:
	pytest

run:
	uvicorn main:app

db:
	docker run -e POSTGRES_USER={{cookiecutter.postgres_user}} -e POSTGRES_PASSWORD={{cookiecutter.postgres_pass}} -e POSTGRES_DB={{cookiecutter.postgres_db}} -p 5432:5432 -d postgres

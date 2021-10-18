pyclean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

buildclean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm .coverage coverage.xml

migrate:
	env PYTHONPATH=. alembic upgrade head
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

downgrade:
	env PYTHONPATH=. alembic downgrade -1
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

miggen:
	python cli.py $(name)
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

lint:
	flake8 src/

test:
	pytest

check:
	flake8 src/
	bandit -r src/
	pytest tests/

run:
	sh entrypoint.sh

nginx_deploy:
	cp deployments/nginx/{{cookiecutter.project_slug}}.nginx.conf /etc/nginx/sites-available/{{cookiecutter.project_slug}}.nginx.conf
	nginx_ensite {{cookiecutter.project_slug}}.nginx.conf

module_first:
	cookiecutter https://github.com/tienhm0202/base-fastapi-modules.git -o src/modules/

module:
	cookiecutter base-fastapi-modules -o src/modules/

docker_build:
	docker build -t {{cookiecutter.docker_url}}/{{cookiecutter.docker_group}}/{{cookiecutter.docker_image}}:$(version) .
	docker image prune -f

docker_push:
	docker push {{cookiecutter.docker_url}}/{{cookiecutter.docker_group}}/{{cookiecutter.docker_image}}:$(version)

docker_run:
	docker rm -vf {{cookiecutter.project_slug}}
	make docker_build version=$(version)
	docker run --network=zog -d --name {{cookiecutter.project_slug}} -p 5000:80 -e POSTGRES_HOST=postgres {{cookiecutter.docker_url}}/{{cookiecutter.docker_group}}/{{cookiecutter.docker_image}}:$(version)

db:
	docker run --network=zog -d --name postgres -e POSTGRES_USER={{cookiecutter.postgres_user}} -e POSTGRES_PASSWORD={{cookiecutter.postgres_pass}} -e POSTGRES_DB={{cookiecutter.postgres_db}} -p 5432:5432 -d postgres

release:
	heroku container:push -a {{cookiecutter.docker_group}} web
	heroku container:release -a {{cookiecutter.docker_group}} web

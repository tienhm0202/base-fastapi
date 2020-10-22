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
	env PYTHONPATH=. alembic upgrade head

downgrade:
	env PYTHONPATH=. alembic downgrade -1

miggen:
	python cli.py $(name)

lint:
	flake8 zogapp/

test:
	pytest

run:
	uvicorn main:app

nginx_deploy:
	cp zogvn_users.nginx.conf /etc/nginx/sites-available/zogvn_users.nginx.conf
	nginx_ensite zogvn_users.nginx.conf

module:
	cookiecutter https://github.com/tienhm0202/base-fastapi-modules.git -o zogapp/modules/

docker-build:
    export DOCKER_IMAGE={{cookiecutter.docker_url}}/{{cookiecutter.docker_group}}/{{cookiecutter.docker_image}}:$(version)
	docker build -t ${DOCKER_IMAGE} .

docker-run:
    export DOCKER_IMAGE={{cookiecutter.docker_url}}/{{cookiecutter.docker_group}}/{{cookiecutter.docker_image}}:$(version)
	make docker-build version=$(version)
	docker run --network=zog -d --name zog-users -p 5000:5000 -e POSTGRES_HOST=postgres ${DOCKER_IMAGE}

db:
	docker run --network=zog -d --name postgres -e POSTGRES_USER={{cookiecutter.postgres_user}} -e POSTGRES_PASSWORD={{cookiecutter.postgres_pass}} -e POSTGRES_DB={{cookiecutter.postgres_db}} -p 5432:5432 -d postgres

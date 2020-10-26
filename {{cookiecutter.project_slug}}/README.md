# {{cookiecutter.project_name}}

[![pipeline status]({{cookiecutter.project_git_path}}/badges/master/pipeline.svg)]({{cookiecutter.project_git_path}}/commits/master) [![coverage report]({{cookiecutter.project_git_path}}/badges/master/coverage.svg)]({{cookiecutter.project_git_path}}/commits/master) [![python version](https://img.shields.io/badge/python-3.7-blue.svg)]({{cookiecutter.project_git_path}}/commits/master) [![document](https://img.shields.io/badge/document-OpenAPI-green.svg)]({{cookiecutter.project_git_path}}/commits/master)

**Version**: {{cookiecutter.project_version}}

{{cookiecutter.project_short_description}}

## To init private pypi (Gitlab)

```
$ poetry config repositories.zog https://gitlab.com/api/v4/projects/{{cookiecutter.gitlab_pypi_id}}/packages/pypi
$ poetry config http_basic.zog {{cookiecutter.gitlab_pypi_user}} {{cookiecutter.gitlab_pypi_token}}
$ export PIP_EXTRA_INDEX_URL=https://__token__:{{cookiecutter.gitlab_pypi_token}}@gitlab.com/api/v4/projects/{{cookiecutter.gitlab_pypi_id}}/packages/pypi/simple
```

## Usage

```bash
# To run lint
$ make lint

# To run test
$ make test

# To run app
$ make run

# Migrate alembic
$ make migrate

# Downgrade alembic
$ make downgrade

# Run local database (Docker required)
$ make db

# Generate new migrations
$ make miggen name="init_users_table"
```

For more detail, check Makefile

## Authors

- [Hoang Manh Tien](https://github.com/tienhm0202)

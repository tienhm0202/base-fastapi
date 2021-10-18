# {{cookiecutter.project_name}}

[![pipeline status]({{cookiecutter.project_git_path}}/badges/prod/pipeline.svg)]({{cookiecutter.project_git_path}}/-/commits/prod) [![coverage report]({{cookiecutter.project_git_path}}/badges/prod/coverage.svg)]({{cookiecutter.project_git_path}}/-/commits/prod) [![python version](https://img.shields.io/badge/python-3.7-blue.svg)]({{cookiecutter.project_git_path}}/-/commits/prod) [![document](https://img.shields.io/badge/document-OpenAPI-green.svg)]({{cookiecutter.project_git_path}}/-/commits/prod)

**Version**: {{cookiecutter.project_version}}

{{cookiecutter.project_short_description}}

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

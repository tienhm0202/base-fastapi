# {{cookiecutter.project_name}}

[![pipeline status]({{cookiecutter.project_git_path}}/badges/prod/pipeline.svg)]({{cookiecutter.project_git_path}}/-/commits/prod) [![coverage report]({{cookiecutter.project_git_path}}/badges/prod/coverage.svg)]({{cookiecutter.project_git_path}}/-/commits/prod) [![python version](https://img.shields.io/badge/python-3.7-blue.svg)]({{cookiecutter.project_git_path}}/-/commits/prod) [![document](https://img.shields.io/badge/document-OpenAPI-green.svg)]({{cookiecutter.project_git_path}}/-/commits/prod)

**Version**: {{cookiecutter.project_version}}

{{cookiecutter.project_short_description}}

## Usage

```bash
# To run lint
$ cli make lint

# To run test
$ cli make test

# Migrate alembic
$ cli db migrate

# Downgrade alembic
$ cli db downgrade

# Run local database (Docker required)
$ cli docker db

# Generate new migrations
$ cli db miggen "init_users_table"
```

For more detail, check

```bash
$ cli --help
```

## Authors

- [Hoang Manh Tien](https://github.com/tienhm0202)

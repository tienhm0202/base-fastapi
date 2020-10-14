# {{cookiecutter.project_name}}

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

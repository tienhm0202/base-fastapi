# FastAPI Backend template

Version FastAPI with Postgres for backend service only.

To use this template:

## 1\. Create new project in Gitlab

## 2\. Update your project CI buildpack:

Goto: Settings --> CI/CD --> Variables Add: BUILDPACK_URL: <https://github.com/tienhm0202/heroku-buildpack-python>

## 3\. Run cookiecutter

```bash
  $ cookiecutter https://github.com/tienhm0202/base-fastapi.git
```

Remember to change `project_git_path` to your Gitlab repo: such as <https://gitlab.com/tienhm0202/base-fastapi.git>

## 4\. New module

```bash
make module
```

When be asked `module_name`, remember to add singular, lower module name.

Eg: user, merchant ...

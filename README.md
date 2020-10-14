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

## 4\. Gitlab CI config

Test jobs may be disabled by setting environment variables:

```
- test: TEST_DISABLED
- code_quality: CODE_QUALITY_DISABLED
- license_management: LICENSE_MANAGEMENT_DISABLED
- performance: PERFORMANCE_DISABLED
- sast: SAST_DISABLED
- dependency_scanning: DEPENDENCY_SCANNING_DISABLED
- container_scanning: CONTAINER_SCANNING_DISABLED
- dast: DAST_DISABLED
- review: REVIEW_DISABLED
- stop_review: REVIEW_DISABLED
```

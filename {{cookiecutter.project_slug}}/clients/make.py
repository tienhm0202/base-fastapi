"""
To run script to clean or build for project
"""
import pathlib
import shutil

from typer import Typer
from rich import print

from clients.helpers import run_commands

app = Typer(name="make",
            help="To run make utils to build or clean project")


@app.command()
def pyclean(out: int = 1):
    """Remove all __pycache__ folders in project path"""
    to_delete = [p.absolute() for p in pathlib.Path('.').rglob('__pycache__')]

    print("__pycache__ will be removed")
    if out == 1:
        for path in to_delete:
            print(path)
    [shutil.rmtree(path) for path in to_delete]


@app.command()
def buildclean():
    """Remove all build folders in project path

    Including:
        build/
        dist/
        *.egg-info
        htmlcov/
        .pytest_cache/
        .coverage coverage.xml
    """
    commands = [
        "rm -rf build/",
        "rm -rf dist/",
        "rm -rf *.egg-info",
        "rm -rf htmlcov/",
        "rm -rf .pytest_cache/",
        "rm .coverage coverage.xml"
    ]
    run_commands(commands)


@app.command()
def lint():
    """Run project linter"""
    commands = ["flake8 src/"]
    run_commands(commands)


@app.command()
def test():
    """Run project test suite"""
    commands = ["pytest tests/"]
    run_commands(commands)


@app.command()
def check():
    """Run project lint, test and security check (bandit)"""
    commands = ["bandit -r src/"]
    lint()
    run_commands(commands)
    test()


@app.command()
def module_first():
    """Init module at first time or in case pulling new code"""
    commands = ["cookiecutter https://github.com/tienhm0202/base-fastapi-modules.git -o src/modules/"]  # noqa
    run_commands(commands)


@app.command()
def module():
    """Init module with existed code based"""
    commands = ["cookiecutter base-fastapi-modules -o src/modules/"]
    run_commands(commands)

from typer import Typer
from rich import print

from clients.helpers import run_commands
from clients.make import pyclean

app = Typer(name="docker",
            help="To run build and run docker image")


@app.command()
def build(tag_version: str = "1.0",
          tag_name: str = '{{cookiecutter.docker_url}}/{{cookiecutter.docker_group}}/{{cookiecutter.docker_image}}', 
          root: str = "."):
    """To build docker image for this project"""
    print("Building docker image ...")

    commands = [
        "docker build -t {tag_name}:{tag_version} {root}".format(
            tag_name=tag_name, tag_version=tag_version, root=root
        ),
        "docker image prune -f"
    ]
    pyclean(out=0)
    run_commands(commands)
    pyclean(out=1)


@app.command()
def run(tag_version: str = "1.0",
        env: str = "POSTGRES_HOST=postgres",
        tag_name: str = '{{cookiecutter.docker_url}}/{{cookiecutter.docker_group}}/{{cookiecutter.docker_image}}'):
    """To run docker image built for this project"""
    print("Running docker image ...")

    docker_name = '{{cookiecutter.project_slug}}'
    envs = " ".join(["-e " + e for e in env.split(",")])

    commands = [
        "docker run --network={{cookiecutter.docker_group}} --name {docker_name} {envs} -d {tag_name}:{tag_version}"
        .format(
            docker_name=docker_name, envs=envs,
            tag_version=tag_version, tag_name=tag_name
        )
    ]
    pyclean(out=0)
    run_commands(commands)
    pyclean(out=1)


@app.command()
def db():
    """Run docker image for database"""
    commands = ["docker run --network={{cookiecutter.docker_group}} -d --name postgres -e POSTGRES_USER={{cookiecutter.postgres_user}} -e POSTGRES_PASSWORD={{cookiecutter.postgres_pass}} -e POSTGRES_DB={{cookiecutter.postgres_db}} -p 5432:5432 -d postgres"]  # noqa
    run_commands(commands)

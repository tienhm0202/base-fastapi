import os
import glob
import re

from typer import Typer
from rich import print

from clients.helpers import run_commands
from clients.make import pyclean

app = Typer(name="db",
            help="Run migration tool")


@app.command()
def migrate():
    """Run DB migration upgrade"""
    commands = [
        "env PYTHONPATH=. alembic upgrade head"
    ]
    run_commands(commands)
    pyclean(out=0)


@app.command()
def downgrade():
    """Run DB migration downgrade"""
    commands = [
        "env PYTHONPATH=. alembic downgrade -1"
    ]
    run_commands(commands)
    pyclean(out=0)


@app.command()
def miggen(name: str):
    """Generate new migration"""
    list_of_files = glob.glob('migrations/versions/*')
    result = None
    if list_of_files:
        latest_file = max(list_of_files, key=os.path.getctime)
        pattern = r"([0-9]+)\_.*"
        result = re.search(pattern, latest_file)
    if not result:
        name = "00001_%s" % name
    else:
        prefix = str(int(result[1]) + 1).zfill(5)
        name = "%s_%s" % (prefix, name)
    trim_name = name[:32] if len(name) > 32 else name
    print("Generating ", trim_name)

    commands = [
        "env PYTHONPATH=. alembic revision --autogenerate --rev-id {id}"
        .format(id=trim_name)
    ]
    pyclean(out=0)
    run_commands(commands)
    pyclean(out=0)

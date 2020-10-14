import glob
import os
import re
import subprocess

from typer import Typer

app = Typer()


@app.command()
def miggen(name: str):
    list_of_files = glob.glob('migrations/versions/*')
    result = None
    if list_of_files:
        latest_file = max(list_of_files, key=os.path.getctime)
        pattern = r"([0-9]+)\-.*"
        result = re.search(pattern, latest_file)
    if not result:
        name = "00001_%s" % name
    else:
        prefix = str(int(result[1]) + 1).zfill(5)
        name = "%s_%s" % (prefix, name)
    print("Generating ", name)
    subprocess.call([
        "env", "PYTHONPATH=.", "alembic", "revision",
        "--autogenerate", "--rev-id", name
    ])


if __name__ == "__main__":
    app()

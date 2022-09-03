from typer import Typer

from clients import make, db, docker

app = Typer(pretty_exceptions_show_locals=False)
app.add_typer(make.app, rich_help_panel="Utilities")
app.add_typer(db.app, rich_help_panel="Utilities")
app.add_typer(docker.app, rich_help_panel="Utilities")


def main():
    app()

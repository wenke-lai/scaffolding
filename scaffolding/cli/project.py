from pathlib import Path
from typing import Annotated

import tomllib
import typer

from ..core.blueprint import Blueprint
from ..core.director import ProjectDirector
from ..core.factory import ProjectFactory
from .constant import TEMPLATES
from .template import Template

app = typer.Typer()


@app.command()
def create(
    project_folder: Annotated[Path, typer.Argument(file_okay=False)],
    template: str,
):
    match template:
        case value if Path(value).is_file():
            # custom template
            path = Path(value)
        case value if value in Template:
            # standard template
            path = (TEMPLATES / value).with_suffix(".toml")
        case _:
            raise typer.Abort()
    config = tomllib.loads(path.read_text())

    # create project
    blueprint = Blueprint(folder=project_folder, **config)
    factory = ProjectFactory(blueprint)
    director = ProjectDirector(factory)
    director.process()

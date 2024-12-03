from pathlib import Path
from typing import Annotated

import structlog
import tomllib
import typer

from ..core.blueprint import Blueprint
from ..core.director import ProjectDirector
from ..core.factory import ProjectFactory
from .constant import TEMPLATES
from .template import Template

logger = structlog.get_logger(__name__)

app = typer.Typer()


@app.command()
def create(
    project_folder: Annotated[Path, typer.Argument(file_okay=False)],
    template: str,
):
    match template:
        case value if Path(value).is_file():
            logger.debug("Custom template", path=value)
            path = Path(value)
        case value if value in Template:
            logger.debug("Standard template", template=value)
            path = (TEMPLATES / value).with_suffix(".toml")
        case _:
            logger.error("Invalid template", template=template)
            raise typer.Abort()

    logger.info(
        "setup",
        folder=project_folder,
        exists=project_folder.exists(),
        git_exists=(project_folder / ".git").exists(),
    )
    # create project
    logger.debug("Loading blueprint", path=path)
    config = tomllib.loads(path.read_text())
    blueprint = Blueprint(folder=project_folder, **config)

    logger.debug("Creating project factory", blueprint=blueprint)
    factory = ProjectFactory(blueprint)

    logger.debug("Processing project", factory=factory)
    director = ProjectDirector(factory)
    director.process()

from pathlib import Path
from typing import Annotated

import typer

from ..libs import git
from ..libs.project import ProjectDirector, PythonProjectBuilder
from .template import Template

app = typer.Typer()


@app.command()
def create(
    project_folder: Annotated[Path, typer.Argument(file_okay=False)],
    template: Template = Template.PYTHON,
):
    match template:
        case Template.PYTHON:
            builder = PythonProjectBuilder()
        case _:
            print(f"Unsupported template: {template}")
            raise typer.Abort()

    director = ProjectDirector(builder)
    project = director.create_project(project_folder, template=template)

    git.create_the_initial_commit(project.folder)

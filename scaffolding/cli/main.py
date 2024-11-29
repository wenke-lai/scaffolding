import typer

from . import project, template

app = typer.Typer()
app.add_typer(project.app, name="project")
app.add_typer(template.app, name="template")

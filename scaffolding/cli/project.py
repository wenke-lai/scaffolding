import base64
import subprocess
from pathlib import Path
from typing import Annotated

import httpx
import typer
from git import Repo

from scaffolding.cli.template import Template, load_template

app = typer.Typer()


class Project:
    folder: Path
    name: str
    template: Template


@app.command()
def create(
    project_folder: Annotated[Path, typer.Argument(file_okay=False)],
    project_name: str | None = None,
    template: Template = Template.PYTHON,
):
    # initial project
    project = Project()
    print("initializing project")

    # setup folder and name
    folder = Path(project_folder)
    folder.mkdir(parents=True, exist_ok=True)
    if any(folder.iterdir()):
        if not typer.confirm(f"Folder {folder} is not empty, continue?"):
            raise typer.Abort()
    project.folder = folder
    project.name = project_name or folder.name

    # setup template
    project.template = template
    print(project.__dict__)

    director = load_template(project.template)
    print(director.items())

    # Create initial project
    if not director["project"]["language"] == template.value:
        raise ValueError(
            f"Invalid template, project.language {director['project']['language']}"
        )
    subprocess.run(["uv", "init"], cwd=project.folder)
    subprocess.run(["uv", "add", *director["dependencies"]], cwd=project.folder)
    subprocess.run(
        ["uv", "add", "--dev", *director["dev-dependencies"]], cwd=project.folder
    )

    # Create README.md
    if director["project"]["readme"]:
        with open(project.folder / "README.md", "w") as fw:
            fw.write(f"# {project.name}")

    # Create LICENSE
    match director["project"]["license"]:
        case "MIT" | "mit":
            response = httpx.get("https://api.github.com/licenses/mit", timeout=10)
            if response.status_code == 200:
                data = response.json()
                with open(project.folder / "LICENSE", "w") as fw:
                    fw.write(data["body"])
            else:
                raise ValueError("Failed to download MIT license")
        case _:
            pass

    # setup git
    match director["project"]["language"]:
        case "python":
            response = httpx.get(
                "https://api.github.com/repos/github/gitignore/contents/Python.gitignore",
                timeout=10,
            )
            if response.status_code == 200:
                data = response.json()
                content = base64.b64decode(data["content"]).decode("utf-8")
                with open(project.folder / ".gitignore", "w") as fw:
                    fw.write(content)
        case _:
            pass

    # create git repo
    repo = Repo.init(project.folder)
    repo.git.branch("-m", "main")

    # check user config
    config = repo.config_reader()
    with repo.config_writer() as writer:
        if not config.has_option("user", "name"):
            if name := typer.prompt("What's your name?"):
                writer.set_value("user", "name", name)
            else:
                raise typer.Abort()
        if not config.has_option("user", "email"):
            if email := typer.prompt("What's your email?"):
                writer.set_value("user", "email", email)
            else:
                raise typer.Abort()

    # initial commit
    repo.git.add(".")
    repo.git.commit("-m", "initial commit")

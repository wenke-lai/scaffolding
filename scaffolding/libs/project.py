import base64
import logging
import os
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path

import httpx
import typer

from ..cli.template import Template, load_template
from .license import create_license_file

logger = logging.getLogger(__name__)


class Project:
    folder: Path = None
    name: str = None


class ProjectBuilder(ABC):
    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def build(self) -> Project:
        pass


class PythonProjectBuilder(ProjectBuilder):
    def __init__(self):
        self.reset()

    def reset(self):
        logger.debug("builder: resetting project")
        self.project = Project()

    def build(self) -> Project:
        logger.debug("builder: building project")
        project = self.project
        self.reset()
        return project

    def create_folder(self, folder: Path):
        logger.debug(f"builder: creating folder {folder}")
        folder.mkdir(parents=True, exist_ok=True)
        if any(folder.iterdir()):
            if not typer.confirm(f"Folder {folder} is not empty, continue?"):
                raise typer.Abort()
        self.project.folder = folder
        self.project.name = folder.name

    def initialize_language(self):
        logger.debug("builder: initializing language")
        subprocess.run(["uv", "init"], cwd=self.project.folder)
        useless_file = self.project.folder.joinpath("hello.py")
        if useless_file.exists():
            os.remove(useless_file)

    def install_dependencies(self, dependencies: list[str]):
        logger.debug(f"builder: installing dependencies {dependencies}")
        subprocess.run(["uv", "add", *dependencies], cwd=self.project.folder)

    def install_dev_dependencies(self, dev_dependencies: list[str]):
        logger.debug(f"builder: installing dev-dependencies {dev_dependencies}")
        subprocess.run(
            ["uv", "add", "--dev", *dev_dependencies], cwd=self.project.folder
        )

    def create_readme_file(self, skip_if_exists: bool = True):
        logger.debug("builder: creating README.md")
        readme_file = self.project.folder.joinpath("README.md")
        if skip_if_exists and readme_file.exists():
            print("README file already exists, skipping")
            return

        with open(readme_file, "w") as fw:
            fw.write(f"# {self.project.name.capitalize()}")

    def create_license_file(self, license: str):
        logger.debug(f"builder: creating LICENSE {license}")
        license_file = self.project.folder.joinpath("LICENSE")
        create_license_file(license_file, license.lower())

    def create_gitignore_file(self, skip_if_exists: bool = True):
        logger.debug("builder: creating .gitignore")
        gitignore_file = self.project.folder.joinpath(".gitignore")
        if skip_if_exists and gitignore_file.exists():
            print(".gitignore file already exists, skipping")
            return

        response = httpx.get(
            "https://api.github.com/repos/github/gitignore/contents/Python.gitignore",
            timeout=10,
        )
        if response.status_code == 200:
            data = response.json()
            content = base64.b64decode(data["content"]).decode("utf-8")
            with open(gitignore_file, "w") as fw:
                fw.write(content)
        else:
            print(f"Failed to download .gitignore file: {response.status_code}")
            raise typer.Abort()


class JavaScriptProjectBuilder(ProjectBuilder):
    pass


class RustProjectBuilder(ProjectBuilder):
    pass


class GoProjectBuilder(ProjectBuilder):
    pass


class ProjectDirector:
    def __init__(self, builder: ProjectBuilder):
        self.builder = builder

    def create_project(self, folder: Path, template: Template):
        config = load_template(template)
        self.builder.reset()

        # create language project
        self.builder.create_folder(folder)
        self.builder.initialize_language()

        # install dependencies
        self.builder.install_dependencies(config["dependencies"])
        self.builder.install_dev_dependencies(config["dev-dependencies"])

        # add scaffold files
        self.builder.create_gitignore_file()
        if config["project"]["readme"]:
            self.builder.create_readme_file()
        if config["project"]["license"]:
            self.builder.create_license_file(config["project"]["license"])

        return self.builder.build()

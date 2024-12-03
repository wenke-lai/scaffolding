from pathlib import Path

import structlog

from ..blueprint import Blueprint

logger = structlog.get_logger(__name__)


class Project:
    def create_directory(self, folder: Path) -> None:
        logger.debug("project create directory", folder=folder)
        folder.mkdir(parents=True, exist_ok=False)

    def create_readme(self, folder: Path) -> None:
        logger.debug("project create readme", folder=folder)
        readme = folder / "README.md"
        with open(readme, "w") as fw:
            fw.write(f"# {folder.name}")


class ProjectBuilder:
    def __init__(self, blueprint: Blueprint) -> None:
        self.blueprint = blueprint

    def build(self) -> None:
        logger.debug("project builder build")
        project = Project()
        project.create_directory(self.blueprint.folder)
        if self.blueprint.project.readme:
            project.create_readme(self.blueprint.folder)

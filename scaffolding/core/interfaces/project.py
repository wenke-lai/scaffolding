from pathlib import Path

from ..blueprint import Blueprint


class Project:
    def create_directory(self, folder: Path) -> None:
        folder.mkdir(parents=True, exist_ok=False)

    def create_readme(self, folder: Path) -> None:
        readme = folder / "README.md"
        with open(readme, "w") as fw:
            fw.write(f"# {folder.name}")


class ProjectBuilder:
    def __init__(self, blueprint: Blueprint) -> None:
        self.blueprint = blueprint

    def build(self) -> None:
        project = Project()
        project.create_directory(self.blueprint.folder)
        if self.blueprint.project.readme:
            project.create_readme(self.blueprint.folder)

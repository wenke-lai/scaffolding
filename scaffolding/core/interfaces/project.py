from pathlib import Path

from ..blueprint import Blueprint


class Project:
    def create_directory(self, folder: Path) -> None:
        folder.mkdir(parents=True, exist_ok=False)

    def create_readme(self, folder: Path, name: str) -> None:
        readme = folder / "README.md"
        with open(readme, "w") as fw:
            fw.write(f"# {name}")


class ProjectBuilder:
    def __init__(self, blueprint: Blueprint) -> None:
        self.blueprint = blueprint

    def build(self) -> None:
        project = Project()
        project.create_directory(self.blueprint.project.folder)
        project.create_readme(
            self.blueprint.project.folder,
            self.blueprint.project.name,
        )

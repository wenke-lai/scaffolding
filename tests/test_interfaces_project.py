from pathlib import Path
from unittest.mock import patch

from scaffolding.core.blueprint import Blueprint
from scaffolding.core.interfaces.project import Project, ProjectBuilder


def test_project(folder: Path):
    project = Project()

    project.create_directory(folder)
    assert folder.exists()

    project.create_readme(folder)
    readme = folder / "README.md"
    assert readme.exists()
    assert readme.read_text() == f"# {folder.name}"


def test_project_builder(blueprint: Blueprint):
    # create the folder cause the create_directory method is mocked
    blueprint.folder.mkdir(parents=True, exist_ok=True)

    with (
        patch.object(Project, "create_directory") as directory,
        patch.object(Project, "create_readme") as readme,
    ):
        project = ProjectBuilder(blueprint)
        project.build()

        directory.assert_called_once_with(blueprint.folder)
        readme.assert_called_once_with(blueprint.folder)

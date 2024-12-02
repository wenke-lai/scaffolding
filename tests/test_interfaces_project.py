import shutil
from pathlib import Path
from unittest.mock import patch

import pytest

from scaffolding.core import blueprint as bp
from scaffolding.core.interfaces.project import Project, ProjectBuilder


@pytest.fixture(scope="function", name="folder")
def test_folder():
    try:
        folder = Path("/tmp/test_folder")
        # don't create the folder, we want to test the creation
        yield folder
    finally:
        shutil.rmtree(folder)


def test_project(folder: Path):
    project = Project()

    project.create_directory(folder)
    assert folder.exists()
    with pytest.raises(FileExistsError):
        project.create_directory(folder)

    project.create_readme(folder, folder.name)
    readme = folder / "README.md"
    assert readme.exists()
    assert readme.read_text() == f"# {folder.name}"


def test_project_builder(folder: Path):
    blueprint = bp.Blueprint(
        project=bp.Project(folder=folder, name=folder.name, license="mit"),
        author=bp.Author(name="tester", email="tester@example.com"),
    )

    # create the folder cause the create_directory method is mocked
    folder.mkdir(parents=True, exist_ok=True)
    with (
        patch.object(Project, "create_directory") as directory,
        patch.object(Project, "create_readme") as readme,
    ):
        project = ProjectBuilder(blueprint)
        project.build()

        directory.assert_called_once_with(blueprint.project.folder)
        readme.assert_called_once_with(blueprint.project.folder, blueprint.project.name)

import shutil
from pathlib import Path
from unittest.mock import patch

import pytest

from scaffolding.core import blueprint as bp
from scaffolding.core.director import ProjectDirector
from scaffolding.core.factory import ProjectFactory


@pytest.fixture(scope="function", name="blueprint")
def blueprint():
    try:
        folder = Path("/tmp/test_folder")
        yield bp.Blueprint(
            project=bp.Project(folder=folder, name=folder.name, license="mit"),
            author=bp.Author(name="tester", email="tester@example.com"),
            language="python",
        )
    finally:
        shutil.rmtree(folder)


def test_project_director(blueprint: bp.Blueprint):
    # create the folder cause the ProjectBuilder.create_directory method is mocked
    blueprint.project.folder.mkdir(parents=True, exist_ok=False)

    with (
        patch.object(ProjectFactory, "create_project") as project,
        patch.object(ProjectFactory, "create_language") as language,
        patch.object(ProjectFactory, "create_license") as license,
        patch.object(ProjectFactory, "create_git") as git,
    ):
        factory = ProjectFactory(blueprint)
        director = ProjectDirector(factory)
        director.process()

        assert project.call_count == 1
        assert language.call_count == 1
        assert license.call_count == 1
        assert git.call_count == 1

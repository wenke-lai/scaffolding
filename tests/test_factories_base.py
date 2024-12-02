import shutil
from pathlib import Path
from unittest.mock import patch

import pytest

from scaffolding.core import blueprint as bp
from scaffolding.core.factories.base import ProjectFactory
from scaffolding.core.interfaces.git import RepositoryBuilder
from scaffolding.core.interfaces.license import LicenseBuilder
from scaffolding.core.interfaces.project import ProjectBuilder


@pytest.fixture(scope="function", name="blueprint")
def blueprint():
    try:
        folder = Path("/tmp/test_folder")
        yield bp.Blueprint(
            project=bp.Project(folder=folder, name=folder.name, license="mit"),
            author=bp.Author(name="tester", email="tester@example.com"),
        )
    finally:
        shutil.rmtree(folder)


def test_project_factory(blueprint: bp.Blueprint):
    factory = ProjectFactory(blueprint)

    # create the folder cause the ProjectBuilder.create_directory method is mocked
    blueprint.project.folder.mkdir(parents=True, exist_ok=False)

    with patch.object(ProjectBuilder, "build") as build:
        factory.create_project()
        assert build.call_count == 1

    with pytest.raises(NotImplementedError):
        factory.create_language()

    with patch.object(LicenseBuilder, "build") as build:
        factory.create_license()
        assert build.call_count == 1

    with patch.object(RepositoryBuilder, "build") as build:
        factory.create_git()
        assert build.call_count == 1

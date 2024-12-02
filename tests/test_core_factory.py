from unittest.mock import patch

from scaffolding.core.blueprint import Blueprint
from scaffolding.core.factory import ProjectFactory
from scaffolding.core.interfaces.git import RepositoryBuilder
from scaffolding.core.interfaces.language import LanguageBuilder
from scaffolding.core.interfaces.license import LicenseBuilder
from scaffolding.core.interfaces.project import ProjectBuilder


def test_project_factory(blueprint: Blueprint):
    # create the folder cause the ProjectBuilder.create_directory method is mocked
    blueprint.folder.mkdir(parents=True, exist_ok=False)

    factory = ProjectFactory(blueprint)

    with patch.object(ProjectBuilder, "build") as build:
        factory.create_project()
        assert build.call_count == 1

    with patch.object(LanguageBuilder, "build") as build:
        factory.create_language()
        assert build.call_count == 1

    with patch.object(LicenseBuilder, "build") as build:
        factory.create_license()
        assert build.call_count == 1

    with patch.object(RepositoryBuilder, "build") as build:
        factory.create_git()
        assert build.call_count == 1

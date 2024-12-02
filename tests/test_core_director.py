from unittest.mock import patch

from scaffolding.core.blueprint import Blueprint
from scaffolding.core.director import ProjectDirector
from scaffolding.core.factory import ProjectFactory


def test_project_director(blueprint: Blueprint):
    # create the folder cause the ProjectBuilder.create_directory method is mocked
    blueprint.folder.mkdir(parents=True, exist_ok=False)

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

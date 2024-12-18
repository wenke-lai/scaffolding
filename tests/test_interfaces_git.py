from pathlib import Path
from unittest.mock import call, patch

from git import Repo

from scaffolding.core.adapter.git import Git
from scaffolding.core.blueprint import Blueprint
from scaffolding.core.interfaces.git import Repository, RepositoryBuilder


def test_repository(folder: Path):
    assert not folder.exists(), "folder should not exist before this test"

    repository = Repository()
    assert isinstance(repository.git, Git)

    repository.initialize(folder)
    assert isinstance(repository.git, Git)
    assert (folder / ".git").exists()

    repo = Repo.init(folder, mkdir=False)

    repository.configure("user", "name", "tester")
    repository.configure("user", "email", "tester@example.com")
    with repo.config_reader() as reader:
        assert reader.get_value("user", "name") == "tester"
        assert reader.get_value("user", "email") == "tester@example.com"

    # value is None, so nothing is changed
    repository.configure("user", "name", None)
    with repo.config_reader() as reader:
        assert reader.get_value("user", "name") == "tester"

    # value it not None, so it overwrited always
    repository.configure("user", "name", "new-name")
    with repo.config_reader() as reader:
        assert reader.get_value("user", "name") == "new-name"

    (folder / "README.md").touch()
    repository.commit("add README.md")
    assert not repo.is_dirty(untracked_files=True)
    assert len(list(repo.iter_commits())) == 1


def test_repository_builder(blueprint: Blueprint):
    # create the folder cause the Repository.initialize method is mocked
    blueprint.folder.mkdir(parents=True, exist_ok=False)

    blueprint.author.name = "tester"
    blueprint.author.email = "tester@example.com"

    with (
        patch.object(Repository, "initialize") as initialize,
        patch.object(Repository, "configure") as configure,
        patch.object(Repository, "commit") as commit,
    ):
        builder = RepositoryBuilder(blueprint)
        builder.build()
    # git init
    initialize.assert_called_once_with(blueprint.folder)
    # git config user.name tester
    # git config user.email tester@example.com
    configure.assert_has_calls(
        [
            call("user", "name", blueprint.author.name),
            call("user", "email", blueprint.author.email),
        ]
    )
    # git commit -m "Initial commit"
    commit.assert_called_once_with("Initial project")

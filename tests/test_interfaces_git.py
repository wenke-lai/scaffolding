import shutil
from pathlib import Path
from unittest.mock import call, patch

import pytest
from git import Repo

from scaffolding.core.interfaces.git import Repository, RepositoryBuilder


@pytest.fixture(scope="function", name="folder")
def test_folder():
    try:
        folder = Path.cwd() / "test_folder"
        folder.mkdir(parents=True, exist_ok=False)
        yield folder
    finally:
        shutil.rmtree(folder)


class FakeAuthor:
    name = "tester"
    email = "tester@example.com"


class FakeProject:
    def __init__(self, folder: Path) -> None:
        self.folder = folder


class FakeBlueprint:
    def __init__(self, folder: Path) -> None:
        self.project = FakeProject(folder)
        self.author = FakeAuthor()


def test_repository(folder: Path):
    repository = Repository()
    assert repository.repo is None

    repository.initialize(folder)
    assert isinstance(repository.repo, Repo)
    with pytest.raises(FileExistsError):
        repository.initialize(folder)

    repository.configure("user", "name", "tester")
    assert repository.repo.config_reader().get_value("user", "name") == "tester"
    repository.configure("user", "name", "new-name", overwrite_ok=False)
    assert repository.repo.config_reader().get_value("user", "name") == "tester"

    with pytest.raises(FileNotFoundError):
        repository.commit("no changes to commit")
    (folder / "README.md").touch()
    repository.commit("add README.md")
    assert not repository.repo.is_dirty(untracked_files=True)
    assert len(list(repository.repo.iter_commits())) == 1


def test_repository_builder(folder: Path):
    blueprint = FakeBlueprint(folder)

    with (
        patch.object(Repository, "initialize") as initialize,
        patch.object(Repository, "configure") as configure,
        patch.object(Repository, "commit") as commit,
    ):
        builder = RepositoryBuilder(blueprint)
        builder.build()
    # git init
    initialize.assert_called_once_with(folder)
    # git config user.name tester
    # git config user.email tester@example.com
    configure.assert_has_calls(
        [
            call("user", "name", blueprint.author.name),
            call("user", "email", blueprint.author.email),
        ]
    )
    # git commit -m "Initial commit"
    commit.assert_called_once_with("Initial commit")

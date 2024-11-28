import shutil
from pathlib import Path

import pytest
from git import Repo

from scaffolding.libs.git import create_the_initial_commit


@pytest.fixture(scope="function", name="folder")
def initialize_project_folder(monkeypatch):
    # Provide default values for git user
    inputs = iter(["username", "username@email.com"])
    monkeypatch.setattr("typer.prompt", lambda _: next(inputs))

    # Create test folder
    test_folder = Path("test_repo")
    test_folder.mkdir()

    # Add a README.md file for initial commit
    test_folder.joinpath("README.md").touch()

    yield test_folder

    # Clean up test folder
    shutil.rmtree(test_folder)


def test_basic_git_init(folder: Path):
    create_the_initial_commit(folder)
    assert (folder / ".git").exists()

    repo = Repo(folder)
    assert not repo.bare
    assert repo.active_branch.name == "main"
    assert len(list(repo.iter_commits())) > 0

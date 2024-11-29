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


@pytest.fixture(scope="function")
def original_repo_user():
    repo = Repo(".")
    reader = repo.config_reader()
    user = reader.get_value("user", "name")
    email = reader.get_value("user", "email")
    yield user, email


def test_basic_git_init(folder: Path, original_repo_user):
    original_user, original_email = original_repo_user

    create_the_initial_commit(folder)
    assert (folder / ".git").exists()

    repo = Repo(folder)
    assert not repo.bare
    assert repo.active_branch.name == "main"
    assert len(list(repo.iter_commits())) > 0

    reader = repo.config_reader()
    user = reader.get_value("user", "name")
    email = reader.get_value("user", "email")

    assert user != original_user, "this project was overwritten by test"
    assert email != original_email, "this project was overwritten by test"

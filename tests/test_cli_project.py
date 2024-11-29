import shutil
from pathlib import Path

import pytest
from typer.testing import CliRunner

from scaffolding.cli.main import app

runner = CliRunner()


@pytest.fixture(scope="function", name="folder")
def initialize_project_folder(monkeypatch):
    # fixme: refactor me using conftest.py

    # Provide default values for git user
    inputs = iter(["username", "username@email.com"])
    monkeypatch.setattr("typer.prompt", lambda _: next(inputs))

    test_folder = Path("/tmp/test_repo")
    yield str(test_folder)  # cli needs str, not Path

    # Clean up test folder
    shutil.rmtree(test_folder)


def test_app(folder: str):
    result = runner.invoke(app, ["project", "create", folder])
    assert result.exit_code == 0, result.stdout

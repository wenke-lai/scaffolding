from pathlib import Path

from typer.testing import CliRunner

from scaffolding.cli.main import app

runner = CliRunner()


def test_standard_project(folder: Path, monkeypatch):
    # Provide default values for git user
    inputs = iter(["username", "username@email.com"])
    monkeypatch.setattr("typer.prompt", lambda _: next(inputs))

    result = runner.invoke(app, ["project", "create", str(folder), "python"])
    assert result.exit_code == 0, result.stdout

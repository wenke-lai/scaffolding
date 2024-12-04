from pathlib import Path

import pytest
from git import GitCommandError
from typer.testing import CliRunner

from scaffolding.cli.main import app

runner = CliRunner()


def test_standard_project(folder: Path):
    result = runner.invoke(app, ["project", "create", str(folder), "python"])
    assert result.exit_code == 0, result.stdout

    assert (folder / ".gitignore").exists()
    assert (folder / "README.md").exists()
    assert (folder / "pyproject.toml").exists()
    assert (folder / "uv.lock").exists()
    assert (folder / ".git").is_dir()

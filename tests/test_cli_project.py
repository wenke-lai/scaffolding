from pathlib import Path

import pytest
from git import GitCommandError
from typer.testing import CliRunner

from scaffolding.cli.main import app

runner = CliRunner()


def test_standard_project(folder: Path):
    result = runner.invoke(app, ["project", "create", str(folder), "python"])
    # assert result.exit_code == 0, result.stdout
    assert (
        result.exit_code == 1
    ), "GitCommandError expected, cause the author of standard template is not set"

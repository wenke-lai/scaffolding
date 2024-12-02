import shutil
from pathlib import Path

import pytest
import tomllib

from scaffolding.cli.constant import TEMPLATES
from scaffolding.core.blueprint import Blueprint

TEST_DIR = Path("/tmp/test_folder")


@pytest.fixture(scope="function", name="blueprint")
def blueprint():
    try:
        folder = Path(TEST_DIR)

        template = TEMPLATES / "python.toml"
        config = tomllib.loads(template.read_text())
        yield Blueprint(folder=folder, **config)
    finally:
        shutil.rmtree(folder, ignore_errors=True)


@pytest.fixture(scope="function", name="folder")
def folder():
    try:
        folder = Path(TEST_DIR)
        yield folder
    finally:
        shutil.rmtree(folder, ignore_errors=True)

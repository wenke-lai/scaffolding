import shutil
from pathlib import Path
from unittest.mock import patch

import pytest

from scaffolding.core import blueprint as bp
from scaffolding.core.interfaces.language import Language, LanguageBuilder, Python


@pytest.fixture(scope="function", name="blueprint")
def blueprint():
    try:
        folder = Path("/tmp/test-language")
        folder.mkdir(parents=True, exist_ok=False)
        yield bp.Blueprint(
            project=bp.Project(folder=folder, name="test", license="MIT"),
            author=bp.Author(name="test", email="test@test.com"),
            language="python",
            dependencies=["httpx"],
            dev_dependencies=["pytest", "pytest-cov"],
        )
    finally:
        shutil.rmtree(folder)


def test_language(blueprint: bp.Blueprint):
    language = Language(blueprint.project.folder)
    assert language.cwd == blueprint.project.folder


def test_python_language(blueprint: bp.Blueprint):
    language = Python(blueprint.project.folder)
    assert language.cwd == blueprint.project.folder


def test_language_builder(blueprint: bp.Blueprint):
    builder = LanguageBuilder(blueprint)
    builder.build()

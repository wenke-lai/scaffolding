import shutil
from pathlib import Path

import pytest
import tomllib

from scaffolding.cli.template import Template
from scaffolding.libs.project import Project, ProjectDirector, PythonProjectBuilder


@pytest.fixture(scope="function", name="folder")
def project_folder():
    try:
        folder = Path("/tmp/test_repo")
        yield folder
    finally:
        shutil.rmtree(folder)


def test_python_project_builder(folder: Path):
    builder = PythonProjectBuilder()
    assert isinstance(builder.project, Project)

    builder.create_folder(folder)
    assert folder.is_dir()
    assert builder.project.folder == folder
    assert builder.project.name == folder.name

    builder.initialize_language()
    assert folder.joinpath("pyproject.toml").is_file()
    assert folder.joinpath(".python-version").is_file()
    assert not folder.joinpath("hello.py").exists()

    # todo: use pytest-subprocess to mock for testing
    builder.install_dependencies(["requests==2.32.3"])
    builder.install_dev_dependencies(["pytest>=8.3.3"])
    assert folder.joinpath("uv.lock").is_file()
    with open(folder.joinpath("pyproject.toml"), "rb") as fr:
        pyproject = tomllib.load(fr)
        assert "requests==2.32.3" in pyproject["project"]["dependencies"]
        assert "pytest>=8.3.3" in pyproject["tool"]["uv"]["dev-dependencies"]

    builder.create_readme_file()
    assert folder.joinpath("README.md").is_file()

    builder.create_license_file("mit")
    assert folder.joinpath("LICENSE").is_file()

    builder.create_gitignore_file()
    assert folder.joinpath(".gitignore").is_file()


def test_project_director(folder: Path):
    director = ProjectDirector(PythonProjectBuilder())

    # fixme: use python template to test director is weak
    project = director.create_project(folder, Template.PYTHON)
    assert project.folder == folder
    assert project.name == folder.name

    assert project.folder.joinpath(".python-version").is_file()
    assert project.folder.joinpath("pyproject.toml").is_file()
    assert not project.folder.joinpath("hello.py").exists()

    assert project.folder.joinpath("uv.lock").is_file()
    with open(project.folder.joinpath("pyproject.toml"), "rb") as fr:
        pyproject = tomllib.load(fr)
        assert not pyproject["project"]["dependencies"]

        # fixme: the latest version of the dependency is not deterministic
        count = 0
        for dep in pyproject["tool"]["uv"]["dev-dependencies"]:
            if dep.startswith("ruff") or dep.startswith("pytest"):
                count += 1
        assert count == 2

    assert project.folder.joinpath("LICENSE").is_file()
    assert project.folder.joinpath(".gitignore").is_file()
    assert project.folder.joinpath("README.md").is_file()

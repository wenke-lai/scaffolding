from pathlib import Path

from .builders import GitBuilder, LanguageBuilder, ScaffoldBuilder


class ProjectDirector:
    def create_scaffold_file(self, folder: Path, license_key: str | None):
        project = ScaffoldBuilder()
        project.create_directory(folder)
        project.create_readme(title=folder.name)
        if license_key:
            project.create_license(license_key=license_key)
        project.create_gitignore(language="python")

    def create_initial_commit(self, folder: Path):
        repository = GitBuilder(folder)
        repository.create_initial_commit()


class PythonDirector(ProjectDirector):
    def __init__(self, builder: LanguageBuilder):
        self.builder = builder

    def create_python_project(self, folder: Path):
        self.builder.setup(folder)
        self.builder.install_dependencies(folder, ["structlog"])
        self.builder.install_dev_dependencies(
            folder, ["ruff", "pytest", "pytest-cov", "bandit"]
        )
        self.builder.teardown()

    def create_django_project(self, folder: Path):
        self.builder.setup(folder)
        self.builder.install_dependencies(
            folder,
            [
                "structlog",
                "django",
                "djangorestframework",
                "django-environ",
                "django-cors-header",
            ],
        )
        self.builder.install_dev_dependencies(
            folder,
            ["ruff", "pytest", "pytest-django", "pytest-cov", "bandit"],
        )
        self.builder.teardown()


""" 
class JavaScriptDirector(ProjectDirector):
    def __init__(self, builder: LanguageBuilder):
        self.builder = builder

    def create_react_project(self):
        self.builder.setup()
        self.builder.install_dependencies(["react", "react-dom"])
        self.builder.install_dev_dependencies(["react-scripts", "typescript"])
        self.builder.teardown()
 """

import subprocess
from pathlib import Path

from ..blueprint import Blueprint


class Language:
    def __init__(self, cwd: Path):
        self.cwd = cwd


class Python(Language):
    def setup(self) -> None:
        subprocess.run(["uv", "--version"], check=True, cwd=self.cwd)

    def initialize(self) -> None:
        subprocess.run(["uv", "init"], check=True, cwd=self.cwd)
        # remove hello.py that is a demo script created by uv init
        (self.cwd / "hello.py").unlink(missing_ok=True)

    def install_dependencies(self, dependencies: dict[str, str]) -> None:
        args = [f"{name}=={version}" for name, version in dependencies.items()]
        subprocess.run(["uv", "add", *args], check=True, cwd=self.cwd)

    def install_dev_dependencies(self, dev_dependencies: dict[str, str]) -> None:
        args = [f"{name}=={version}" for name, version in dev_dependencies.items()]
        subprocess.run(["uv", "add", *args], check=True, cwd=self.cwd)


class LanguageBuilder:
    def __init__(self, blueprint: Blueprint):
        self.blueprint = blueprint

    def build(self) -> None:
        match self.blueprint.project.language:
            case "python":
                language = Python(cwd=self.blueprint.folder)
            case _:
                raise ValueError(
                    f"Unsupported language: {self.blueprint.project.language}"
                )

        language.setup()
        language.initialize()
        if self.blueprint.dependencies:
            language.install_dependencies(self.blueprint.dependencies)
        if self.blueprint.dev_dependencies:
            language.install_dev_dependencies(self.blueprint.dev_dependencies)

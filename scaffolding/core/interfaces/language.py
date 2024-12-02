import os
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
        demo_file = self.cwd / "hello.py"
        if demo_file.is_file():
            os.remove(demo_file)

    def install_dependencies(self, dependencies: list[str]) -> None:
        if dependencies:
            subprocess.run(["uv", "add", *dependencies], check=True, cwd=self.cwd)

    def install_dev_dependencies(self, dev_dependencies: list[str]) -> None:
        if dev_dependencies:
            subprocess.run(["uv", "add", *dev_dependencies], check=True, cwd=self.cwd)


class LanguageBuilder:
    def __init__(self, blueprint: Blueprint):
        self.blueprint = blueprint

    def build(self) -> None:
        match self.blueprint.language:
            case "python":
                language = Python(cwd=self.blueprint.project.folder)
            case _:
                raise ValueError(f"Unsupported language: {self.blueprint.language}")

        language.setup()
        language.initialize()
        language.install_dependencies(self.blueprint.dependencies)
        language.install_dev_dependencies(self.blueprint.dev_dependencies)

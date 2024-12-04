from pathlib import Path

from ..adapter.package_manager import Uv
from ..blueprint import Blueprint


class Language:
    def __init__(self, cwd: Path):
        self.cwd = cwd


class Python(Language):
    def __init__(self, cwd: Path):
        super().__init__(cwd)
        # todo: make it dynamic
        self.package_manager = Uv()

    def setup(self) -> None:
        if not self.package_manager.exists():
            self.package_manager.install()

    def initialize(self) -> None:
        self.package_manager.init(self.cwd)
        # remove hello.py that is a demo script created by uv init
        (self.cwd / "hello.py").unlink(missing_ok=True)

    def install_dependencies(self, dependencies: dict[str, str]) -> None:
        self.package_manager.add(self.cwd, dependencies)

    def install_dev_dependencies(self, dev_dependencies: dict[str, str]) -> None:
        self.package_manager.add(self.cwd, dev_dependencies, dev=True)


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

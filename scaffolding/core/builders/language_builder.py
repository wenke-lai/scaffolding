from abc import ABC, abstractmethod
from pathlib import Path

from ..managers import PackageManager
from .builder import Builder


class Command(ABC):
    @abstractmethod
    def invoke(self) -> None:
        pass


class LanguageBuilder(Builder):
    def __init__(self, package_manager: PackageManager):
        self.package_manager = package_manager

    def setup(self, folder: Path) -> None:
        if self.package_manager.exists():
            self.package_manager.upgrade()
        else:
            self.package_manager.install()
        self.package_manager.init(folder)

    def install_dependencies(self, cwd: Path, dependencies: list[str]) -> None:
        self.package_manager.add(cwd, dependencies)

    def install_dev_dependencies(self, cwd: Path, dependencies: list[str]) -> None:
        self.package_manager.add(cwd, dependencies, dev=True)

    def teardown(self, commands: list[Command]) -> None:
        for command in commands:
            command.invoke()

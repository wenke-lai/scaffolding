from abc import ABC, abstractmethod
from pathlib import Path

from .system import System


class PackageManager(ABC):
    def __init__(self) -> None:
        self.system = System()

    @abstractmethod
    def exists(self) -> bool:
        """check if the package manager exists"""
        pass

    @abstractmethod
    def install(self) -> None:
        """install the package manager"""
        pass

    @abstractmethod
    def upgrade(self) -> None:
        """upgrade the package manager"""
        pass

    @abstractmethod
    def init(self, folder: Path) -> None:
        """create a new project"""
        pass

    @abstractmethod
    def add(self, folder: Path, dependencies: list[str], dev=False) -> None:
        """add dependencies to the project"""
        pass

    @abstractmethod
    def remove(self, folder: Path, dependencies: list[str], dev=False) -> None:
        """remove dependencies from the project"""
        pass

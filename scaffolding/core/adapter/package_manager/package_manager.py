from abc import ABC, abstractmethod
from pathlib import Path

from ..system import System


class PackageManager(ABC):
    def __init__(self) -> None:
        self.system = System()
        self.cwd = Path.cwd()

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
    def add(self, dependencies: list[str], group: str | None = None) -> None:
        """add dependencies to the project"""
        pass

    @abstractmethod
    def remove(self, dependencies: list[str], group: str | None = None) -> None:
        """remove dependencies from the project"""
        pass

    def serialize_dependencies(self, dependencies: dict[str, str | None]) -> list[str]:
        """serialize dependency and version to a string"""

        args = []
        for dependency, version in dependencies.items():
            match version:
                case "latest" | "*" | None:
                    # latest version
                    args.append(dependency)
                case value if value[0] in [">", "<", "="]:
                    # version syntax `package>=1.0.0` `package>=1.0.0,<2.0.0`
                    args.append(dependency + value)
                case value if value.startswith("@"):
                    # poetry specific syntax `package@version`
                    args.append(dependency + value)
                case _:
                    # default version syntax
                    args.append(f"{dependency}>={version}")
        return args

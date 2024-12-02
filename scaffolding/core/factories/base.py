from abc import ABC, abstractmethod

from ..blueprint import Blueprint
from ..interfaces.git import RepositoryBuilder
from ..interfaces.license import LicenseBuilder
from ..interfaces.project import ProjectBuilder


class Factory(ABC):
    @abstractmethod
    def create_project(self) -> None:
        pass

    @abstractmethod
    def create_language(self) -> None:
        pass

    @abstractmethod
    def create_license(self) -> None:
        pass

    @abstractmethod
    def create_git(self) -> None:
        pass


class ProjectFactory(Factory):
    def __init__(self, blueprint: Blueprint) -> None:
        self.blueprint = blueprint

    def create_project(self) -> None:
        project = ProjectBuilder(self.blueprint)
        project.build()

    def create_language(self) -> None:
        raise NotImplementedError("`.create_language` not implemented")

    def create_license(self) -> None:
        license = LicenseBuilder(self.blueprint)
        license.build()

    def create_git(self) -> None:
        git = RepositoryBuilder(self.blueprint)
        git.build()

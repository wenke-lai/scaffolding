from abc import ABC, abstractmethod

import structlog

from .blueprint import Blueprint
from .interfaces.git import RepositoryBuilder
from .interfaces.language import LanguageBuilder
from .interfaces.license import LicenseBuilder
from .interfaces.project import ProjectBuilder

logger = structlog.get_logger(__name__)


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
        logger.debug("factory create project")
        project = ProjectBuilder(self.blueprint)
        project.build()

    def create_language(self) -> None:
        logger.debug("factory create language")
        language = LanguageBuilder(self.blueprint)
        language.build()

    def create_license(self) -> None:
        logger.debug("factory create license")
        license = LicenseBuilder(self.blueprint)
        license.build()

    def create_git(self) -> None:
        logger.debug("factory create git")
        git = RepositoryBuilder(self.blueprint)
        git.build()

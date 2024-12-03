import logging
from pathlib import Path

from git import Repo

from ..blueprint import Blueprint

logger = logging.getLogger(__name__)


class Repository:
    def __init__(self) -> None:
        self.repo = None

    def initialize(self, folder: Path) -> None:
        self.repo = Repo.init(folder, mkdir=True)

    def configure(self, section: str, field: str, value: str | None) -> None:
        if value is None:
            return
        with self.repo.config_writer() as writer:
            writer.set_value(section, field, value)

    def commit(self, message: str) -> None:
        self.repo.git.add(["."])
        self.repo.git.commit("-m", message)


class RepositoryBuilder:
    def __init__(self, blueprint: Blueprint) -> None:
        self.blueprint = blueprint

    def build(self) -> None:
        repository = Repository()
        repository.initialize(self.blueprint.folder)
        if self.blueprint.author.name:
            repository.configure("user", "name", self.blueprint.author.name)
        if self.blueprint.author.email:
            repository.configure("user", "email", self.blueprint.author.email)
        repository.commit("Initial project")

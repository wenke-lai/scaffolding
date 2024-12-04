import logging
from pathlib import Path

from ..adapter.git import Git
from ..blueprint import Blueprint

logger = logging.getLogger(__name__)


class Repository:
    def __init__(self) -> None:
        self.git = Git()

    def initialize(self, folder: Path) -> None:
        if not self.git.exists():
            # todo: skip install git command, needs root privileges
            raise RuntimeError("Git is not installed")

        self.git.init(folder)

    def configure(self, section: str, field: str, value: str | None) -> None:
        self.git.write_config(section, field, value)

    def commit(self, message: str) -> None:
        self.git.add()  # add all untracked files
        self.git.commit(message)


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

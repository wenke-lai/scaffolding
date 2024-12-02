import logging
from configparser import NoSectionError
from pathlib import Path

from git import Repo

from ..blueprint import Blueprint

logger = logging.getLogger(__name__)


class Repository:
    def __init__(self) -> None:
        self.repo = None

    def initialize(self, folder: Path) -> None:
        if (folder / ".git").exists():
            raise FileExistsError(f"Git repository already exists in {folder}")
        self.repo = Repo.init(folder)

    def configure(
        self,
        section: str,
        field: str,
        value: str | None = None,
        overwrite_ok: bool = False,
    ) -> None:
        if value is None:
            return
        with self.repo.config_reader() as reader, self.repo.config_writer() as writer:
            try:
                exists_value = reader.get_value(section, field)
                if overwrite_ok or not exists_value:
                    writer.set_value(section, field, value)
                return
            except NoSectionError:
                writer.set_value(section, field, value)

        logger.warning(f"Git config `{section}.{field}` already exists")

    def commit(self, message: str) -> None:
        if self.repo.is_dirty(untracked_files=True):
            self.repo.git.add(["."])
            self.repo.git.commit("-m", message)
            return
        raise FileNotFoundError("No changes to commit")


class RepositoryBuilder:
    def __init__(self, blueprint: Blueprint) -> None:
        self.blueprint = blueprint

    def build(self) -> None:
        repository = Repository()
        repository.initialize(self.blueprint.project.folder)
        repository.configure("user", "name", self.blueprint.author.name)
        repository.configure("user", "email", self.blueprint.author.email)
        repository.commit("Initial commit")

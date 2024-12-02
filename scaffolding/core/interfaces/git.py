import logging
from configparser import NoOptionError, NoSectionError
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
            except (NoSectionError, NoOptionError):
                writer.set_value(section, field, value)

        logger.warning(f"Git config `{section}.{field}` already exists")

    def commit(self, message: str) -> None:
        if self.repo.is_dirty(untracked_files=True):
            self.repo.git.add(["."])
            if self.check_user_exists():
                self.repo.git.commit("-m", message)
            else:
                logger.warning("Git user not configured, skipping commit")
            return
        raise FileNotFoundError("No changes to commit")

    def check_user_exists(self) -> bool:
        with self.repo.config_reader() as reader:
            try:
                name = reader.get_value("user", "name")
                email = reader.get_value("user", "email")
                return all([name, email])
            except (NoSectionError, NoOptionError):
                return False


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
        repository.commit("Initial commit")

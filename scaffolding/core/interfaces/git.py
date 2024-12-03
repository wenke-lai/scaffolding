from configparser import NoOptionError, NoSectionError
from pathlib import Path

import structlog
from git import Repo

from ..blueprint import Blueprint

logger = structlog.get_logger(__name__)


class Repository:
    def __init__(self) -> None:
        self.repo = None
        self.log = None

    def initialize(self, folder: Path) -> None:
        logger.debug("`git init`", folder=folder, git_exists=(folder / ".git").exists())
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
        logger.debug(
            "`git config`",
            section=section,
            field=field,
            value=value,
            overwrite_ok=overwrite_ok,
        )
        if value is None:
            logger.warning("value is None")
            return
        with self.repo.config_reader() as reader, self.repo.config_writer() as writer:
            try:
                exists_value = reader.get_value(section, field)
                if overwrite_ok or not exists_value:
                    logger.debug("setting value")
                    writer.set_value(section, field, value)
                else:
                    logger.warning(
                        "`git config`", section=section, field=field, value=value
                    )
            except (NoSectionError, NoOptionError):
                writer.set_value(section, field, value)

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

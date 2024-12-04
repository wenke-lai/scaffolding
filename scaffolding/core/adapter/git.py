from pathlib import Path

from git import Repo

from .system import System


class Git:
    def __init__(self) -> None:
        self.repo: Repo | None = None
        self.system = System()

    def exists(self) -> None:
        try:
            command = ["git", "--version"]
            self.system.invoke(command)
            return True
        except FileNotFoundError:
            return False

    def install(self) -> None:
        command = ["apt-get", "install", "git"]
        self.system.invoke(command)

    def upgrade(self) -> None:
        command = ["apt-get", "install", "--only-upgrade", "git"]
        self.system.invoke(command)

    def init(self, cwd: Path) -> None:
        self.repo = Repo.init(cwd, mkdir=True)

    def clone(self, cwd: Path, url: str) -> None:
        self.repo = Repo.clone_from(url, to_path=cwd)

    def untracked_files(self) -> list[str]:
        assert self.repo is not None, "Repository not initialized"
        return self.repo.untracked_files

    def add(self, paths: list[str] | None = None) -> None:
        self.repo.index.add(paths or self.repo.untracked_files)

    def commit(self, message: str) -> None:
        if self.repo.is_dirty():
            self.repo.index.commit(message)

    def read_config(self, section: str, field: str) -> str | None:
        with self.repo.config_reader() as reader:
            return reader.get_value(section, field, default=None)

    def write_config(self, section: str, field: str, value: str | None) -> None:
        if value is None:
            return

        with self.repo.config_writer() as writer:
            writer.set_value(section, field, value)

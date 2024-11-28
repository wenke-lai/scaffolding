from abc import ABC, abstractmethod
from pathlib import Path
from typing import Self

import typer
from git import Repo


class Repository(Repo):
    pass


class Builder(ABC):
    @abstractmethod
    def reset(self) -> Self:
        pass


class GitBuilder(Builder):
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> Self:
        self.repo = None
        return self

    def init(self, folder: Path) -> Self:
        if (folder / ".git").exists():
            print(f"Git repository already exists in {folder}")
            raise typer.Abort()

        self.repo = Repository.init(folder)
        return self

    def config(self, section: str, field: str, value: str) -> Self:
        if not value:
            print(f"Invalid {section}.{field}: {value}")
            raise typer.Abort()

        with self.repo.config_writer() as writer:
            writer.set_value(section, field, value)
        return self

    def commit(self, message: str) -> Self:
        if not self.repo.is_dirty(untracked_files=True):
            print("No changes to commit")
            raise typer.Abort()

        self.repo.git.add(".")
        self.repo.git.commit("-m", message)
        return self

    def build(self) -> Repository:
        repo = self.repo
        self.reset()
        return repo


class SVNBuilder(Builder):
    def reset(self) -> Self:
        raise NotImplementedError("SVN is not currently supported")


class RepositoryDirector:
    def __init__(self, builder: Builder) -> None:
        self.builder = builder

    def create_a_initial_commit(self, folder: Path) -> Repository:
        return (
            self.builder.reset()
            .init(folder)
            .config("user", "name", typer.prompt("What's your name?"))
            .config("user", "email", typer.prompt("What's your email?"))
            .commit("initial commit")
            .build()
        )


def create_a_initial_commit(folder: Path) -> Repository:
    builder = GitBuilder()
    director = RepositoryDirector(builder)
    return director.create_a_initial_commit(folder)

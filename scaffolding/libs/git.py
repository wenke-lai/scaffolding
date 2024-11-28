from pathlib import Path

import typer
from git import GitConfigParser, Repo


def _configure_git_user(
    config: GitConfigParser,
    writer: GitConfigParser,
    field: str,
):
    if config.has_option("user", field):
        return

    if value := typer.prompt(f"What's your {field}?"):
        writer.set_value("user", field, value)
    else:
        print(f"Invalid {field}")
        raise typer.Abort()


def create_the_initial_commit(folder: Path):
    if (folder / ".git").exists():
        print(f"Git repository already exists in {folder}")
        raise typer.Abort()

    # create the git repo
    repo = Repo.init(folder)
    repo.git.branch("-m", "main")

    # verify and configure git user settings if not already set
    config = repo.config_reader()
    with repo.config_writer() as writer:
        _configure_git_user(config, writer, "name")
        _configure_git_user(config, writer, "email")

    # create the initial commit
    repo.git.add(".")
    repo.git.commit("-m", "initial commit")

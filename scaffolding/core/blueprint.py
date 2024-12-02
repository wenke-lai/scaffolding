from dataclasses import dataclass
from pathlib import Path


@dataclass
class Project:
    folder: Path
    name: str
    license: str


@dataclass
class Author:
    name: str
    email: str


@dataclass
class Blueprint:
    project: Project
    author: Author

    language: str
    dependencies: list[str] | None = None
    dev_dependencies: list[str] | None = None

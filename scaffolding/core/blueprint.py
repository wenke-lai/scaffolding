from pathlib import Path

from pydantic import BaseModel, Field


class Project(BaseModel):
    language: str | None = None
    readme: bool | None = None
    license: str | None = None
    git: bool | None = None


class Author(BaseModel):
    name: str | None = None
    email: str | None = None


class Blueprint(BaseModel):
    folder: Path

    project: Project

    author: Author

    dependencies: dict[str, str] = Field(default_factory=dict)

    dev_dependencies: dict[str, str] = Field(default_factory=dict)

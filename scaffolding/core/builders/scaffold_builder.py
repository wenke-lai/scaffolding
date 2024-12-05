from pathlib import Path

import httpx

from .builder import Builder


def get_license_content(license_key: str) -> str:
    response = httpx.get(f"https://api.github.com/licenses/{license_key}")
    response.raise_for_status()
    return response.json()["body"]


def get_gitignore_content(language: str) -> str:
    response = httpx.get(
        f"https://raw.githubusercontent.com/github/gitignore/main/{language.capitalize()}.gitignore"
    )
    response.raise_for_status()
    return response.text


class ScaffoldBuilder(Builder):
    def create_directory(self, folder: Path) -> None:
        folder.mkdir(parents=True, exist_ok=True)

    def create_readme(self, folder: Path) -> None:
        with open(folder / "README.md", "w") as fw:
            fw.write(f"# {folder.name.capitalize()}")

    def create_license(self, folder: Path, license_key: str) -> None:
        content = get_license_content(license_key)
        with open(folder / "LICENSE", "w") as fw:
            fw.write(content)

    def create_gitignore(self, folder: Path, language: str) -> None:
        content = get_gitignore_content(language)
        with open(folder / ".gitignore", "w") as fw:
            fw.write(content)

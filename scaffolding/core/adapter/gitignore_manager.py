from pathlib import Path
from urllib.parse import urljoin

import httpx

GITHUB_ENDPOINT: str = (
    "https://raw.githubusercontent.com/github/gitignore/refs/heads/main/"
)


class GitIgnoreManager:
    def download(self, template_name: str, folder: Path) -> None:
        response = httpx.get(urljoin(GITHUB_ENDPOINT, template_name), timeout=10)
        response.raise_for_status()

        with open(folder / ".gitignore", "w") as fw:
            fw.write(response.text)


class PythonGitIgnoreManager(GitIgnoreManager):
    def download(self, folder: Path) -> None:
        super().download("Python.gitignore", folder)


class RustGitIgnoreManager(GitIgnoreManager):
    def download(self, folder: Path) -> None:
        super().download("Rust.gitignore", folder)


class GoGitIgnoreManager(GitIgnoreManager):
    def download(self, folder: Path) -> None:
        super().download("Go.gitignore", folder)


class JavaScriptGitIgnoreManager(GitIgnoreManager):
    def download(self, folder: Path) -> None:
        # * the .gitignore should be created by frontend framework scaffolding, e.g. vite.

        path = folder / ".gitignore"
        if not path.exists():
            path.touch()


class TypeScriptGitIgnoreManager(JavaScriptGitIgnoreManager):
    pass

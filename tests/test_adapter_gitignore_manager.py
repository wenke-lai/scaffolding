from pathlib import Path
from unittest.mock import Mock, patch

from scaffolding.core.adapter.gitignore_manager import (
    GitIgnoreManager,
    GoGitIgnoreManager,
    JavaScriptGitIgnoreManager,
    PythonGitIgnoreManager,
    RustGitIgnoreManager,
    TypeScriptGitIgnoreManager,
)


@patch("httpx.get", return_value=Mock(text="content"))
def test_gitignore_manager(mock: Mock, folder: Path):
    folder.mkdir(parents=True, exist_ok=False)

    manager = GitIgnoreManager()
    manager.download("fake", folder)
    assert mock.call_count == 1
    assert (folder / ".gitignore").read_text() == "content"


@patch.object(GitIgnoreManager, "download")
def test_python_gitignore_manager(mock: Mock, folder: Path):
    manager = PythonGitIgnoreManager()
    manager.download(folder)
    mock.assert_called_once_with("Python.gitignore", folder)


@patch.object(GitIgnoreManager, "download")
def test_rust_gitignore_manager(mock: Mock, folder: Path):
    manager = RustGitIgnoreManager()
    manager.download(folder)
    mock.assert_called_once_with("Rust.gitignore", folder)


@patch.object(GitIgnoreManager, "download")
def test_go_gitignore_manager(mock: Mock, folder: Path):
    manager = GoGitIgnoreManager()
    manager.download(folder)
    mock.assert_called_once_with("Go.gitignore", folder)


@patch.object(GitIgnoreManager, "download")
def test_javascript_gitignore_manager(mock: Mock, folder: Path):
    folder.mkdir(parents=True, exist_ok=False)

    manager = JavaScriptGitIgnoreManager()
    manager.download(folder)
    assert (folder / ".gitignore").exists()
    assert (
        mock.call_count == 0
    ), "JavaScript .gitignore is created by frontend framework scaffolding"


@patch.object(GitIgnoreManager, "download")
def test_typescript_gitignore_manager(mock: Mock, folder: Path):
    folder.mkdir(parents=True, exist_ok=False)

    manager = TypeScriptGitIgnoreManager()
    assert isinstance(manager, JavaScriptGitIgnoreManager)

    manager.download(folder)
    assert (folder / ".gitignore").exists()
    assert (
        mock.call_count == 0
    ), "TypeScript .gitignore is created by frontend framework scaffolding"

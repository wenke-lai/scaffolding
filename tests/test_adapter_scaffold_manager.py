from pathlib import Path

from scaffolding.core.adapter.scaffold_manager import ReadmeManager


def test_readme_manager(folder: Path):
    folder.mkdir(parents=True, exist_ok=False)

    manager = ReadmeManager()
    manager.create_readme(folder)

    assert (folder / "README.md").is_file()
    assert (folder / "README.md").read_text() == f"# {folder.name}"

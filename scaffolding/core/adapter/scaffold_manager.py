from pathlib import Path


class ScaffoldManager:
    pass


class ReadmeManager(ScaffoldManager):
    def create_readme(self, folder: Path) -> None:
        with open(folder / "README.md", "w") as fw:
            fw.write(f"# {folder.name}")

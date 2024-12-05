from pathlib import Path

from .package_manager import PackageManager


class Uv(PackageManager):
    def exists(self) -> bool:
        try:
            self.system.invoke(["uv", "--version"])
            return True
        except FileNotFoundError:  # uv command not found
            return False

    def install(self) -> None:
        command = ["curl", "-fsSL", "https://astral.sh/uv/install.sh", "|", "sh"]
        self.system.invoke(command)

    def upgrade(self) -> None:
        command = ["uv", "self", "update"]
        self.system.invoke(command)

    def init(self, cwd: Path) -> None:
        cwd.mkdir(parents=True, exist_ok=True)
        command = ["uv", "init"]
        self.system.invoke(command, cwd=cwd)
        (cwd / "hello.py").unlink()

    def add(self, cwd: Path, dependencies: list[str], dev=False) -> None:
        options = ["-d"] if dev else []
        command = ["uv", "add", *options, *dependencies]
        self.system.invoke(command, cwd=cwd)

    def remove(self, cwd: Path, dependencies: list[str], dev=False) -> None:
        options = ["--dev"] if dev else []
        command = ["uv", "remove", *options, *dependencies]
        self.system.invoke(command, cwd=cwd)

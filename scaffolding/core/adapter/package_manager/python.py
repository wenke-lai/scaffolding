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
        command = ["curl", "-LsSf", "https://astral.sh/uv/install.sh", "|", "sh"]
        self.system.invoke(command)

    def upgrade(self) -> None:
        command = ["uv", "self", "update"]
        self.system.invoke(command)

    def init(self, cwd: Path) -> None:
        cwd.mkdir(parents=True, exist_ok=True)
        command = ["uv", "init"]
        self.system.invoke(command, cwd=cwd)

    def add(
        self, cwd: Path, dependencies: dict[str, str | None], dev: bool = False
    ) -> None:
        options = ["--dev"] if dev else []
        dependencies = self.serialize_dependencies(dependencies)
        command = ["uv", "add", *options, *dependencies]
        self.system.invoke(command, cwd=cwd)

    def remove(self, cwd: Path, dependencies: list[str], dev: bool = False) -> None:
        options = ["--dev"] if dev else []
        command = ["uv", "remove", *options, *dependencies]
        self.system.invoke(command, cwd=cwd)


# class Poetry(PackageManager):
#     def exists(self) -> bool:
#         try:
#             self.system.invoke(["poetry", "--version"])
#             return True
#         except FileNotFoundError:  # poetry command not found
#             return False

#     def install(self) -> None:
#         url = "https://install.python-poetry.org"
#         self.system.invoke(["curl", "-sSL", url, "|", "python3", "-"])

#     def upgrade(self) -> None:
#         self.system.invoke(["poetry", "self", "update"])

#     def init(self, folder: Path) -> None:
#         folder.mkdir(parents=True, exist_ok=True)
#         self.system.invoke(["poetry", "new", folder])

#     def add(self, dependencies: dict[str, str]) -> None:
#         dependencies = self.serialize_dependencies(dependencies)
#         self.system.invoke(["poetry", "add", *dependencies])

#     def remove(self, dependencies: dict[str, str]) -> None:
#         dependencies = list(dependencies.keys())
#         self.system.invoke(["poetry", "remove", *dependencies])


# class Pip(PackageManager):
#     def exists(self) -> bool:
#         try:
#             self.system.invoke(["pip", "--version"])
#             return True
#         except FileNotFoundError:  # pip command not found
#             return False

#     def install(self) -> None:
#         url = "https://bootstrap.pypa.io/get-pip.py"
#         self.system.invoke(["curl", "-LsSf", url, "|", "python3", "-"])

#     def upgrade(self) -> None:
#         self.system.invoke(["pip", "install", "--upgrade", "pip"])

#     def init(self, folder: Path) -> None:
#         folder.mkdir(parents=True, exist_ok=True)
#         (folder / "requirements.txt").touch()

#     def add(self, dependencies: dict[str, str | None]) -> None:
#         self.system.invoke(["pip", "install", *dependencies])

#     def remove(self, dependencies: list[str]) -> None:
#         self.system.invoke(["pip", "uninstall", *dependencies])

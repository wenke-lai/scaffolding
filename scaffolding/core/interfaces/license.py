from pathlib import Path

from ..adapter.license_manager import MitLicenseManager
from ..blueprint import Blueprint


class License:
    def __init__(self) -> None:
        # todo: make it dynamic
        self.license_manager = MitLicenseManager()

    def download(self) -> None:
        self.license_manager.download()

    def implement(self, *args, **kwargs) -> None:
        self.license_manager.implement(*args, **kwargs)

    def save(self, folder: Path) -> None:
        self.license_manager.save(folder)


class LicenseBuilder:
    def __init__(self, blueprint: Blueprint) -> None:
        self.blueprint = blueprint

    def build(self) -> None:
        license = License()
        license.download()
        license.implement(fullname=self.blueprint.author.name)
        license.save(self.blueprint.folder)

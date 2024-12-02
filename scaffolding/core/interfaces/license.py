from datetime import date
from pathlib import Path
from urllib.parse import urljoin

import httpx

from ..blueprint import Blueprint

GITHUB_API_ENDPOINT: str = "https://api.github.com"


class License:
    license_key: str

    def __init__(self) -> None:
        self.content = ""

    def download(self) -> None:
        assert self.license_key, "License key is not set"
        response = httpx.get(
            urljoin(GITHUB_API_ENDPOINT, f"/licenses/{self.license_key}"), timeout=10
        )
        response.raise_for_status()
        self.content = response.json()["body"]

    def implement(self, *args, **kwargs) -> None:
        pass

    def save(self, folder: Path) -> None:
        file = folder / "LICENSE"
        if file.exists():
            raise FileExistsError(f"License file already exists in {folder}")
        with open(file, "w") as fw:
            fw.write(self.content)


class MITLicense(License):
    license_key = "mit"

    def implement(self, fullname: str, *args, **kwargs) -> None:
        self.content = self.content.replace("[year]", str(date.today().year))
        if fullname is not None:
            self.content = self.content.replace("[fullname]", fullname)


class Apache2License(License):
    license_key = "apache-2.0"


class GPL2License(License):
    license_key = "gpl-2.0"


class GPL3License(License):
    license_key = "gpl-3.0"


class LicenseBuilder:
    def __init__(self, blueprint: Blueprint) -> None:
        self.blueprint = blueprint

    def build(self) -> None:
        match self.blueprint.project.license:
            case "MIT" | "mit":
                license = MITLicense()
            case "Apache-2.0" | "apache-2.0":
                license = Apache2License()
            case "GPL-2.0" | "gpl-2.0":
                license = GPL2License()
            case "GPL-3.0" | "gpl-3.0":
                license = GPL3License()
            case _:
                # no license
                return

        license.download()
        license.implement(fullname=self.blueprint.author.name)
        license.save(self.blueprint.folder)

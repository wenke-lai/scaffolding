from datetime import date
from pathlib import Path

import httpx

GITHUB_API_ENDPOINT: str = "https://api.github.com"


class LicenseManager:
    license_key: str

    def __init__(self) -> None:
        self.content = ""

    def download(self) -> None:
        response = httpx.get(
            f"{GITHUB_API_ENDPOINT}/licenses/{self.license_key}", timeout=10
        )
        response.raise_for_status()
        self.content = response.json()["body"]

    def implement(self, *args, **kwargs) -> None:
        pass

    def save(self, folder: Path) -> None:
        with open(folder / "LICENSE", "w") as fw:
            fw.write(self.content)


class MitLicenseManager(LicenseManager):
    license_key = "mit"

    def implement(self, fullname: str | None = None) -> None:
        self.content = self.content.replace("[year]", str(date.today().year))
        if fullname:
            self.content = self.content.replace("[fullname]", fullname)


class Apache2LicenseManager(LicenseManager):
    license_key = "apache-2.0"


class GPL2LicenseManager(LicenseManager):
    license_key = "gpl-2.0"


class GPL3LicenseManager(LicenseManager):
    license_key = "gpl-3.0"

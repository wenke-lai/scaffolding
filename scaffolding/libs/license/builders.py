from abc import ABC, abstractmethod
from datetime import date
from pathlib import Path
from typing import Self
from urllib.parse import urljoin

import httpx

LICENSE_FILE = "LICENSE"


GITHUB_ENDPOINT: str = "https://api.github.com"


class LicenseBuilder(ABC):
    endpoint: str = GITHUB_ENDPOINT
    license_key: str = ""

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.content: str = ""

    def build(self) -> str:
        license = self.content
        self.reset()
        return license

    def download(self) -> Self:
        assert self.license_key, "License key is not set"

        url = urljoin(self.endpoint, f"licenses/{self.license_key}")
        response = httpx.get(url, timeout=10)
        response.raise_for_status()
        self.content = response.json()["body"]
        return self

    @abstractmethod
    def implement(self, *args, **kwargs) -> Self:
        return self

    def save(self, folder: Path) -> Self:
        assert self.content, "License content is not set"

        with open(folder / LICENSE_FILE, "w") as fw:
            fw.write(self.content)
        return self


class MITLicenseBuilder(LicenseBuilder):
    license_key: str = "mit"

    def implement(self, name: str = "[fullname]") -> Self:
        self.content = self.content.replace("[year]", str(date.today().year))
        self.content = self.content.replace("[fullname]", name)
        return self


class Apache2LicenseBuilder(LicenseBuilder):
    license_key: str = "apache-2.0"

    def implement(self, *args, **kwargs) -> Self:
        return super().implement(*args, **kwargs)


class GPL2LicenseBuilder(LicenseBuilder):
    license_key: str = "gpl-2.0"

    def implement(self, *args, **kwargs) -> Self:
        return super().implement(*args, **kwargs)


class GPL3LicenseBuilder(LicenseBuilder):
    license_key: str = "gpl-3.0"

    def implement(self, *args, **kwargs) -> Self:
        return super().implement(*args, **kwargs)

from pathlib import Path
from typing import Generator

import httpx

LICENSE_FILE = "LICENSE"


def list_licenses() -> Generator[dict, None, None]:
    """List all licenses from GitHub"""
    response = httpx.get("https://api.github.com/licenses", timeout=10)
    response.raise_for_status()
    for license in response.json():
        yield {
            "key": license["key"],
            "url": license["url"],
        }


def get_license(key: str | None = None, url: str | None = None) -> dict:
    assert key is not None or url is not None, "key or url is required"

    if key:
        url = f"https://api.github.com/licenses/{key}"
    else:
        if url is None:
            raise ValueError("url is required")

    response = httpx.get(url, timeout=10)
    response.raise_for_status()
    license = response.json()
    # fixme: we should implement license by license["implementation"]
    return {
        "implementation": license["implementation"],
        "body": license["body"],
    }


def create_license_file(path: Path, license_key: str):
    license = get_license(license_key)
    with open(path, "w") as fw:
        fw.write(license["body"])

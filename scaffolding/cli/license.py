from enum import StrEnum

import click
import httpx


class LicenseEnum(StrEnum):
    MIT = "mit"
    APACHE2 = "apache-2.0"
    GPL2 = "gpl-2.0"
    GPL3 = "gpl-3.0"


@click.group()
def license():
    print("license commands")


@license.command()
def list():
    response = httpx.get("https://api.github.com/licenses", timeout=10)
    response.raise_for_status()

    for item in response.json():
        print(item["key"], item["name"])


@license.command()
@click.argument("license", type=click.Choice(LicenseEnum))
def get(license: LicenseEnum):
    response = httpx.get(
        f"https://api.github.com/licenses/{license.value}",
        timeout=10,
    )
    response.raise_for_status()

    print(response.json())


@license.command()
@click.argument("license", type=click.Choice(LicenseEnum))
@click.option("--output", "-o", type=click.File("w"), required=True)
def create(license: LicenseEnum, output: click.File):
    response = httpx.get(
        f"https://api.github.com/licenses/{license.value}",
        timeout=10,
    )
    response.raise_for_status()

    output.write(response.json()["body"])

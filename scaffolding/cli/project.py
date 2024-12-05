from enum import StrEnum
from pathlib import Path

import click
from core import managers
from core.builders import LanguageBuilder
from core.director import PythonDirector


class PackageManagerEnum(StrEnum):
    UV = "uv"


class FrameworkEnum(StrEnum):
    DJANGO = "django"


class LicenseEnum(StrEnum):
    MIT = "mit"
    APACHE2 = "apache-2.0"
    GPL2 = "gpl-2.0"
    GPL3 = "gpl-3.0"


@click.group()
def project():
    pass


@project.command()
@click.argument("folder", type=click.Path(file_okay=False, dir_okay=True))
@click.option(
    "--package-manager", "-p", required=True, type=click.Choice(PackageManagerEnum)
)
@click.option("--framework", "-f", type=click.Choice(FrameworkEnum), default=None)
@click.option("--license", "-l", type=click.Choice(LicenseEnum), default=None)
def create(
    folder: Path,
    package_manager: PackageManagerEnum,
    framework: FrameworkEnum,
    license: LicenseEnum,
):
    match package_manager:
        case PackageManagerEnum.UV:
            builder = LanguageBuilder(managers.Uv())
            director = PythonDirector(builder)
        case _:
            raise RuntimeError(f"Unsupported package manager: {package_manager}")

    director.create_scaffold_file(folder, license_key=license.value)
    match framework:
        case FrameworkEnum.DJANGO:
            director.create_django_project(folder)
        case _:
            director.create_python_project(folder)
    director.create_initial_commit(folder)

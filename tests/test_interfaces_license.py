from datetime import date
from pathlib import Path
from unittest.mock import Mock, patch

from scaffolding.core.blueprint import Blueprint
from scaffolding.core.interfaces.license import (
    Apache2License,
    GPL2License,
    GPL3License,
    License,
    LicenseBuilder,
    MITLicense,
)


def test_license(folder: Path):
    folder.mkdir(parents=True, exist_ok=False)

    license = License()
    assert license.content == ""

    response = {"body": "content"}
    license.license_key = "mit"
    with patch("httpx.get", return_value=Mock(json=lambda: response)) as mock:
        license.download()
        assert mock.call_count == 1
        assert license.content == response["body"]

    license.implement()  # default implementation does nothing
    assert license.content == response["body"]

    license.save(folder)
    file = folder / "LICENSE"
    assert file.exists()
    assert file.read_text() == response["body"]


def test_mit_license():
    license = MITLicense()
    assert license.license_key == "mit"

    license.content = "prefix [year] [fullname] suffix"
    license.implement(fullname="tester")
    assert license.content == f"prefix {date.today().year} tester suffix"


def test_apache2_license():
    license = Apache2License()
    assert license.license_key == "apache-2.0"


def test_gpl2_license():
    license = GPL2License()
    assert license.license_key == "gpl-2.0"


def test_gpl3_license():
    license = GPL3License()
    assert license.license_key == "gpl-3.0"


def test_license_builder(blueprint: Blueprint):
    blueprint.folder.mkdir(parents=True, exist_ok=False)

    builder = LicenseBuilder(blueprint=blueprint)
    with (
        patch.object(MITLicense, "download") as download,
        patch.object(MITLicense, "implement") as implement,
        patch.object(MITLicense, "save") as save,
    ):
        builder.build()

        download.assert_called_once()
        implement.assert_called_once_with(fullname=blueprint.author.name)
        save.assert_called_once_with(blueprint.folder)

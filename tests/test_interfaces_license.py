from pathlib import Path
from unittest.mock import Mock, patch

from scaffolding.core.adapter.license_manager import MitLicenseManager
from scaffolding.core.blueprint import Blueprint
from scaffolding.core.interfaces.license import License, LicenseBuilder


def test_license(folder: Path):
    folder.mkdir(parents=True, exist_ok=False)

    license = License()

    response = {"body": "content"}
    license.license_key = "mit"
    with patch("httpx.get", return_value=Mock(json=lambda: response)) as mock:
        license.download()
        assert mock.call_count == 1
        assert license.license_manager.content == response["body"]

    license.implement()  # default implementation does nothing
    assert license.license_manager.content == response["body"]

    license.save(folder)
    file = folder / "LICENSE"
    assert file.exists()
    assert file.read_text() == response["body"]


def test_license_builder(blueprint: Blueprint):
    blueprint.folder.mkdir(parents=True, exist_ok=False)

    builder = LicenseBuilder(blueprint=blueprint)
    with (
        patch.object(MitLicenseManager, "download") as download,
        patch.object(MitLicenseManager, "implement") as implement,
        patch.object(MitLicenseManager, "save") as save,
    ):
        builder.build()

        download.assert_called_once()
        implement.assert_called_once_with(fullname=blueprint.author.name)
        save.assert_called_once_with(blueprint.folder)

import shutil
from pathlib import Path
from typing import Self
from unittest.mock import Mock, patch

import pytest

from scaffolding.libs.license import builders


@pytest.fixture(scope="function", name="folder")
def mock_folder():
    try:
        folder = Path("/tmp/test-license")
        assert not folder.exists()
        folder.mkdir(parents=True, exist_ok=True)

        yield folder
    finally:
        shutil.rmtree(folder)


class TheBuilder(builders.LicenseBuilder):
    def implement(self, *args, **kwargs) -> Self:
        return self


def test_license_builder(folder: Path):
    builder = TheBuilder()
    assert builder.endpoint == builders.GITHUB_ENDPOINT
    assert builder.content == ""

    builder.license_key = "mit"
    response = {"body": "content"}
    with patch("httpx.get", return_value=Mock(json=lambda: response)) as mock:
        returned = builder.download()
        assert builder.content == "content"
        assert returned is builder
        mock.assert_called_once_with(
            f"{builders.GITHUB_ENDPOINT}/licenses/mit", timeout=10
        )

    builder.save(folder)
    assert (folder / builders.LICENSE_FILE).exists()
    content = (folder / builders.LICENSE_FILE).read_text(encoding="utf-8")
    assert content == response["body"]


def test_mit_license_builder(folder: Path):
    builder = builders.MITLicenseBuilder()
    assert isinstance(builder, builders.LicenseBuilder)
    assert builder.license_key == "mit"

    builder.content = "prefix [year] [fullname] suffix"
    builder.implement(name="John Doe")
    assert builder.content == "prefix 2024 John Doe suffix"


def test_apache2_license_builder(folder: Path):
    builder = builders.Apache2LicenseBuilder()
    assert isinstance(builder, builders.LicenseBuilder)
    assert builder.license_key == "apache-2.0"


def test_gpl2_license_builder(folder: Path):
    builder = builders.GPL2LicenseBuilder()
    assert isinstance(builder, builders.LicenseBuilder)
    assert builder.license_key == "gpl-2.0"


def test_gpl3_license_builder(folder: Path):
    builder = builders.GPL3LicenseBuilder()
    assert isinstance(builder, builders.LicenseBuilder)
    assert builder.license_key == "gpl-3.0"

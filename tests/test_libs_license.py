import shutil
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from faker import Faker

from scaffolding.libs import license
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


def test_get_license_builder():
    builder = license.get_builder("mit")
    assert builder == builders.MITLicenseBuilder

    builder = license.get_builder("apache")
    assert builder == builders.Apache2LicenseBuilder

    builder = license.get_builder("gpl")
    assert builder == builders.GPL3LicenseBuilder

    with pytest.raises(ValueError):
        license.get_builder("unknown")


def test_license_processor(folder: Path):
    builder = builders.MITLicenseBuilder()
    with (
        patch.object(builder, "download") as download_mock,
        patch.object(builder, "implement") as implement_mock,
        patch.object(builder, "save") as save_mock,
    ):
        # the process method is chainable, so we need to mock the return value
        download_mock.return_value = builder
        implement_mock.return_value = builder
        save_mock.return_value = builder

        # call the method
        license.process(builder, folder, "Sherlock Holmes")

        # assert the mocks were called
        assert download_mock.call_count == 1
        assert implement_mock.call_count == 1
        assert save_mock.call_count == 1

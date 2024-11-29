import shutil
from pathlib import Path
from unittest.mock import Mock, patch

from faker import Faker

from scaffolding.libs.license import create_license_file, get_license, list_licenses

fake = Faker()


def test_list_licenses():
    licenses = [
        {"key": fake.word(), "name": fake.name(), "url": fake.url()},
        {"key": fake.word(), "name": fake.name(), "url": fake.url()},
    ]

    with patch("httpx.get", return_value=Mock(json=lambda: licenses)) as mock_get:
        result = list(list_licenses())
        for index, license in enumerate(licenses):
            assert set(result[index].keys()) == {"key", "url"}
            assert result[index]["key"] == license["key"]
            assert result[index]["url"] == license["url"]
        mock_get.assert_called_once_with("https://api.github.com/licenses", timeout=10)


def test_get_license():
    url = fake.url()
    license = {
        "key": fake.word(),
        "name": fake.name(),
        "implementation": fake.sentence(),
        "body": fake.paragraph(),
    }

    with patch("httpx.get", return_value=Mock(json=lambda: license)) as mock_get:
        result = get_license(url=url)
        assert set(result.keys()) == {"body", "implementation"}
        assert license["implementation"] == result["implementation"]
        assert license["body"] == result["body"]
        mock_get.assert_called_once_with(url, timeout=10)


def test_create_license_file():
    try:
        folder = Path("/tmp/test_repo")
        folder.mkdir(parents=True, exist_ok=True)
        license_file = folder / "LICENSE"

        license = {
            "key": fake.word(),
            "name": fake.name(),
            "implementation": fake.sentence(),
            "body": fake.paragraph(),
        }
        with patch("httpx.get", return_value=Mock(json=lambda: license)) as mock_get:
            create_license_file(license_file, fake.word())
            mock_get.assert_called_once()

        assert license_file.is_file()
        with open(license_file, "r") as fr:
            content = fr.read()
            assert content == license["body"]

    finally:
        shutil.rmtree(folder)

from datetime import date

from scaffolding.core.adapter.license_manager import (
    Apache2LicenseManager,
    GPL2LicenseManager,
    GPL3LicenseManager,
    MitLicenseManager,
)


def test_mit_license():
    license = MitLicenseManager()
    assert license.license_key == "mit"

    license.content = "prefix [year] [fullname] suffix"
    license.implement(fullname="tester")
    assert license.content == f"prefix {date.today().year} tester suffix"


def test_apache2_license():
    license = Apache2LicenseManager()
    assert license.license_key == "apache-2.0"


def test_gpl2_license():
    license = GPL2LicenseManager()
    assert license.license_key == "gpl-2.0"


def test_gpl3_license():
    license = GPL3LicenseManager()
    assert license.license_key == "gpl-3.0"

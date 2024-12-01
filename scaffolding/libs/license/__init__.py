from pathlib import Path

from . import builders


def get_builder(license_key: str) -> builders.LicenseBuilder:
    match license_key.upper():
        case "MIT":
            return builders.MITLicenseBuilder
        case "APACHE-2.0" | "APACHE":
            return builders.Apache2LicenseBuilder
        case "GPL-2.0":
            return builders.GPL2LicenseBuilder
        case "GPL-3.0" | "GPL":
            return builders.GPL3LicenseBuilder
        case _:
            raise ValueError(f"Unsupported license: {license_key}")


def process(
    builder: builders.LicenseBuilder,
    folder: Path,
    name: str = "",
) -> None:
    print(f"Processing license {builder.license_key} to {folder} for {name}")
    builder.download().implement(name).save(folder)

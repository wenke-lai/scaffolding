from pathlib import Path
from unittest.mock import Mock, patch

from scaffolding.core.adapter.package_manager import Uv
from scaffolding.core.adapter.system import System


@patch.object(System, "invoke")
def test_python_uv(mock: Mock, folder: Path):
    uv = Uv()

    result = uv.exists()
    assert isinstance(result, bool)
    mock.assert_called_once_with(["uv", "--version"])

    uv.install()
    install_command = ["curl", "-LsSf", "https://astral.sh/uv/install.sh", "|", "sh"]
    mock.assert_called_with(install_command)

    uv.upgrade()
    upgrade_command = ["uv", "self", "update"]
    mock.assert_called_with(upgrade_command)

    with patch.object(Path, "unlink") as unlink:
        uv.init(folder)
        init_command = ["uv", "init", folder]
        mock.assert_called_with(init_command)
        unlink.assert_called_once()

    packages = {
        "package-1": None,
        "package-2": "*",
        "package-3": "latest",
        "package-4": "@0.1.0",
        "package-5": ">=1.1.1,<2.0.0",
        "package-6": "1.1.1",
    }
    uv.add(packages)
    add_command = [
        "uv",
        "add",
        "package-1",
        "package-2",
        "package-3",
        "package-4" + packages["package-4"],
        "package-5" + packages["package-5"],
        f"package-6>={packages['package-6']}",
    ]
    mock.assert_called_with(add_command)

    uv.add({"package": None}, dev=True)
    add_command = ["uv", "add", "--dev", "package"]
    mock.assert_called_with(add_command)

    uv.remove(["package"])
    remove_command = ["uv", "remove", "package"]
    mock.assert_called_with(remove_command)

    uv.remove(["package"], dev=True)
    remove_command = ["uv", "remove", "--dev", "package"]
    mock.assert_called_with(remove_command)

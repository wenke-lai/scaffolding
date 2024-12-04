import subprocess
from pathlib import Path

import httpx


class System:
    def __init__(self, timeout: int = 30, check: bool = True) -> None:
        self.timeout = timeout
        self.check = check

    def invoke(self, commands, **kwargs) -> subprocess.CompletedProcess:
        return subprocess.run(
            commands, timeout=self.timeout, check=self.check, **kwargs
        )

    def download(self, url: str, path: Path | None = None) -> str:
        response = httpx.get(url, timeout=self.timeout)
        response.raise_for_status()
        if path is not None:
            path.write_bytes(response.content)
        return response.text

import subprocess


class System:
    def __init__(self, timeout: int = 30, check: bool = True) -> None:
        self.timeout = timeout
        self.check = check

    def invoke(self, commands: list[str], **kwargs) -> subprocess.CompletedProcess:
        return subprocess.run(
            commands, timeout=self.timeout, check=self.check, **kwargs
        )

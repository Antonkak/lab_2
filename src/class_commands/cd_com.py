import os
from pathlib import Path
from src.logging.logger import command_logger

class CdCommand:
    """Class for cd command"""

    @command_logger
    def cd(self, path: str):
        """Change the shell working directory."""
        if path == "~":
            new_path = Path.home()
        elif path == "..":
            new_path = Path.cwd().parent
        else:
            new_path = Path(path)

        if not new_path.exists() or not new_path.is_dir():
            raise FileNotFoundError(f"cd: {path}: No such file or directory")

        os.chdir(new_path)

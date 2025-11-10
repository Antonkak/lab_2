import os
import typer #ignore
from pathlib import Path
from typing import List
from src.logging.logger import command_logger

class CatCommand:
    """Class for cat command"""

    @command_logger
    def cat(self, files: List[str]):
        """Concatenate FILE(s) to standard output."""
        for file in files:
            file_path = Path(file)

            if not file_path.exists():
                raise FileNotFoundError(f"cat: {file}: No such file or directory")
            if file_path.is_dir():
                raise IsADirectoryError(f"cat: {file}: Is a directory")
            if not os.access(file_path, os.R_OK):
                raise PermissionError(f"cat: {file}: Permission denied")
            with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    typer.echo(content)

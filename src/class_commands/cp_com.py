import os
import shutil
from pathlib import Path
from typing import List
from src.logging.logger import command_logger

class CpCommand:
    """Class for cp command"""

    @command_logger
    def cp(self, sources: List[str], destination: str, recursive: bool = False):
        """Copy SOURCE to DEST, or multiple SOURCE(s) to DIRECTORY."""

        dest_path = Path(destination)
        source_paths = [Path(src) for src in sources]
        for src in source_paths:
            if not src.exists():
                raise FileNotFoundError(f"cp: {src}: No such file or directory")
        if dest_path.exists() and dest_path.is_dir():
            for src in source_paths:
                self._copy_item(src, dest_path / src.name, recursive)
        elif len(source_paths) == 1:
            src = source_paths[0]
            self._copy_item(src, dest_path, recursive)
        else:
            raise ValueError(f"cp: cannot overwrite non-directory '{destination}' with directory '{source_paths}' is not a directory")

    def _copy_item(self, source: Path, destination: Path, recursive: bool):
        """Copy file/dir"""
        if not self._can_read(source):
            raise PermissionError(f"cp: {source}: Permission denied")
        if not self._can_write(destination.parent):
            raise PermissionError(f"cp: cannot create '{destination}': Permission denied")
        if destination.exists() and not self._can_write(destination):
            raise PermissionError(f"cp: cannot overwrite '{destination}': Permission denied")
        if source == destination:
            raise ValueError("cp: source and destination are the same")
        if destination.is_relative_to(source):
            raise ValueError("cp: cannot copy a directory into itself")
        if source.is_file():
            shutil.copy2(source, destination)
        elif source.is_dir():
            if recursive:
                shutil.copytree(source, destination)
            else:
                raise ValueError(f"cp: -r not specified; omitting directory '{source}'")

    def _can_read(self, path: Path) -> bool:
        """Chek read for file/dir"""
        try:
            return os.access(path, os.R_OK)
        except OSError:
            return False

    def _can_write(self, path: Path) -> bool:
        """Chek write for file/dir"""
        try:
            return os.access(path, os.W_OK)
        except OSError:
            return False

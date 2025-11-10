import os
import shutil
import typer
from pathlib import Path
from src.logging.logger import command_logger

class RmCommand:
    """Class for rm command"""

    @command_logger
    def rm(self, path: str, recursive: bool = False):
        """Delete file/dir"""

        target_path = Path(path)
        if not target_path.exists():
            raise FileNotFoundError(f"rm: {path}: No such file or directory")
        self._check_protected_paths(target_path)
        if target_path.is_file():
            self._remove_file(target_path)
        elif target_path.is_dir():
            self._remove_directory(target_path, recursive)
        else:
            raise ValueError(f"rm: {path}: Invalid file type")

    def _check_protected_paths(self, path: Path):
        """Chek for '/' or '..'"""
        absolute_path = path.resolve()
        if path == Path(absolute_path.root):
            raise PermissionError("rm: cannot remove root directory '/'")
        if absolute_path == Path('..').resolve():
            raise PermissionError("rm: cannot remove parent directory '..'")

    def _remove_file(self, file_path: Path):
        """Delete file"""
        if not self._can_write(file_path):
            raise PermissionError(f"rm: cannot remove '{file_path}': Permission denied")
        if not typer.confirm(f"Remove file '{file_path}'?"):
            typer.echo("Canceled")
            return
        try:
            file_path.unlink()
        except Exception as e:
            raise OSError(f"rm: cannot remove '{file_path}': {str(e)}")

    def _remove_directory(self, dir_path: Path, recursive: bool):
        """Delete dir"""
        if not recursive:
            raise ValueError(f"rm: {dir_path}: is a directory (use -r to remove recursively)")
        if not self._can_write(dir_path):
            raise PermissionError(f"rm: cannot remove '{dir_path}': Permission denied")
        message = f"Delete dir '{dir_path}'?"
        if not typer.confirm(message):
            return
        try:
            shutil.rmtree(dir_path)
        except Exception as e:
            raise OSError(f"rm: cannot remove '{dir_path}': {str(e)}")

    def _can_write(self, path: Path) -> bool:
        """Chek permision for write"""
        try:
            return os.access(path, os.W_OK)
        except OSError:
            return False

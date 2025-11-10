import os
import tarfile
import typer
from pathlib import Path
from typing import Optional
from src.logging.logger import command_logger

class TarCommand:
    """Class for tar command"""

    @command_logger
    def tar(self, folder: str, archive: str):
        """Make TAR archive"""
        folder_path = Path(folder)
        archive_path = Path(archive)
        if not folder_path.exists():
            raise FileNotFoundError(f"tar: {folder}: No such file or directory")
        if not folder_path.is_dir():
            raise NotADirectoryError(f"tar: {folder}: Not a directory")
        if not os.access(folder_path, os.R_OK):
            raise PermissionError(f"tar: {folder}: Permission denied")
        if archive_path.exists():
            if not os.access(archive_path, os.W_OK):
                raise PermissionError(f"tar: {archive}: Permission denied")
            if not typer.confirm(f"Overwrite {archive}?"):
                typer.echo("Canceled")
                return
        if not archive_path.name.endswith(('.tar.gz', '.tgz')):
            archive_path = archive_path.with_suffix('.tar.gz')
        try:
            with tarfile.open(archive_path, 'w:gz') as tar:
                tar.add(folder_path, arcname=folder_path.name)
        except Exception as e:
            if archive_path.exists():
                archive_path.unlink()
            raise OSError(f"tar: failed to create archive: {str(e)}")
    @command_logger
    def untar(self, archive: str, extract_path: Optional[str] = None):
        """Распаковывает TAR.GZ архив"""
        archive_path = Path(archive)
        if not archive_path.exists():
            raise FileNotFoundError(f"untar: {archive}: No such file or directory")
        if not tarfile.is_tarfile(archive_path):
            raise ValueError(f"untar: {archive}: Not a valid TAR archive")
        if extract_path:
            target_path = Path(extract_path)
        else:
            target_path = Path.cwd()
        if not target_path.exists():
            target_path.mkdir(parents=True, exist_ok=True)
        if not os.access(target_path, os.W_OK):
            raise PermissionError(f"untar: {target_path}: Permission denied")
        try:
            with tarfile.open(archive_path, "r:gz") as tar:
                file_list = tar.getnames()
                conflicting_files = []
                for file in file_list:
                    target_file = target_path / file
                    if target_file.exists():
                        conflicting_files.append(file)
                if conflicting_files and not typer.confirm(
                    f"Overwrite {len(conflicting_files)}?"
                ):
                    typer.echo("Cancelsed")
                    return
                tar.extractall(target_path)
        except Exception as e:
            raise OSError(f"untar: failed to extract archive: {str(e)}")

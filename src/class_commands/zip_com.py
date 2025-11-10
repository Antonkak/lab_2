import os
import zipfile
import typer
from pathlib import Path
from typing import Optional
from src.logging.logger import command_logger

class ZipCommand:
    """Class for zip command"""

    @command_logger
    def zip(self, folder: str, archive: str):
        """make ZIP archive"""
        folder_path = Path(folder)
        archive_path = Path(archive)
        if not folder_path.exists():
            raise FileNotFoundError(f"zip: {folder}: No such file or directory")
        if not folder_path.is_dir():
            raise NotADirectoryError(f"zip: {folder}: Not a directory")
        if not os.access(folder_path, os.R_OK):
            raise PermissionError(f"zip: {folder}: Permission denied")
        if not archive_path.suffix.lower() == '.zip':
            archive_path = archive_path.with_suffix('.zip')
        if archive_path.exists():
            if not os.access(archive_path, os.W_OK):
                raise PermissionError(f"zip: {archive}: Permission denied")
            if not typer.confirm(f"Overwrite {archive_path}?"):
                typer.echo("Canceled")
                return
        try:
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        file_path = Path(root) / file
                        try:
                            arcname = file_path.relative_to(folder_path)
                            zipf.write(file_path, arcname)
                        except ValueError:
                            zipf.write(file_path, file_path.name)
            typer.echo(f"ZIP created {archive_path}")
        except Exception as e:
            if archive_path.exists():
                try:
                    archive_path.unlink()
                except Exception:
                    pass
            raise OSError(f"zip: failed to create archive: {str(e)}")
    @command_logger
    def unzip(self, archive: str, extract_path: Optional[str] = None):
        """Unzip zip archive"""
        archive_path = Path(archive)
        if not archive_path.exists():
            raise FileNotFoundError(f"unzip: {archive}: No such file or directory")
        if not zipfile.is_zipfile(archive_path):
            raise ValueError(f"unzip: {archive}: Not a valid ZIP archive")
        if extract_path:
            target_path = Path(extract_path)
        else:
            target_path = Path.cwd()
        if not target_path.exists():
            target_path.mkdir(parents=True, exist_ok=True)
        if not os.access(target_path, os.W_OK):
            raise PermissionError(f"unzip: {target_path}: Permission denied")
        try:
            with zipfile.ZipFile(archive_path, 'r') as zipf:
                file_list = zipf.namelist()
                conflicting_files = []
                for file in file_list:
                    target_file = target_path / file
                    if target_file.exists():
                        conflicting_files.append(file)

                if conflicting_files and not typer.confirm(
                    f"Overwrite {len(conflicting_files)}?"
                ):
                    typer.echo("Canceled")
                    return
                zipf.extractall(target_path)
        except Exception as e:
            raise OSError(f"unzip: failed to extract archive: {str(e)}")

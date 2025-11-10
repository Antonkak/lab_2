import stat
import time
import typer
from pathlib import Path
from typing import Optional
from src.logging.logger import command_logger

class LsCommand:
    """Class for ls command"""

    @staticmethod
    def _format_file_mode(st_mode: int) -> str:
        """Formate permisions to '-rwxr-xr-x'"""
        file_type = 'd' if stat.S_ISDIR(st_mode) else '-'
        permissions = [
            'r' if st_mode & stat.S_IRUSR else '-',
            'w' if st_mode & stat.S_IWUSR else '-',
            'x' if st_mode & stat.S_IXUSR else '-',
            'r' if st_mode & stat.S_IRGRP else '-',
            'w' if st_mode & stat.S_IWGRP else '-',
            'x' if st_mode & stat.S_IXGRP else '-',
            'r' if st_mode & stat.S_IROTH else '-',
            'w' if st_mode & stat.S_IWOTH else '-',
            'x' if st_mode & stat.S_IXOTH else '-',
        ]
        return file_type + ''.join(permissions)

    @staticmethod
    def _format_time(timestamp: float) -> str:
        """Formate like bash ls -l"""
        file_time = time.localtime(timestamp)
        current_time = time.localtime()

        if (current_time.tm_year - file_time.tm_year > 0 or
            current_time.tm_mon - file_time.tm_mon > 6):
            return time.strftime("%b %d  %Y", file_time)
        else:
            return time.strftime("%b %d %H:%M", file_time)

    @command_logger
    def ls(self, path: Optional[str] = None, detailed: bool = False):
        """List information about the FILEs (the current directory by default)."""
        target_path = Path(path) if path else Path.cwd()

        if not target_path.exists():
            raise FileNotFoundError(f"ls: {path}: No such file or directory")
        if not target_path.is_dir():
            typer.echo(path)
            return

        items = list(target_path.iterdir())

        if not detailed:
            for item in items:
                name = item.name
                if item.is_dir():
                    name += "/"
                typer.echo(name)
            return

        file_stats = []
        max_size_len = 0

        for item in items:
            try:
                stat_info = item.stat()

                max_size_len = max(max_size_len, len(str(stat_info.st_size)))

                file_stats.append((item, stat_info))
            except OSError:
                continue


        for item, stat_info in file_stats:
            permissions = self._format_file_mode(stat_info.st_mode)
            size_str = f"{stat_info.st_size:>{max_size_len}}"
            time_str = self._format_time(stat_info.st_mtime)
            name = item.name

            if item.is_dir():
                name += "/"

            line = f"{permissions} {size_str} {time_str} {name}"
            typer.echo(line)

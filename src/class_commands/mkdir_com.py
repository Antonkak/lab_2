import typer
from pathlib import Path
from src.logging.logger import command_logger

class MkdirCommand:
    """Class for mkdir command"""
    @command_logger
    def mkdir(self, directories: list[str]):
        """Create dir"""
        for directory in directories:
            path = Path(directory)
            try:
                if path.exists():
                    if path.is_file():
                        raise FileExistsError(f"mkdir: {directory}: File exists")
                    else:
                        typer.echo(f"mkdir: {directory}: Directory already exists")
                        continue
                path.mkdir(exist_ok=True)
                if not path.parent.exists():
                        raise FileNotFoundError(f"mkdir: {path.parent}: No such file or directory")
            except PermissionError:
                raise PermissionError(f"mkdir: {directory}: Permission denied")
            except Exception as e:
                raise OSError(f"mkdir: {directory}: {str(e)}")

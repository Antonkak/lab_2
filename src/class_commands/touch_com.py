from pathlib import Path
from src.logging.logger import command_logger

class TouchCommand:
    """Class for touch commsnd"""

    @command_logger
    def touch(self, files: list, create_parents: bool = False):
        """Create files"""

        for file_path in files:
            path = Path(file_path)

            try:
                if not path.exists():
                    if create_parents:
                        path.parent.mkdir(parents=True, exist_ok=True)
                    elif not path.parent.exists():
                        raise FileNotFoundError(f"touch: {path.parent}: No such directory")
                    path.touch()
                else:
                    path.touch()
            except PermissionError:
                raise PermissionError(f"touch: {path}: Permission denied")
            except Exception as e:
                raise OSError(f"touch: {path}: {str(e)}")

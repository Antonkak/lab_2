import re
import typer
from pathlib import Path
from src.logging.logger import command_logger

class GrepCommand:
    """Class for grep command"""

    @command_logger
    def grep(self, pattern: str, paths: list[str], recursive: bool = False,
             ignore_case: bool = False, line_number: bool = False):
        """Search patterns in files"""
        flags = re.IGNORECASE if ignore_case else 0
        try:
            regex = re.compile(pattern, flags)
        except re.error as e:
            raise ValueError(f"grep: invalid pattern '{pattern}': {str(e)}")
        found_matches = False
        for path_str in paths:
            path = Path(path_str)
            if not path.exists():
                typer.echo(f"grep: {path}: No such file or directory")
                continue
            if path.is_file():
                try:
                    if self._search_in_file(path, regex, line_number):
                        found_matches = True
                except PermissionError:
                    typer.echo(f"grep: {path}: Permission denied")
                except Exception as e:
                    typer.echo(f"grep: {path}: {str(e)}")
            elif path.is_dir():
                if recursive:
                    try:
                        if self._search_in_directory(path, regex, line_number):
                            found_matches = True
                    except PermissionError:
                        typer.echo(f"grep: {path}: Permission denied")
                else:
                    typer.echo(f"grep: {path}: Is a directory")

        if not found_matches:
            pass

    def _search_in_file(self, file_path: Path, regex: re.Pattern, show_line_number: bool):
        """Search for pattern in file"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line_num, line in enumerate(file, 1):
                line = line.rstrip('\n\r')
                if regex.search(line):
                    if show_line_number:
                        typer.echo(f"{file_path}:{line_num}:", nl=False)
                    else:
                        typer.echo(f"{file_path}:", nl=False)

                    self._print_line(line, regex)

    def _search_in_directory(self, dir_path: Path, regex: re.Pattern, show_line_number: bool) -> bool:
        """Recursion search in dirs"""
        found = False
        try:
            for item in dir_path.iterdir():
                if item.is_file():
                    try:
                        if self._search_in_file(item, regex, show_line_number):
                            found = True
                    except PermissionError:
                        typer.echo(f"grep: {item}: Permission denied")
                elif item.is_dir():
                    if self._search_in_directory(item, regex, show_line_number):
                        found = True
        except PermissionError:
            raise PermissionError(f"grep: {dir_path}: Permission denied")
        return found

    def _print_line(self, line: str, regex: re.Pattern):
        """Print finded line"""
        last_end = 0
        for match in regex.finditer(line):
            if match.start() > last_end:
                typer.echo(line[last_end:match.start()], nl=False)
            typer.secho(match.group(0), fg=typer.colors.RED, bold=True, nl=False)
            last_end = match.end()
        if last_end < len(line):
            typer.echo(line[last_end:])
        else:
            typer.echo()

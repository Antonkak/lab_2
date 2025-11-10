import os
import shutil
import typer
from pathlib import Path
from src.logging.logger import command_logger

class MvCommand:
    """Класс для команды mv - перемещение и переименование файлов и каталогов"""

    @command_logger
    def mv(self, source: str, destination: str):
        """Перемещает или переименовывает файлы и каталоги"""

        source_path = Path(source)
        dest_path = Path(destination)

        # Проверяем существование исходного пути
        if not source_path.exists():
            raise FileNotFoundError(f"mv: {source}: No such file or directory")

        # Проверяем права на чтение исходного файла/директории
        if not self._can_read(source_path):
            raise PermissionError(f"mv: {source}: Permission denied")

        # Если целевой путь - существующая директория, перемещаем в нее
        if dest_path.exists() and dest_path.is_dir():
            final_dest = dest_path / source_path.name
        else:
            final_dest = dest_path

        # Проверяем права на запись в целевую директорию
        if not self._can_write(final_dest.parent):
            raise PermissionError(f"mv: cannot create '{final_dest}': Permission denied")

        # Если целевой файл существует, проверяем права на перезапись
        if final_dest.exists() and not self._can_write(final_dest):
            raise PermissionError(f"mv: cannot overwrite '{final_dest}': Permission denied")

        # Запрещаем перемещение в самого себя
        if source_path == final_dest:
            raise ValueError("mv: source and destination are the same")

        # Запрещаем перемещение родительской директории в дочернюю
        if final_dest.is_relative_to(source_path):
            raise ValueError("mv: cannot move a directory into itself")
        try:
            shutil.move(str(source_path), str(final_dest))
            typer.echo(f"Успешно перемещено: {source} -> {final_dest}")
        except Exception as e:
            raise OSError(f"mv: failed to move '{source}' to '{destination}': {str(e)}")

    def _can_read(self, path: Path) -> bool:
        """Проверяет, можно ли читать файл/директорию"""
        try:
            return os.access(path, os.R_OK)
        except OSError:
            return False

    def _can_write(self, path: Path) -> bool:
        """Проверяет, можно ли писать в директорию/файл"""
        try:
            return os.access(path, os.W_OK)
        except OSError:
            return False

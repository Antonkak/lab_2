import typer
from typing import Optional
from src.class_commands.ls_com import LsCommand
from src.class_commands.cat_com import CatCommand
from src.class_commands.cd_com import CdCommand
from src.class_commands.cp_com import CpCommand
from src.class_commands.mv_com import MvCommand
from src.class_commands.rm_com import RmCommand

app = typer.Typer()

ls_command = LsCommand()
cat_command = CatCommand()
cd_command = CdCommand()
cp_command = CpCommand()
mv_command = MvCommand()
rm_command = RmCommand()

@app.command()
def ls(
    path: Optional[str] = typer.Argument(None),
    detailed: bool = typer.Option(False, "-l", help="Use a long listing format")
):
    """List information about the FILEs (the current directory by default)."""
    ls_command.ls(path, detailed)

@app.command()
def cat(files: list[str] = typer.Argument(...)):
    """Concatenate FILE(s) to standard output."""
    cat_command.cat(files)

@app.command()
def cd(path: str = typer.Argument(...)):
    """Change the shell working directory."""
    cd_command.cd(path)

@app.command()
def cp(
    sources: list[str] = typer.Argument(..., help="Источники для копирования"),
    destination: str = typer.Argument(..., help="Назначение"),
    recursive: bool = typer.Option(False, "-r", help="Рекурсивное копирование каталогов")
):
    """Copy SOURCE to DEST, or multiple SOURCE(s) to DIRECTORY."""
    cp_command.cp(sources, destination, recursive)

@app.command()
def mv(
    source: str = typer.Argument(..., help="Источник для перемещения"),
    destination: str = typer.Argument(..., help="Назначение"),
):
    """Перемещает или переименовывает файлы и каталоги"""
    mv_command.mv(source, destination)

@app.command()
def rm(
    path: str = typer.Argument(..., help="Путь к файлу или каталогу"),
    recursive: bool = typer.Option(False, "-r", help="Рекурсивное удаление каталогов"),
):
    """Удаляет файлы и каталоги"""
    rm_command.rm(path, recursive)

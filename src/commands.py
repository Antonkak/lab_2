import typer
from typing import Optional
from src.class_commands.ls_com import LsCommand
from src.class_commands.cat_com import CatCommand
from src.class_commands.cd_com import CdCommand
from src.class_commands.cp_com import CpCommand
from src.class_commands.mv_com import MvCommand
from src.class_commands.rm_com import RmCommand
from src.class_commands.zip_com import ZipCommand
from src.class_commands.tar_com import TarCommand
from src.class_commands.touch_com import TouchCommand
from src.class_commands.mkdir_com import MkdirCommand
from src.class_commands.grep_com import GrepCommand

app = typer.Typer()

ls_command = LsCommand()
cat_command = CatCommand()
cd_command = CdCommand()
cp_command = CpCommand()
mv_command = MvCommand()
rm_command = RmCommand()
zip_command = ZipCommand()
tar_command = TarCommand()
touch_command = TouchCommand()
mkdir_command = MkdirCommand()
grep_command = GrepCommand()

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
    sources: list[str] = typer.Argument(..., help="file/dir"),
    destination: str = typer.Argument(..., help="Destination"),
    recursive: bool = typer.Option(False, "-r", help="Recursion copy for dirs")
):
    """Copy SOURCE to DEST, or multiple SOURCE(s) to DIRECTORY."""
    cp_command.cp(sources, destination, recursive)

@app.command()
def mv(
    source: str = typer.Argument(..., help="file/dir"),
    destination: str = typer.Argument(..., help="Destonatoin"),
):
    """Moove or rename file/dir"""
    mv_command.mv(source, destination)

@app.command()
def rm(
    path: str = typer.Argument(..., help="path to file/dir"),
    recursive: bool = typer.Option(False, "-r", help="Recursion delet for dirs"),
):
    """Delete file/dir"""
    rm_command.rm(path, recursive)

@app.command()
def zip(
    folder: str = typer.Argument(..., help="Files for ZIP"),
    archive: str = typer.Argument(..., help="ZIP archive")
):
    """ZIP dirs"""
    zip_command.zip(folder, archive)

@app.command()
def unzip(
    archive: str = typer.Argument(..., help="File"),
    extract_path: Optional[str] = typer.Argument(None, help="Destination zip")
):
    """Unzip dirs"""
    zip_command.unzip(archive, extract_path)

@app.command()
def tar(
    folder: str = typer.Argument(..., help="Dir"),
    archive: str = typer.Argument(..., help="name for archive")
):
    """TAR dir"""
    tar_command.tar(folder, archive)

@app.command()
def untar(
    archive: str = typer.Argument(..., help="Dir"),
    extract_path: Optional[str] = typer.Argument(None, help="Path to UnTAR")
):
    """UnTAR dir"""
    tar_command.untar(archive, extract_path)

@app.command()
def touch(
    files: list[str] = typer.Argument(..., help="Name file to create"),
):
    """Create files"""
    touch_command.touch(files)

@app.command()
def mkdir(
    directories: list[str] = typer.Argument(..., help="Name dir for create"),
):
    """Create dirs"""
    mkdir_command.mkdir(directories)

@app.command()
def grep(
    pattern: str = typer.Argument(..., help="Pattern for search"),
    paths: list[str] = typer.Argument(..., help="File/dir for searh"),
    recursive: bool = typer.Option(False, "-r", help="Recursion search for dirs"),
    ignore_case: bool = typer.Option(False, "-i", help="Ignore register"),
):
    """Serach lines by pattern"""
    grep_command.grep(pattern, paths, recursive, ignore_case, line_number=True)

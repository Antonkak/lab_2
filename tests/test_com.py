import pytest
from unittest.mock import patch
import sys
import os
from pyfakefs.fake_filesystem_unittest import Patcher

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestLsCommand:
    def test_ls_current_directory(self):
        """Тест ls без аргументов (текущая директория)"""
        with Patcher() as patcher:
            fs = patcher.fs
            fs.create_dir("/test_dir")
            fs.create_file("/test_dir/file1.txt", contents="Content of file1")
            fs.create_file("/test_dir/file2.txt", contents="Content of file2")
            fs.create_dir("/test_dir/subdir")
            fs.create_file("/test_dir/subdir/file3.txt", contents="Content of file3")

            from src.class_commands.ls_com import LsCommand

            os.chdir("/test_dir")

            command = LsCommand()
            with patch('typer.echo') as mock_echo:
                command.ls()

                assert mock_echo.call_count >= 2
                calls = [c[0][0] for c in mock_echo.call_args_list]
                file_names = [str(call) for call in calls]
                assert any("file1.txt" in name for name in file_names)
                assert any("subdir" in name for name in file_names)

    def test_ls_specific_path(self):
        """Тест ls с указанием пути"""
        with Patcher() as patcher:
            fs = patcher.fs
            fs.create_dir("/test_dir")
            fs.create_file("/test_dir/file1.txt", contents="Content of file1")
            fs.create_file("/test_dir/file2.txt", contents="Content of file2")

            from src.class_commands.ls_com import LsCommand

            command = LsCommand()
            with patch('typer.echo') as mock_echo:
                command.ls("/test_dir")

                calls = [c[0][0] for c in mock_echo.call_args_list]
                file_names = [str(call) for call in calls]
                assert any("file1.txt" in name for name in file_names)

    def test_ls_nonexistent_path(self):
        """Тест ls с несуществующим путем"""
        with Patcher():
            from src.class_commands.ls_com import LsCommand

            command = LsCommand()
            with pytest.raises(FileNotFoundError):
                command.ls("/nonexistent_path")
class TestCatCommand:
    def test_cat_single_file(self):
        """Тест cat с одним файлом"""
        with Patcher() as patcher:
            fs = patcher.fs
            fs.create_file("/test.txt", contents="Content of file")
            from src.class_commands.cat_com import CatCommand
            command = CatCommand()
            with patch('typer.echo') as mock_echo:
                command.cat(["/test.txt"])
                mock_echo.assert_called_once_with("Content of file")
    def test_cat_multiple_files(self):
        """Тест cat с несколькими файлами"""
        with Patcher() as patcher:
            fs = patcher.fs
            fs.create_file("/file1.txt", contents="Content 1")
            fs.create_file("/file2.txt", contents="Content 2")
            from src.class_commands.cat_com import CatCommand
            command = CatCommand()
            with patch('typer.echo') as mock_echo:
                command.cat(["/file1.txt", "/file2.txt"])

                assert mock_echo.call_count == 2
                calls = [c[0][0] for c in mock_echo.call_args_list]
                assert "Content 1" in calls
                assert "Content 2" in calls
    def test_cat_nonexistent_file(self):
        """Тест cat с несуществующим файлом"""
        with Patcher():
            from src.class_commands.cat_com import CatCommand
            command = CatCommand()
            with pytest.raises(FileNotFoundError):
                command.cat(["/nonexistent.txt"])
class TestCpCommand:
    def test_cp_file_to_directory(self):
        """Тест копирования файла в директорию"""
        with Patcher() as patcher:
            fs = patcher.fs
            fs.create_file("/file.txt", contents="File content")
            fs.create_dir("/target_dir")
            from src.class_commands.cp_com import CpCommand
            command = CpCommand()
            command.cp(["/file.txt"], "/target_dir/")
            assert fs.exists("/target_dir/file.txt")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
class TestRmCommand:
    def test_rm_directory_without_recursive(self):
        """Тест удаления директории без -r"""
        with Patcher() as patcher:
            fs = patcher.fs
            fs.create_dir("/dir")
            fs.create_file("/dir/file.txt", contents="Content")
            from src.class_commands.rm_com import RmCommand
            command = RmCommand()
            with pytest.raises(ValueError, match="is a directory"):
                command.rm("/dir")

    def test_rm_nonexistent_file(self):
        """Тест удаления несуществующего файла"""
        with Patcher():
            from src.class_commands.rm_com import RmCommand
            command = RmCommand()
            with pytest.raises(FileNotFoundError):
                command.rm("/nonexistent.txt")

    def test_rm_protected_paths(self):
        """Тест защиты системных путей"""
        with Patcher():
            from src.class_commands.rm_com import RmCommand
            command = RmCommand()
            with pytest.raises(PermissionError):
                command.rm("/", recursive=True)

    def test_rm_cancel_confirmation(self):
        """Тест отмены удаления при неподтверждении"""
        with Patcher() as patcher:
            fs = patcher.fs
            fs.create_file("/file.txt", contents="Content")

            from src.class_commands.rm_com  import RmCommand

            command = RmCommand()
            with patch('typer.confirm') as mock_confirm, patch('typer.echo') as mock_echo:
                mock_confirm.return_value = False
                command.rm("/file.txt")
                assert fs.exists("/file.txt")
                mock_echo.assert_called_with("Операция отменена")

    def test_rm_multiple_files_in_directory(self):
        """Тест удаления директории с несколькими файлами"""
        with Patcher() as patcher:
            fs = patcher.fs
            fs.create_dir("/project")
            for i in range(5):
                fs.create_file(f"/project/file{i}.txt", contents=f"Content {i}")
            fs.create_dir("/project/src")
            fs.create_file("/project/src/main.py", contents="print('hello')")
            from src.class_commands.rm_com import RmCommand
            command = RmCommand()
            with patch('typer.confirm') as mock_confirm:
                mock_confirm.return_value = True
                command.rm("/project", recursive=True)
                assert not fs.exists("/project")
                assert not fs.exists("/project/src/main.py")

class TestZipCommand:
    def test_zip_create_archive(self):
        """Тест создания ZIP архива"""
        with Patcher() as patcher:
            fs = patcher.fs
            fs.create_dir("/test_folder")
            fs.create_file("/test_folder/file1.txt", contents="Content 1")
            fs.create_file("/test_folder/file2.txt", contents="Content 2")
            fs.create_dir("/test_folder/subdir")
            fs.create_file("/test_folder/subdir/file3.txt", contents="Content 3")
            from src.class_commands.zip_com import ZipCommand
            command = ZipCommand()
            with patch('typer.echo'):
                command.zip("/test_folder", "/test.zip")
                assert fs.exists("/test.zip")
    def test_zip_nonexistent_folder(self):
        """Тест создания архива из несуществующей папки"""
        with Patcher():
            from src.class_commands.zip_com import ZipCommand
            command = ZipCommand()
            with pytest.raises(FileNotFoundError):
                command.zip("/nonexistent", "/test.zip")
    def test_unzip_archive(self):
        """Тест распаковки ZIP архива"""
        with Patcher() as patcher:
            fs = patcher.fs
            import zipfile
            from io import BytesIO
            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w') as zipf:
                zipf.writestr('file1.txt', 'Content 1')
                zipf.writestr('file2.txt', 'Content 2')
            fs.create_file("/test.zip", contents=zip_buffer.getvalue())
            from src.class_commands.zip_com import ZipCommand
            command = ZipCommand()
            with patch('typer.echo'):
                command.unzip("/test.zip", "/extract_dir")
                assert fs.exists("/extract_dir/file1.txt")
                assert fs.exists("/extract_dir/file2.txt")

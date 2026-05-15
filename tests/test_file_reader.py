import os
import tempfile
import pytest
from tools.file_reader import list_files, read_file


@pytest.fixture
def sample_project(tmp_path):
    (tmp_path / "main.py").write_text("print('hello')")
    (tmp_path / "utils.py").write_text("def add(a, b): return a + b")
    (tmp_path / "requirements.txt").write_text("requests==2.31.0")
    subdir = tmp_path / "subpackage"
    subdir.mkdir()
    (subdir / "module.py").write_text("x = 1")
    return tmp_path


def test_list_files_returns_python_files(sample_project):
    result = list_files(str(sample_project))
    assert "error" not in result
    files = result["files"]
    assert any("main.py" in f for f in files)
    assert any("utils.py" in f for f in files)


def test_list_files_returns_requirements(sample_project):
    result = list_files(str(sample_project))
    assert any("requirements.txt" in f for f in result["files"])


def test_list_files_includes_subdirectories(sample_project):
    result = list_files(str(sample_project))
    assert any("module.py" in f for f in result["files"])


def test_list_files_invalid_path():
    result = list_files("/nonexistent/path")
    assert "error" in result


def test_read_file_returns_content(sample_project):
    result = read_file(str(sample_project), "main.py")
    assert "error" not in result
    assert "print('hello')" in result["content"]


def test_read_file_invalid_file(sample_project):
    result = read_file(str(sample_project), "doesnotexist.py")
    assert "error" in result

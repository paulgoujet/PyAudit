import pytest
from tools.code_quality import analyse_quality


@pytest.fixture
def project_with_clean_code(tmp_path):
    (tmp_path / "clean.py").write_text(
        "def add(a, b):\n    return a + b\n"
    )
    return tmp_path


@pytest.fixture
def project_with_issues(tmp_path):
    (tmp_path / "bad.py").write_text(
        "def foo():\n    return undefined_variable\n"
    )
    return tmp_path


@pytest.fixture
def empty_project(tmp_path):
    return tmp_path


def test_analyse_quality_returns_result(project_with_clean_code):
    result = analyse_quality(str(project_with_clean_code))
    assert "error" not in result
    assert "files" in result
    assert "total_issues" in result


def test_analyse_quality_detects_issues(project_with_issues):
    result = analyse_quality(str(project_with_issues))
    assert "error" not in result
    assert result["total_issues"] > 0


def test_analyse_quality_no_python_files(empty_project):
    result = analyse_quality(str(empty_project))
    assert "error" in result

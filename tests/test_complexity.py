import pytest
from tools.complexity import analyse_complexity


@pytest.fixture
def project_with_functions(tmp_path):
    (tmp_path / "module.py").write_text(
        "def simple(x):\n    return x + 1\n\n"
        "def branchy(x):\n    if x > 0:\n        return x\n"
        "    elif x == 0:\n        return 0\n"
        "    else:\n        return -x\n"
    )
    return tmp_path


@pytest.fixture
def empty_project(tmp_path):
    return tmp_path


def test_analyse_complexity_returns_result(project_with_functions):
    result = analyse_complexity(str(project_with_functions))
    assert "error" not in result
    assert "files" in result


def test_analyse_complexity_contains_functions(project_with_functions):
    result = analyse_complexity(str(project_with_functions))
    files = result["files"]
    assert len(files) > 0
    for path, blocks in files.items():
        for block in blocks:
            assert "name" in block
            assert "complexity" in block
            assert "rank" in block


def test_analyse_complexity_no_python_files(empty_project):
    result = analyse_complexity(str(empty_project))
    assert "error" in result

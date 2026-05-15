import subprocess
import os
import sys
import json


def analyse_quality(project_path: str) -> dict:
    """Run pylint on all Python files in the project and return the results."""
    python_files = []
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in {"__pycache__", ".git", ".venv", "venv"}]
        for filename in files:
            if filename.endswith(".py"):
                python_files.append(os.path.join(root, filename))

    if not python_files:
        return {"error": "No Python files found in the project."}

    try:
        result = subprocess.run(
            [sys.executable, "-m", "pylint", "--output-format=json", "--score=no"] + python_files,
            capture_output=True,
            text=True,
            timeout=60
        )
        issues = json.loads(result.stdout) if result.stdout.strip() else []

        by_file = {}
        for issue in issues:
            rel_path = os.path.relpath(issue["path"], project_path)
            by_file.setdefault(rel_path, []).append({
                "line": issue["line"],
                "type": issue["type"],
                "message": issue["message"],
                "symbol": issue["symbol"]
            })

        return {"files": by_file, "total_issues": len(issues)}
    except Exception as e:
        return {"error": str(e)}

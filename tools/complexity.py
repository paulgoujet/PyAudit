import subprocess
import os
import json


def analyse_complexity(project_path: str) -> dict:
    """Run radon cc on all Python files and return cyclomatic complexity results."""
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
            ["radon", "cc", "--json", "-s"] + python_files,
            capture_output=True,
            text=True,
            timeout=60
        )
        data = json.loads(result.stdout) if result.stdout.strip() else {}

        formatted = {}
        for filepath, blocks in data.items():
            rel_path = os.path.relpath(filepath, project_path)
            formatted[rel_path] = [
                {
                    "name": block["name"],
                    "complexity": block["complexity"],
                    "rank": block["rank"]
                }
                for block in blocks
            ]

        return {"files": formatted}
    except Exception as e:
        return {"error": str(e)}

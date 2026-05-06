import os


def list_files(project_path: str) -> dict:
    """Return the directory tree and list of Python/config files in the project."""
    result = {"project_path": project_path, "files": []}

    if not os.path.isdir(project_path):
        return {"error": f"Path not found: {project_path}"}

    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in {"__pycache__", ".git", ".venv", "venv", "node_modules"}]
        for filename in files:
            if filename.endswith((".py", ".txt", ".toml", ".cfg", ".ini", ".md")):
                full_path = os.path.join(root, filename)
                rel_path = os.path.relpath(full_path, project_path)
                result["files"].append(rel_path)

    return result


def read_file(project_path: str, relative_path: str) -> dict:
    """Read and return the content of a file inside the project."""
    full_path = os.path.join(project_path, relative_path)

    if not os.path.isfile(full_path):
        return {"error": f"File not found: {relative_path}"}

    try:
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"path": relative_path, "content": content}
    except Exception as e:
        return {"error": str(e)}

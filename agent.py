import anthropic
from tools.file_reader import list_files, read_file
from tools.vulnerability import check_vulnerabilities
from tools.code_quality import analyse_quality
from tools.complexity import analyse_complexity

MODEL = "claude-sonnet-4-6"

TOOLS = [
    {
        "name": "list_files",
        "description": "List all relevant files in the project directory (Python files, config files, requirements).",
        "input_schema": {
            "type": "object",
            "properties": {
                "project_path": {
                    "type": "string",
                    "description": "Absolute path to the project directory."
                }
            },
            "required": ["project_path"]
        }
    },
    {
        "name": "read_file",
        "description": "Read the content of a specific file inside the project.",
        "input_schema": {
            "type": "object",
            "properties": {
                "project_path": {
                    "type": "string",
                    "description": "Absolute path to the project directory."
                },
                "relative_path": {
                    "type": "string",
                    "description": "Relative path to the file inside the project."
                }
            },
            "required": ["project_path", "relative_path"]
        }
    },
    {
        "name": "check_vulnerabilities",
        "description": "Check the project dependencies in requirements.txt for known security vulnerabilities using the OSV API.",
        "input_schema": {
            "type": "object",
            "properties": {
                "project_path": {
                    "type": "string",
                    "description": "Absolute path to the project directory."
                }
            },
            "required": ["project_path"]
        }
    },
    {
        "name": "analyse_quality",
        "description": "Run pylint on all Python files in the project and return code quality issues.",
        "input_schema": {
            "type": "object",
            "properties": {
                "project_path": {
                    "type": "string",
                    "description": "Absolute path to the project directory."
                }
            },
            "required": ["project_path"]
        }
    },
    {
        "name": "analyse_complexity",
        "description": "Run radon on all Python files to measure cyclomatic complexity.",
        "input_schema": {
            "type": "object",
            "properties": {
                "project_path": {
                    "type": "string",
                    "description": "Absolute path to the project directory."
                }
            },
            "required": ["project_path"]
        }
    }
]

SYSTEM_PROMPT = """You are PyAudit, an AI assistant that audits Python projects.

When given a project path, you must:
1. List the project files to understand its structure.
2. Check dependencies for known security vulnerabilities.
3. Analyse code quality with pylint.
4. Analyse code complexity with radon.
5. Produce a clear, structured audit report in the terminal.

Use the available tools to gather all necessary information before writing the report.
Be concise and actionable in your recommendations."""


def run_tool(name: str, inputs: dict) -> str:
    """Dispatch a tool call to the correct function and return the result as a string."""
    import json

    if name == "list_files":
        result = list_files(inputs["project_path"])
    elif name == "read_file":
        result = read_file(inputs["project_path"], inputs["relative_path"])
    elif name == "check_vulnerabilities":
        result = check_vulnerabilities(inputs["project_path"])
    elif name == "analyse_quality":
        result = analyse_quality(inputs["project_path"])
    elif name == "analyse_complexity":
        result = analyse_complexity(inputs["project_path"])
    else:
        result = {"error": f"Unknown tool: {name}"}

    return json.dumps(result, indent=2)


def run_agent(project_path: str, api_key: str) -> None:
    """Run the PyAudit agent on the given project path."""
    client = anthropic.Anthropic(api_key=api_key)

    messages = [
        {
            "role": "user",
            "content": f"Please audit the Python project located at: {project_path}"
        }
    ]

    print("Running PyAudit...\n")

    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages
        )

        # Collect any text output from this turn
        for block in response.content:
            if hasattr(block, "text"):
                print(block.text)

        # Stop if Claude is done
        if response.stop_reason == "end_turn":
            break

        # Handle tool calls
        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})

            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"  > Calling tool: {block.name}...")
                    output = run_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": output
                    })

            messages.append({"role": "user", "content": tool_results})
        else:
            break

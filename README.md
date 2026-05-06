# PyAudit

An AI-powered command-line assistant that automatically audits Python projects using the Claude API (Anthropic).

## Description

PyAudit is a command-line AI assistant that automatically audits Python projects. The user provides a project directory path, and the system analyses its structure, code quality, dependency vulnerabilities, and cyclomatic complexity. The agent then generates a structured report with prioritised recommendations directly in the terminal.

The system is built around an agentic loop: Claude receives the user request, autonomously decides which tools to call and in which order, interprets the results, and produces a final report without any hardcoded execution sequence.

## AI and Agent-based Approach

The system uses the tool use pattern provided by the Claude API. The agent is given a set of tools and a system prompt. Claude acts as the reasoning core: it decides which tools to call, in which order, and how to interpret their results before producing the final report. The execution flow is driven by the model, not by a fixed script.

The agentic loop in `agent.py` works as follows:
1. The user request is sent to Claude along with the list of available tools.
2. Claude responds with one or more tool calls.
3. Each tool is executed locally and its result is returned to Claude.
4. Claude continues calling tools until it has enough information.
5. Claude produces the final audit report.

## Tools

| Tool | File | Description |
|------|------|-------------|
| list_files | tools/file_reader.py | Walks the project directory and returns all relevant file paths |
| read_file | tools/file_reader.py | Reads the content of a specific file inside the project |
| check_vulnerabilities | tools/vulnerability.py | Queries the OSV API for each dependency in requirements.txt |
| analyse_quality | tools/code_quality.py | Runs pylint on all Python files and returns structured issue data |
| analyse_complexity | tools/complexity.py | Runs radon cc to measure cyclomatic complexity per function |

## Programming Concepts Applied

- **LLM tool use / function calling** - The Claude API tool use feature is used in `agent.py` to let the model call Python functions during its reasoning process. Tool schemas are defined as JSON and passed to the API on each request.

- **Agentic loop** - `agent.py` implements a while loop that continues sending messages to Claude until the stop reason is `end_turn`, allowing multi-step autonomous reasoning.

- **HTTP requests** - `tools/vulnerability.py` sends POST requests to the OSV REST API using the `requests` library to retrieve vulnerability records per package.

- **Subprocess management** - `tools/code_quality.py` and `tools/complexity.py` launch pylint and radon as subprocesses using `subprocess.run` and capture their JSON output.

- **File I/O and directory traversal** - `tools/file_reader.py` uses `os.walk` to explore the project tree and built-in file reading to return source content to the agent.

- **JSON parsing and data transformation** - Tool outputs from external processes and APIs are parsed from JSON and restructured into a consistent format before being returned to the agent.

- **CLI argument parsing** - `main.py` uses `argparse` to handle the `--project` argument.

- **Environment variable management** - `python-dotenv` is used to load the API key from a `.env` file at startup.

- **Unit testing with pytest** - Tests are located in the `tests/` directory and cover each tool individually.

## Project Structure

```
PyAudit/
├── main.py              # Entry point - CLI parsing and startup
├── agent.py             # Claude API agentic loop and tool dispatch
├── tools/
│   ├── __init__.py
│   ├── file_reader.py   # list_files and read_file tools
│   ├── vulnerability.py # OSV API vulnerability checker
│   ├── code_quality.py  # pylint wrapper
│   └── complexity.py    # radon wrapper
├── tests/               # pytest test suite
├── .env.example         # API key configuration template
├── requirements.txt     # Python dependencies
└── README.md
```

## Installation

```bash
git clone https://github.com/paulgoujet/PyAudit.git
cd PyAudit
pip install -r requirements.txt
```

## Configuration

Copy `.env.example` to `.env` and add your Anthropic API key:

```bash
cp .env.example .env
```

Then edit `.env`:

```
ANTHROPIC_API_KEY=your_api_key_here
```

## Usage

```bash
python main.py --project ./path/to/your/python/project
```

## Requirements

- Python 3.10+
- An Anthropic API key

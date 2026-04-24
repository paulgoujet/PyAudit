# PyAudit

## Description

PyAudit is a command-line AI assistant that automatically audits Python projects. The user provides a project directory, and the system analyses its code quality, dependency vulnerabilities, and complexity, then generates a structured report with prioritised recommendations. The goal is to help developers quickly identify security and quality issues in their codebase without running multiple tools manually.

## AI and Agent-based Approach

The system uses an agentic approach built on the Claude API (Anthropic). Claude acts as the reasoning core of the system: given the user's request, it autonomously decides which tools to call, in which order, and how to interpret the results. This follows the tool use pattern where the LLM drives the execution flow rather than following a fixed script.

## Tools

- **File reader** - Explores the project structure and reads source files
- **Vulnerability checker** - Queries the OSV API to detect known vulnerabilities in dependencies
- **Code quality analyser** - Runs pylint on Python source files
- **Complexity analyser** - Runs radon to measure code complexity

## Programming Concepts

- LLM tool use / function calling (Claude API)
- HTTP requests (OSV API)
- Subprocess management (pylint, radon)
- File I/O and directory traversal
- JSON parsing and data transformation
- CLI argument parsing
- Unit testing with pytest
- Project packaging (requirements.txt)

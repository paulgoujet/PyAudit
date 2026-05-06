import argparse
import os
import sys
from dotenv import load_dotenv
from agent import run_agent


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="PyAudit - AI-powered Python project auditor"
    )
    parser.add_argument(
        "--project",
        required=True,
        help="Path to the Python project directory to audit"
    )
    args = parser.parse_args()

    project_path = os.path.abspath(args.project)
    if not os.path.isdir(project_path):
        print(f"Error: '{project_path}' is not a valid directory.")
        sys.exit(1)

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY is not set. Please check your .env file.")
        sys.exit(1)

    run_agent(project_path, api_key)


if __name__ == "__main__":
    main()

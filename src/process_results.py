import json
import os
import sys
from typing import TypedDict
from github import Github, Auth


class Failure(TypedDict):
    check_name: str
    guideline: str
    resource: str
    filepath: str
    code: str
    start_line: int
    end_line: int
    tool: str


# using an access token
auth = Auth.Token("access_token")


def create_annotation(file_path, start_line, end_line, title, message, level="warning",):
    """Create a GitHub annotation with the given parameters."""
    print(
        f"::{level} file={file_path},"
        f"line={start_line},endLine={end_line},title={title}::{message}"
    )


def process_checkov_results(results_file, github_token, hostname):
    print(f"Processing Checkov results from {results_file}")
    print(f"Using GitHub host: {hostname}")

    g = Github(github_token, base_url=f"https://{hostname}/api/v3")

    try:
        with open(results_file, 'r') as f:
            results = json.load(f)
    except FileNotFoundError:
        print(f"Error: Results file '{results_file}' not found")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in results file: {e}")
        with open(results_file, 'r') as f:
            print("File contents:")
            print(f.read())
        sys.exit(1)
    except Exception as e:
        print(f"Error reading results file: {e}")
        sys.exit(1)

    if isinstance(results, dict):
        results = [results]

    failures: list[Failure] = [
        {
            'check_name': c.get('check_name'),
            'guideline': c.get('guideline'),
            'resource': c.get('resource'),
            'filepath': c.get('repo_file_path', c.get('file_path')),
            'code': ''.join([c for n, c in c.get('code_block', [])]),
            'start_line': c.get('file_line_range')[0],
            'end_line': c.get('file_line_range')[1],
            'tool': 'checkov',
        }
        for framework in results
        for c in framework.get('results', {}).get('failed_checks', [])
    ]

    for failure in failures:
        file_path = failure.get('filepath', '')
        start_line = failure.get('start_line', 1)
        end_line = failure.get('end_line', 1)
        create_annotation(
            file_path=file_path,
            start_line=start_line,
            end_line=end_line,
            title=failure.get('check_name', ''),
            message=f"{failure.get('guideline', '')}",
        )

        # Also print to console for visibility
        print(f"Created annotation in {file_path}:{start_line}-{end_line}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: process_results.py <github_token> <github_hostname>")
        sys.exit(1)
    github_token = sys.argv[1]
    github_hostname = sys.argv[2]
    process_checkov_results(
        'checkov_output.json',
        github_token,
        github_hostname,
    )

import json
import os
import sys
from typing import TypedDict
from github import Auth


class Failure(TypedDict):
    check_name: str
    guideline: str
    resource: str
    filepath: str
    code: str
    start_line: int
    end_line: int
    tool: str


GITHUB_HOSTNAME = (
    os.environ.get("GITHUB_SERVER_URL", "github.com")
    .replace("https://", "")
    .replace("http://", "")
)

GITHUB_TOKEN = os.environ.get("INPUT_GITHUB_TOKEN")
if not GITHUB_TOKEN:
    msg = "github_token must be set"
    raise ValueError(msg)
auth = Auth.Token(GITHUB_TOKEN)


def create_annotation(
    file_path: str,
    start_line: int,
    end_line: int,
    title: str,
    message: str,
    level: str = "warning",
):
    """Create a GitHub annotation with the given parameters."""
    print(
        f"::{level} file={file_path},"
        f"line={start_line},endLine={end_line},title={title}::{message}"
    )


def process_checkov_results(checkov_filename, tfsec_filename):
    # region Checkov findings
    print(f"Processing checkov findings.")
    checkov_results = _read_results_file(checkov_filename)
    if isinstance(checkov_results, dict):
        checkov_results = [checkov_results]
    checkov_failures: list[Failure] = [
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
        for framework in checkov_results
        for c in framework.get('results', {}).get('failed_checks', [])
    ]
    # endregion

    # region tfsec findings
    print(f"Processing tfsec findings.")
    tfsec_results: dict = _read_results_file(tfsec_filename)
    tfsec_failures: list[Failure] = [
        {
            'check_name': c.get('rule_description'),
            'guideline': (
                f"[{c.get('severity')}] "
                f"{c.get('resolution')}: {c.get('links')[0]}"
            ),
            'resource': c.get('resource'),
            'filepath': c.get('location', {}).get('filename', ''),
            'code': '',
            'start_line': c.get('location', {}).get('start_line', 1),
            'end_line': c.get('location', {}).get('end_line', 1),
            'tool': 'tfsec',
        }
        for c in tfsec_results.get("results", [])
    ]
    failures = checkov_failures + tfsec_failures

    for failure in failures:
        file_path = failure.get('filepath', '')
        start_line = failure.get('start_line', 1)
        end_line = failure.get('end_line', 1)
        create_annotation(
            file_path=file_path,
            start_line=start_line,
            end_line=end_line,
            title=f"{failure.get('resource', '')}: {failure.get('check_name', '')}",
            message=(
                f"Tool: {failure.get('tool', '')} - "
                f"Guideline: {failure.get('guideline', '')}"
            ),
        )

        # Also print to console for visibility
        print(f"Created annotation in {file_path}:{start_line}-{end_line}")

def _read_results_file(filename: str):
    try:
        with open(filename, 'r') as f:
            results = json.load(f)
        return results
    except FileNotFoundError:
        print(f"Error: Results file '{filename}' not found")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in results file: {e}")
        with open(filename, 'r') as f:
            print("File contents:")
            print(f.read())
        sys.exit(1)
    except Exception as e:
        print(f"Error reading results file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    process_checkov_results(
        'checkov_output.json',
        'tfsec_output.json',
    )

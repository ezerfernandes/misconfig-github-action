import json
import os
import sys


def create_annotation(file_path, line_number, message, level="error"):
    """Create a GitHub annotation with the given parameters."""
    print(f"::{level} file={file_path},line={line_number}::{message}")


def process_checkov_results(results_file):
    print(f"Processing Checkov results from {results_file}")
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

    failed_checks = []
    for result in results:
        failed_checks.extend(result.get('results', {}).get('failed_checks', []))
    print(f"Found {len(failed_checks)} failed checks")

    # Process failed checks
    for check_type in failed_checks:
        file_path = check_type.get('file_path', '')
        line_number = check_type.get('file_line_range', [1])[0]
        check_id = check_type.get('check_id', '')
        check_name = check_type.get('check_name', '')

        message = f"[{check_id}] {check_name}"
        create_annotation(file_path, line_number, message)

        # Also print to console for visibility
        print(f"Created annotation for {check_id} in {file_path}:{line_number}")

if __name__ == "__main__":
    process_checkov_results('checkov_output.json')
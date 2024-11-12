import json
import os
import sys

def create_annotation(file_path, line_number, message, level="error"):
    print(f"::{level} file={file_path},line={line_number}::{message}")

def process_checkov_results(results_file):
    try:
        with open(results_file, 'r') as f:
            results = json.load(f)
    except Exception as e:
        print(f"Error reading results file: {e}")
        sys.exit(1)

    # Process failed checks
    for check_type in results.get('results', {}).get('failed_checks', []):
        file_path = check_type.get('file_path', '')
        line_number = check_type.get('file_line_range', [1])[0]
        check_id = check_type.get('check_id', '')
        check_name = check_type.get('check_name', '')

        message = f"[{check_id}] {check_name}"
        create_annotation(file_path, line_number, message)

if __name__ == "__main__":
    process_checkov_results('checkov_output.json')
#!/bin/bash
set -e

# region Get inputs with defaults
PATH_TO_SCAN="${INPUT_PATH:-.}"
FRAMEWORKS="${INPUT_FRAMEWORK:-terraform,terraform_plan}"
SKIP_CHECKS="${INPUT_SKIP_CHECK:-}"
CHECKS="${INPUT_CHECK:-}"

echo "Starting misconfiguration scan..."
echo "Path to scan: $PATH_TO_SCAN"
echo "Frameworks: $FRAMEWORKS"
echo "Skip checks: $SKIP_CHECKS"
echo "Specific checks: $CHECKS"

# region Prepare parameters
FRAMEWORK_PARAM=""
if [ ! -z "$FRAMEWORKS" ]; then
    FRAMEWORK_PARAM="--framework ${FRAMEWORKS}"
fi

SKIP_CHECK_PARAM=""
if [ ! -z "$SKIP_CHECKS" ]; then
    SKIP_CHECK_PARAM="--skip-check ${SKIP_CHECKS}"
fi

CHECK_PARAM=""
if [ ! -z "$CHECKS" ]; then
    CHECK_PARAM="--check ${CHECKS}"
fi
# endregion

# region Run checkov and create GitHub annotations
echo "Running Checkov with parameters:"
echo "checkov -d \"$PATH_TO_SCAN\" $FRAMEWORK_PARAM $SKIP_CHECK_PARAM $CHECK_PARAM -o json"

# Run checkov and capture both stdout and stderr
if ! checkov -d "$PATH_TO_SCAN" $FRAMEWORK_PARAM $SKIP_CHECK_PARAM $CHECK_PARAM -o json > checkov_output.json 2>checkov_error.txt; then
    echo "Checkov completed with findings"
    cat checkov_error.txt
fi

# Check if output file exists and has content
if [ ! -s checkov_output.json ]; then
    echo "Error: No output generated by Checkov"
    if [ -f checkov_error.txt ]; then
        echo "Error output:"
        cat checkov_error.txt
    fi
    exit 1
fi

echo "Processing results..."
python process_results.py

# Print summary of findings
echo "Scan complete. See annotations in PR for details."
# endregion
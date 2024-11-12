#!/bin/bash
set -e

# region Get inputs with defaults
PATH_TO_SCAN="${1:-.}"
FRAMEWORKS="${2:-terraform}"
SKIP_CHECKS="${3:-''}"
CHECKS="${4:-''}"
# endregion

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
checkov -d "$PATH_TO_SCAN" $FRAMEWORK_PARAM $SKIP_CHECK_PARAM $CHECK_PARAM -o json > checkov_output.json

python /process_results.py
# endregion
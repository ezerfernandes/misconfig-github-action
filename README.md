# misconfig-github-action

GitHub Action for scanning Infrastructure as Code files for misconfigurations using Checkov. This action will scan your files and create annotations in your PR for any findings.

## Usage

```yaml
name: Check for misconfigurations

on: [pull_request]

jobs:
  check-misconfigurations:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Scan for misconfigurations
        uses: ezerfernandes/misconfig-github-action@v1
        with:
          path: ./terraform
          framework: terraform,helm
          skip_check: CKV_AWS_123,CKV_AWS_124
          check: CKV_AWS_125,CKV_AWS_126
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| path | Path to scan | No | ./terraform |
| framework | Frameworks to scan (comma-separated) | No | terraform |
| skip_check | Checks to skip (comma-separated) | No | |
| check | Specific checks to run (comma-separated) | No | |

## Outputs

The action will create annotations in your PR for any misconfigurations found. These will appear directly in the "Files changed" tab of your PR.

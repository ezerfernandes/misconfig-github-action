FROM python:3.12-slim

LABEL "com.github.actions.name"="Misconfiguration Scanner"
LABEL "com.github.actions.description"="Scan for misconfigurations in Terraform code"
LABEL "com.github.actions.icon"="code"
LABEL "com.github.actions.color"="yellow"

LABEL "repository"="https://github.com/ezerfernandes/misconfig-github-action"
LABEL "homepage"="https://github.com/ezerfernandes/misconfig-github-action"
LABEL "maintainer"="Ezer Silva <ezersilva@gmail.com>"

RUN pip install checkov

COPY ./src/entrypoint.sh /entrypoint.sh
COPY ./src/process_results.py /process_results.py

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
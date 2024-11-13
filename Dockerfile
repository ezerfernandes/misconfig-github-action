FROM python:3.12-slim

LABEL "com.github.actions.name"="Misconfiguration Scanner"
LABEL "com.github.actions.description"="Scan for misconfigurations in Terraform code"
LABEL "com.github.actions.icon"="code"
LABEL "com.github.actions.color"="yellow"

LABEL "repository"="https://github.com/ezerfernandes/misconfig-github-action"
LABEL "homepage"="https://github.com/ezerfernandes/misconfig-github-action"
LABEL "maintainer"="Ezer Silva <ezersilva@gmail.com>"

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN curl -s https://raw.githubusercontent.com/aquasecurity/tfsec/master/scripts/install_linux.sh | bash

COPY ./src/entrypoint.sh /entrypoint.sh
COPY ./src/process_results.py /process_results.py
COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
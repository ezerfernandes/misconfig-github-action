FROM python:3.12-slim

LABEL "com.github.actions.name"="Misconfiguration Scanner"
LABEL "com.github.actions.description"="Scan for misconfigurations in Terraform code"
LABEL "com.github.actions.icon"="code"
LABEL "com.github.actions.color"="yellow"

LABEL "repository"="https://github.com/ezerfernandes/misconfig-github-action"
LABEL "homepage"="https://github.com/ezerfernandes/misconfig-github-action"
LABEL "maintainer"="Ezer Silva <ezersilva@gmail.com>"

COPY ./src/entrypoint.sh /entrypoint.sh
COPY ./src/process_results.py /process_results.py
COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
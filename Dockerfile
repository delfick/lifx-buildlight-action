FROM python:3.8-alpine

LABEL "version"="1.0.0"
LABEL "repository"="https://github.com/delfick/lifx-buildlight-action"
LABEL "homepage"="https://github.com/delfick/lifx-buildlight-action"
LABEL "maintainer"="Stephen Moore <delfick755@gmail.com>"

LABEL "com.github.actions.name"="LIFX GitHub Action buildlight"
LABEL "com.github.actions.description"="GitHub Action for triggering LIFX lights as a buildlight"
LABEL "com.github.actions.icon"="package"
LABEL "com.github.actions.color"="blue"

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY LICENSE README.rst entrypoint.py /
RUN chmod +x /entrypoint.py

ENTRYPOINT [ "/entrypoint.py" ]

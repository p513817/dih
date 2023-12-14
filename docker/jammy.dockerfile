FROM ubuntu:22.04
RUN apt update && \
    apt install -yq python3-dev python3-pip && \
    apt install -yq --no-install-recommends docker.io

WORKDIR /tmp
COPY [ "requirements.txt", "./" ]
RUN pip install -r requirements.txt

VOLUME [ "/var/run/docker.sock" ]

ENTRYPOINT [ "/bin/bash", "-lc" ]
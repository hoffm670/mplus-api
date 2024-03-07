FROM python:3.10.12

# COPY requirements.txt requirements.txt
COPY requirements-frozen.txt requirements-frozen.txt
RUN pip3 install -r requirements-frozen.txt

ARG WORKDIR="/mplus-api"

WORKDIR $WORKDIR
COPY app ${WORKDIR}/app
COPY log_conf.yaml firebase-admin-key.json ${WORKDIR}

ENTRYPOINT [ "/usr/local/bin/python3", "main.py" ]
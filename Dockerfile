### Builder ###
FROM python:3.13-alpine AS builder

RUN apk add binutils

COPY requirements-frozen.txt requirements-frozen.txt
RUN pip3 install -r requirements-frozen.txt

COPY app /app

RUN pyinstaller --onefile /app/main.py


### Executor ###
FROM alpine:3.21

ARG WORKDIR="/mplus-api"
WORKDIR $WORKDIR
COPY --from=builder /dist/main ${WORKDIR}
COPY log_conf.yaml firebase-admin-key.json ${WORKDIR}

ENV ENVIRONMENT='PROD'

ENTRYPOINT ["./main"]
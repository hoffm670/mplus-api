### Builder ###
FROM python:3.10.12-alpine as builder

RUN apk add binutils

COPY requirements-frozen.txt requirements-frozen.txt
RUN pip3 install -r requirements-frozen.txt

COPY app /app

RUN pyinstaller --onefile /app/main.py


### Executor ###
FROM alpine:3.16

ARG WORKDIR="/mplus-api"
WORKDIR $WORKDIR
COPY --from=builder /dist/main ${WORKDIR}
COPY log_conf.yaml firebase-admin-key.json ${WORKDIR}
COPY deploy-config.json ${WORKDIR}/config.json

ENTRYPOINT ["./main"]
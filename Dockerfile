FROM python:3.10.12


COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt


COPY app/ /app
COPY log_conf.yaml /app/log_conf.yaml
WORKDIR /app


EXPOSE 80

# ENTRYPOINT [ "/bin/bash" ]
ENTRYPOINT [ "/usr/local/bin/python3", "main.py" ]
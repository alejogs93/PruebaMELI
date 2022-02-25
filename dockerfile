# set base image (host OS)
FROM python:3.8.12
WORKDIR /app
COPY requirements.txt .

RUN set -eux && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y default-libmysqlclient-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt
COPY *.py .
CMD [ "python", "./main.py" ]

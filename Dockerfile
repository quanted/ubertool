FROM python:2

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -qr /tmp/requirements.txt

COPY . /src/
WORKDIR /src


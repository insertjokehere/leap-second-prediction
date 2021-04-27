FROM python:3.9

WORKDIR /src

ADD . .

RUN pip install -r requirements.txt

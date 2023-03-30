FROM harbor.hhome.me/library/poetry311:latest AS builder

WORKDIR /src

COPY . .

RUN poetry-wheel-dist

FROM python:3.11-alpine@sha256:4b4078a3ab81edc2f5725cd42b065beaeeb4f9be3b4b1e3b4cf11dd6ae9720d3

COPY --from=builder /src/dist/* /src/
COPY --from=builder /src/poetry.lock /src/

RUN pip install bulletin-a --no-index --find-links /src && rm /src/*.whl

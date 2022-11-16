FROM harbor.hhome.me/library/poetry310:latest AS builder

WORKDIR /src

COPY . .

RUN poetry-wheel-dist

FROM python:3.10-alpine@sha256:00be2731a1c650d3573aebd84a46c06f3a3251377323f6f43ff1386e70ea2992

COPY --from=builder /src/dist/* /src/
COPY --from=builder /src/poetry.lock /src/

RUN pip install bulletin-a --no-index --find-links /src && rm /src/*.whl

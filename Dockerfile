FROM harbor.hhome.me/library/poetry310:latest AS builder

WORKDIR /src

COPY . .

RUN poetry-wheel-dist

FROM python:3.11-alpine@sha256:af8fef83397b3886ed93d2c81bf3b4e70d39c0789c1c6feb1ecb86ca9bc42a0a

COPY --from=builder /src/dist/* /src/
COPY --from=builder /src/poetry.lock /src/

RUN pip install bulletin-a --no-index --find-links /src && rm /src/*.whl

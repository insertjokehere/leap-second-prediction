FROM harbor.hhome.me/library/poetry311:latest AS builder

WORKDIR /src

COPY . .

RUN poetry-wheel-dist

FROM python:3.11-alpine@sha256:4e8e9a59bf1b3ca8e030244bc5f801f23e41e37971907371da21191312087a07

COPY --from=builder /src/dist/* /src/
COPY --from=builder /src/poetry.lock /src/

RUN pip install bulletin-a --no-index --find-links /src && rm /src/*.whl

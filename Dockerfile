FROM harbor.hhome.me/library/poetry311:latest AS builder

WORKDIR /src

COPY . .

RUN poetry-wheel-dist

FROM python:3.11-alpine@sha256:f9ce6fe33d9a5499e35c976df16d24ae80f6ef0a28be5433140236c2ca482686

COPY --from=builder /src/dist/* /src/
COPY --from=builder /src/poetry.lock /src/

RUN pip install bulletin-a --no-index --find-links /src && rm /src/*.whl

FROM harbor.hhome.me/library/poetry311:latest AS builder

WORKDIR /src

COPY . .

RUN poetry-wheel-dist

FROM python:3.11-alpine@sha256:2e23d6cd236ffccc88db47e7520f67cfb5cd9dd62b8d534d3249834930cc226e

COPY --from=builder /src/dist/* /src/
COPY --from=builder /src/poetry.lock /src/

RUN pip install bulletin-a --no-index --find-links /src && rm /src/*.whl

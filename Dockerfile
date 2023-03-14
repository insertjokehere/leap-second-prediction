FROM harbor.hhome.me/library/poetry311:latest AS builder

WORKDIR /src

COPY . .

RUN poetry-wheel-dist

FROM python:3.11-alpine@sha256:04eb46ecb35f63d47fa675fbcfa287f1a5043eab138587b57bad8c579cab51a3

COPY --from=builder /src/dist/* /src/
COPY --from=builder /src/poetry.lock /src/

RUN pip install bulletin-a --no-index --find-links /src && rm /src/*.whl

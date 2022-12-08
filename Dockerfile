FROM harbor.hhome.me/library/poetry310:latest AS builder

WORKDIR /src

COPY . .

RUN poetry-wheel-dist

FROM python:3.10-alpine@sha256:63d0c387f30f82da7e9404b7157b6f077656b5263c8d64c7b7b889f4d8c1c60a

COPY --from=builder /src/dist/* /src/
COPY --from=builder /src/poetry.lock /src/

RUN pip install bulletin-a --no-index --find-links /src && rm /src/*.whl

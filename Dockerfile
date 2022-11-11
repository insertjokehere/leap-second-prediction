FROM harbor.hhome.me/library/poetry310:latest AS builder

WORKDIR /src

COPY . .

RUN poetry-wheel-dist

FROM python:3.10-alpine@sha256:486782edd7f7363ffdc256fc952265a5cbe0a6e047a6a1ff51871d2cdb665351

COPY --from=builder /src/dist/* /src/
COPY --from=builder /src/poetry.lock /src/

RUN pip install bulletin-a --no-index --find-links /src && rm /src/*.whl

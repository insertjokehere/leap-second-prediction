FROM harbor.hhome.me/library/poetry310:latest AS builder

WORKDIR /src

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-dev

COPY . .

RUN poetry build --format sdist \
    && poetry export --format requirements.txt > /tmp/requirements.txt \
    && require-setuptools \
    && pip download -r /tmp/requirements.txt -d dist/  \
    && pip download pip wheel -d dist/ \
    && pip wheel -r /tmp/requirements.txt -w dist/


FROM python:3.10-alpine@sha256:9316f0d151250a0b5a6c6bc26ed11f7e1cb29e856fa0da48fa9d084a3c67d46d

COPY --from=builder /src/dist/* /src/
COPY --from=builder /src/poetry.lock /src/

RUN pip install bulletin-a --no-index --find-links /src && rm /src/*.whl

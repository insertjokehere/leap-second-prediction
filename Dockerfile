FROM harbor.hhome.me/library/poetry39:latest AS builder

WORKDIR /src

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-dev

COPY . .

RUN poetry build --format sdist \
    && poetry export --format requirements.txt --without-hashes > /tmp/requirements.txt \
    && pip download -r /tmp/requirements.txt -d dist/  \
    && pip download pip setuptools wheel -d dist/ \
    && pip wheel -r /tmp/requirements.txt -w dist/


FROM python:3.9-alpine@sha256:aded2e43ada04522e712ce507ce8a04392f8cbe047c914c5a88e4016a7141bd0

COPY --from=builder /src/dist/* /src/
COPY --from=builder /src/poetry.lock /src/

RUN pip install bulletin-a --no-index --find-links /src && rm /src/*.whl

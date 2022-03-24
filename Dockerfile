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


FROM python:3.10-alpine@sha256:cef1da7133de6dbde6c0e253dcd5b2b3085ed3d9c49392f76c07a973df3fa0f7

COPY --from=builder /src/dist/* /src/
COPY --from=builder /src/poetry.lock /src/

RUN pip install bulletin-a --no-index --find-links /src && rm /src/*.whl

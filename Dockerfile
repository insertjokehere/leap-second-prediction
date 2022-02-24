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


FROM python:3.9-alpine@sha256:e23a202fecc2542be4c64f2dc0cb5a387fbdcc7f8d2a875b3a54efe74628ea1f

COPY --from=builder /src/dist/* /src/
COPY --from=builder /src/poetry.lock /src/

RUN pip install bulletin-a --no-index --find-links /src && rm /src/*.whl

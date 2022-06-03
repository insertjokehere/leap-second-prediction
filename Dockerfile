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


FROM python:3.10-alpine@sha256:f04a62c5f08dffec45b3d33a41c61112394669f17aca2b2dc260f7a993fa373b

COPY --from=builder /src/dist/* /src/
COPY --from=builder /src/poetry.lock /src/

RUN pip install bulletin-a --no-index --find-links /src && rm /src/*.whl

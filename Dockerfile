
FROM python:3.13.5-bookworm

LABEL MAINTAINER="Ameya Shenoy <shenoy.ameya@gmail.com>"

ENV PIP_VERSION=25.1.1
ENV UV_VERSION=0.7.21
ENV UV_SYSTEM_PYTHON=true

WORKDIR /app

COPY pyproject.toml uv.lock /app/

RUN set -ex \
  && pip install --no-cache-dir \
    "pip==$PIP_VERSION" \
    "uv==$UV_VERSION" \
  && uv sync --frozen --no-install-project

COPY . /app


# syntax=docker/dockerfile:1.7-labs

FROM python:3.11-slim@sha256:6459da0f052d819e59b5329bb8f76b2f2bd16427ce6fd4db91e11b3759850380 as base

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"

# NB: get the package version using: apt-cache policy <package name>
RUN apt-get update
RUN apt-get install -y openssl=3.0.11-1~deb12u2 pango1.0=1.50.12+ds-1
RUN rm -rf /var/cache/apt/lists

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


FROM base as release
COPY --exclude=tests --exclude=*_test.* . .
RUN adduser nonroot --disabled-password
USER nonroot
CMD ./cmd.sh


FROM base as test
COPY . .
RUN pip install --no-cache-dir -r requirements_test.txt
RUN adduser nonroot --disabled-password
USER nonroot
# Now wait for test commands passed with "exec"

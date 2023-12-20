# syntax=docker/dockerfile:1

FROM python:3.11-slim as base

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y openssl
RUN rm -rf /var/cache/apt/lists

RUN pip install --no-cache-dir --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

FROM base as intermediate1
COPY . .

FROM intermediate1 as intermediate2
RUN rm -rf tests
RUN rm -f *_test.*

FROM base as release
# Copying from an earlier target rather than using FROM ensures
# that the removed files are not hidden in a layer in the release.
COPY --from=intermediate2 /app .
RUN adduser nonroot --disabled-password
USER nonroot
CMD ./cmd.sh

FROM intermediate1 as test
RUN adduser nonroot --disabled-password
USER nonroot
RUN pip install --no-cache-dir -r requirements_test.txt
# Now wait for test commands passed with "exec"

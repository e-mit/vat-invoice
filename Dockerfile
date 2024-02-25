# syntax=docker/dockerfile:1

FROM python:3.11-slim@sha256:6459da0f052d819e59b5329bb8f76b2f2bd16427ce6fd4db91e11b3759850380 as base

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"

# NB: get the package version using: apt-cache policy <package name>
RUN apt-get update && apt-get install -y openssl=3.0.11-1~deb12u2 weasyprint=57.2-1
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
RUN pip install --no-cache-dir -r requirements_test.txt
RUN adduser nonroot --disabled-password
USER nonroot
# Now wait for test commands passed with "exec"

# VAT invoice generator

![docker test build](https://github.com/e-mit/vat-invoice/actions/workflows/docker-test-build.yml/badge.svg)
![tests](https://github.com/e-mit/vat-invoice/actions/workflows/tests.yml/badge.svg)
![coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/e-mit/9df92671b4e2859b1e75cf762121b73f/raw/vat-invoice.json)
![flake8](https://github.com/e-mit/vat-invoice/actions/workflows/flake8.yml/badge.svg)
![mypy](https://github.com/e-mit/vat-invoice/actions/workflows/mypy.yml/badge.svg)
![pycodestyle](https://github.com/e-mit/vat-invoice/actions/workflows/pycodestyle.yml/badge.svg)
![pydocstyle](https://github.com/e-mit/vat-invoice/actions/workflows/pydocstyle.yml/badge.svg)
![pylint](https://github.com/e-mit/vat-invoice/actions/workflows/pylint.yml/badge.svg)
![pyright](https://github.com/e-mit/vat-invoice/actions/workflows/pyright.yml/badge.svg)
![bandit](https://github.com/e-mit/vat-invoice/actions/workflows/bandit.yml/badge.svg)
![docker release build](https://github.com/e-mit/vat-invoice/actions/workflows/docker-release-build.yml/badge.svg)
![release test](https://github.com/e-mit/vat-invoice/actions/workflows/release-test.yml/badge.svg)
![docker-hub-push](https://github.com/e-mit/vat-invoice/actions/workflows/docker-hub-push.yml/badge.svg)
![google-cloud-deploy](https://github.com/e-mit/vat-invoice/actions/workflows/google-cloud-deploy.yml/badge.svg)

A Python web application for creating VAT invoices.

This project uses Flask, WTForms and Docker. PDFs are generated with Weasyprint.

[Try the example deployment on Google Cloud Run.](https://vat-invoice-service-uzzizxhvgq-ew.a.run.app/)
(Note: this is a free GCR instance which scales to zero, causing a brief startup delay).

It is also hosted on AWS EC2 at [https://vat.e-mit.dev](https://vat.e-mit.dev).

[Docker Hub image repository](https://hub.docker.com/r/emit5/vat-invoice)

### Readme Contents

- **[Development and testing](#development-and-testing)**<br>
- **[Continuous deployment](#continuous-deployment)**<br>
- **[License](#license)**<br>


## Development and testing

The Dockerfile has two targets: test and release. The release target excludes test files/packages.

Tests and linting checks run via GitHub actions, in the test container, after each push.

During local development:
- Run all tests with ```build_and_test.sh```
- Try the release version at ```127.0.0.1:8080``` with ```release_run.sh```

## Continuous deployment

If all GitHub action test/lint workflows pass, and if the commit was tagged with a version, the new release image is automatically pushed to Docker Hub and deployed to Google Cloud Run as a new revision.

The release image on Docker Hub is tagged with the commit hash. The app's ```/version``` HTTP route serves a json string giving the version tag and the commit hash.

## License

See the [LICENSE](LICENSE) file for software license rights and limitations (AGPL-3.0).

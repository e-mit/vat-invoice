# VAT invoice generator

![docker test build](https://github.com/e-mit/vat-invoice/actions/workflows/docker-test-build.yml/badge.svg)
![tests](https://github.com/e-mit/vat-invoice/actions/workflows/tests.yml/badge.svg)
![coverage](https://github.com/e-mit/vat-invoice/actions/workflows/coverage.yml/badge.svg)
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

This project uses Flask, WTForms and Docker. [Try the example deployment on Google Cloud Run.](https://vat-invoice-service-uzzizxhvgq-ew.a.run.app/)

[Docker Hub image repository](https://hub.docker.com/r/emit5/vat-invoice)

### Readme Contents

- **[Development and testing](#development-and-testing)**<br>
- **[Deployment](#deployment)**<br>
- **[Changelog](#changelog)**<br>
- **[License](#license)**<br>


## Development and testing

The Dockerfile has two targets: test and release. The release target is designed to avoid the inclusion of test files/packages in its hidden layers.

Tests and linting checks run in the test container with GitHub actions. The release image is tagged with the commit hash.

Run all tests locally during development with ```build_and_test.sh``` and try the release version locally at ```127.0.0.1:8080``` with ```release_run.sh```.

## Continuous deployment

If all workflows on the test image have passed, the SHA256 of the newly-built release image is compared with the most recent [image on Docker Hub](https://hub.docker.com/r/emit5/vat-invoice). If the hash has changed, the new image is pushed to Docker Hub and deployed to Google Cloud Run as a new revision.

The triggering commit for new release images must be tagged (with a semantic version), else this process will fail and no push/deployment occurs.

## License

See the [LICENSE](LICENSE) file for software license rights and limitations (AGPL-3.0).

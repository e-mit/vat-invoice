# VAT invoice generator

![docker test build](https://github.com/e-mit/vat-invoice/actions/workflows/docker-test-build.yml/badge.svg)
![tests](https://github.com/e-mit/vat-invoice/actions/workflows/tests.yml/badge.svg)
![coverage](https://github.com/e-mit/vat-invoice/actions/workflows/coverage.yml/badge.svg)
![coverage%](https://coverage-badge.samuelcolvin.workers.dev/e-mit/vat-invoice.svg)
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
- **[Deployment](#continuous-deployment)**<br>
- **[License](#license)**<br>


## Development and testing

The Dockerfile has two targets: test and release. The release target avoids the inclusion of test files/packages in its hidden layers.

Tests and linting checks run via GitHub actions, in the test container, after each push.

During local development:
- Run all tests with ```build_and_test.sh```
- Try the release version at ```127.0.0.1:8080``` with ```release_run.sh```

## Continuous deployment

If all workflows on the test image have passed, and if the commit was tagged with a version, the new release image is pushed to Docker Hub and deployed to Google Cloud Run as a new revision.

The release image on Docker Hub is tagged with the commit hash. The ```/version``` route serves a json string giving the version tag and the commit hash.

## License

See the [LICENSE](LICENSE) file for software license rights and limitations (AGPL-3.0).

"""Gather the results of all GitHub action workflows, or timeout."""

import os
import sys
import time
from typing import Any
from pathlib import Path
from io import BytesIO, TextIOWrapper
from zipfile import ZipFile
import requests


TIMEOUT_SECONDS: int = 180
PAUSE_SECONDS: int = 3
GH_API_VERSION: str = "2022-11-28"
ARTIFACT_FILENAME: str = "data.txt"
PASS_RETURN_VALUE: int = 0
FAIL_RETURN_VALUE: int = 1
WORKFLOW_SUCCESS: str = "success"

GITHUB_SHA: str = os.environ['GITHUB_SHA']
REPO_PATH: str = os.environ['REPO_PATH']
GH_TOKEN: str = os.environ['GH_TOKEN']
BASE_URL = f"https://api.github.com/repos/{REPO_PATH}/actions/runs"
HEADERS = {"Accept": "application/vnd.github+json",
           "Authorization": f"Bearer {GH_TOKEN}",
           "X-GitHub-Api-Version": GH_API_VERSION}


def list_all_yaml_files(dir: Path | str) -> set[str]:
    """Find all yaml files in the specified directory."""
    files = set()
    for file in os.listdir(dir):
        if file.lower().endswith(".yaml") or file.lower().endswith(".yml"):
            files.add(str(Path(file).stem))
    return files


def list_exclude_files(argv: list[str]) -> set[str]:
    """Find files/workflows to exclude from input list."""
    files = set()
    for file in argv[1:]:
        if file.lower().endswith(".yaml") or file.lower().endswith(".yml"):
            files.add(str(Path(file).stem))
        else:
            files.add(file)
    return files


def get_workflows() -> list[dict[str, Any]]:
    """List all workflows for the current commit."""
    workflow_query = f"{BASE_URL}?head_sha={GITHUB_SHA}"
    return requests.get(url=workflow_query,
                        headers=HEADERS).json()['workflow_runs']


def get_artifacts(workflow_id: str) -> list[dict[str, Any]]:
    """List all artifacts for the workflow with the input ID."""
    artifact_query = f"{BASE_URL}/{workflow_id}/artifacts"
    return requests.get(url=artifact_query,
                        headers=HEADERS).json()['artifacts']


def workflow_pass(archive_download_url: str) -> bool:
    """Open the data file in the artifact and check contents."""
    data = requests.get(url=archive_download_url, headers=HEADERS)
    with ZipFile(BytesIO(data.content)) as z:
        with TextIOWrapper(z.open(ARTIFACT_FILENAME), encoding="utf-8") as f:
            if f.read().strip() == WORKFLOW_SUCCESS:
                return True
            return False


if __name__ == "__main__":
    required_workflows = (list_all_yaml_files(Path(".github/workflows"))
                          - list_exclude_files(sys.argv))
    start_time = time.time()
    while (time.time() - start_time) < TIMEOUT_SECONDS:
        passed_workflows: set[str] = set()
        failed_workflows: set[str] = set()
        for workflow in get_workflows():
            if workflow['name'] in required_workflows:
                expected_artifact_name = f"{workflow['name']}_{GITHUB_SHA}"
                for artifact in get_artifacts(workflow['id']):
                    if artifact['name'] == expected_artifact_name:
                        if workflow_pass(artifact['archive_download_url']):
                            passed_workflows.add(workflow['name'])
                        else:
                            failed_workflows.add(workflow['name'])
        if passed_workflows == required_workflows:
            exit(PASS_RETURN_VALUE)
        if failed_workflows:
            break
        time.sleep(PAUSE_SECONDS)
    print(f"Passing workflows: {passed_workflows}")  # type: ignore
    print(f"Failing workflows: {failed_workflows}")  # type: ignore
    not_reported = (required_workflows - passed_workflows  # type: ignore
                    - failed_workflows)  # type: ignore
    if not_reported:
        print(f"Workflows not reported: {not_reported}")
    exit(FAIL_RETURN_VALUE)

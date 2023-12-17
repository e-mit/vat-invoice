"""Tests for invoice.py"""
import pytest
from main import app
import config


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_version(client):
    response = client.get('/version')
    assert response.status_code == 200
    assert response.is_json
    assert response.json['version'] == config.VERSION

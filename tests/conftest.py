import pytest
from fastapi.testclient import TestClient

from my_api.db.database import db_init
from my_api.main import app


@pytest.fixture(scope="module")
def client():
    db_init()
    client = TestClient(app=app)
    yield client

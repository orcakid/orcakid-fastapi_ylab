import pytest
from main import app
from fastapi.testclient import TestClient
from dotenv import load_dotenv


@pytest.fixture(scope='module')
def client():
    load_dotenv(".env")
    client = TestClient(app=app)
    yield client
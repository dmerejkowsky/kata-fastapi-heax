from fastapi.testclient import TestClient

from fastapi_hexa.main import app

test_client = TestClient(app)


def test_get_index() -> None:
    response = test_client.get("/")

    assert response.is_success

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from fastapi_hexa.database import Database
from fastapi_hexa.main import app, get_database

test_client = TestClient(app)


def test_get_index() -> None:
    response = test_client.get("/")

    assert response.is_success


@pytest.fixture
def test_app(database: Database) -> FastAPI:
    def get_database_override() -> Database:
        return database

    app.dependency_overrides[get_database] = get_database_override
    return app


def test_get_trains_when_database_is_not_empty(
    database: Database, test_app: FastAPI
) -> None:
    database.insert_train("express_2000")

    response = test_client.get("/trains")

    assert response.is_success
    assert response.json() == [{"name": "express_2000"}]


def test_get_trains_when_database_is_empty(
    database: Database, test_app: FastAPI
) -> None:
    response = test_client.get("/trains")

    assert response.is_success
    assert response.json() == []

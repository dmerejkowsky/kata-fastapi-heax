import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from fastapi_hexa.database import Database
from fastapi_hexa.main import app, get_database


@pytest.fixture
def test_app(database: Database) -> FastAPI:
    def get_database_override() -> Database:
        return database

    app.dependency_overrides[get_database] = get_database_override
    return app


@pytest.fixture
def test_client(test_app: FastAPI) -> TestClient:
    return TestClient(test_app)


def test_get_index(test_client: TestClient) -> None:
    response = test_client.get("/")

    assert response.is_success


def test_get_trains_when_database_is_not_empty(
    database: Database, test_client: TestClient
) -> None:
    database.insert_train("express_2000")

    response = test_client.get("/trains")

    assert response.is_success
    assert response.json() == [{"name": "express_2000"}]


def test_get_trains_when_database_is_empty(
    database: Database, test_client: TestClient
) -> None:
    response = test_client.get("/trains")

    assert response.is_success
    assert response.json() == []


def test_get_train_with_one_seat_booked(
    database: Database, test_client: TestClient
) -> None:
    response = test_client.get("/trains")
    database.insert_train("express_2000")
    database.insert_seat(
        number="1A",
        train_name="express_2000",
        booking_reference="",
    )
    database.insert_seat(
        number="2A",
        train_name="express_2000",
        booking_reference="abc123",
    )

    response = test_client.get("/train/express_2000")

    assert response.is_success
    assert response.json() == {
        "seats": {
            "1A": {"seat_number": "1A", "booking_reference": ""},
            "2A": {"seat_number": "2A", "booking_reference": "abc123"},
        }
    }


def test_book_empty_seat(database: Database, test_client: TestClient) -> None:
    database.insert_train("express_2000")
    database.insert_seat(
        number="1A",
        train_name="express_2000",
        booking_reference="abc123",
    )
    database.insert_seat(
        number="2A",
        train_name="express_2000",
        booking_reference="",
    )

    response = test_client.post(
        "/train/book",
        json={
            "train": "express_2000",
            "seat_number": "2A",
            "booking_reference": "def456",
        },
    )

    assert response.is_success

    seat = database.get_seat(train_name="express_2000", number="2A")

    assert seat
    assert seat.booking_reference == "def456"


def test_cannot_book_same_seat_twice(
    database: Database, test_client: TestClient
) -> None:
    database.insert_train("express_2000")
    database.insert_seat(
        number="1A",
        train_name="express_2000",
        booking_reference="abc123",
    )
    database.insert_seat(
        number="2A",
        train_name="express_2000",
        booking_reference="",
    )

    response = test_client.post(
        "/train/book",
        json={
            "train": "express_2000",
            "seat_number": "1A",
            "booking_reference": "def456",
        },
    )

    assert response.is_client_error

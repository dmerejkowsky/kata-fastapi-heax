
from fastapi_hexa.booking import Train
from fastapi_hexa.database import Database


def test_can_insert_a_train(database: Database) -> None:
    database.insert_train("express_2000")

    saved_train = database.get_train(name="express_2000")

    assert saved_train
    assert saved_train.name == "express_2000"
    assert database.get_train_names() == ["express_2000"]


def test_can_insert_a_train_twice(database: Database) -> None:
    database.insert_train("express_2000")
    database.insert_train("express_2000")


def test_train_not_found(database: Database) -> None:
    assert database.get_train(name="express_2000") is None
    assert database.get_train_names() == []


def test_can_add_seats_to_train(database: Database) -> None:
    database.insert_train("express_2000")
    database.insert_seat(number="1A", train_name="express_2000", booking_reference="")
    database.insert_seat(
        number="2A", train_name="express_2000", booking_reference="abc123"
    )

    saved_seats = database.get_seats(train_name="express_2000")
    assert len(saved_seats) == 2



def test_can_book_a_seat(database: Database) -> None:
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

    database.insert_seat(
        number="1A",
        train_name="express_2000",
        booking_reference="abc123",
    )

    saved_seat = database.get_seat(train_name="express_2000", number="1A")

    assert saved_seat
    assert saved_seat.booking_reference == "abc123"


def test_can_save_and_load_a_train(database: Database) -> None:
    train = Train.empty("express_2000", seat_numbers=["1A", "2A", "3A"])

    train.book("1A", "BOOK1")

    database.save_train(train)

    train = database.load_train(train.name)

    assert train.get_seat("1A").booking_reference == "BOOK1"

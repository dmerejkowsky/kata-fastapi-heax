import pytest

from fastapi_hexa.booking import AlreadyBooked, Seat, Train


def test_booking_an_free_seat() -> None:
    seat = Seat.free("1A")
    assert seat.is_free

    seat.book("BOOK1")

    assert not seat.is_free
    assert seat.booking_reference == "BOOK1"


def test_two_people_booking_same_seat() -> None:
    """
    Given seat A1 with booking reference BOOK1
    When trying to book seat A1 with booking reference BOOK2
    Then an exception is raised.
    """

    seat = Seat.booked("A1", "BOOK1")

    with pytest.raises(AlreadyBooked) as e:
        seat.book("BOOK2")

    assert e.value.seat_number == "A1"
    assert e.value.existing_reference == "BOOK1"
    assert e.value.conflicting_reference == "BOOK2"


def test_can_create_an_empty_train_has_free_seats() -> None:
    train = Train.empty("express_2000", seat_numbers=["1A", "2A", "3A"])
    seats = train.seats
    for seat in seats:
        assert seat.is_free


def test_can_book_seats_from_train() -> None:
    train = Train.empty("express_2000", seat_numbers=["1A", "2A", "3A"])

    train.book("1A", "BOOK1")

    seat = train.get_seat("1A")
    assert seat.is_booked
    assert seat.booking_reference == "BOOK1"

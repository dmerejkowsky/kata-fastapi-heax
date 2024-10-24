import pytest

from fastapi_hexa.booking import Seat


def test_two_people_booking_same_seat() -> None:
    """Given seat A1 with booking reference
    BOOK1,
    When trying to book seat A1 with booking
    reference BOOK2
    Then an exception is raised."""

    seat = Seat("A1")
    seat.book("BOOK1")

    with pytest.raises(ValueError):
        seat.book("BOOK2")

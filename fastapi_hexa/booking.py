from __future__ import annotations


class AlreadyBooked(Exception):
    def __init__(
        self, seat_number: str, existing_reference: str, conflicting_reference: str
    ) -> None:
        self.seat_number = seat_number
        self.existing_reference = existing_reference
        self.conflicting_reference = conflicting_reference


class Seat:
    def __init__(self, number: str, booking_reference: str) -> None:
        self._number = number
        self._booking_reference = booking_reference

    @classmethod
    def free(cls, number: str) -> Seat:
        return Seat(number, booking_reference="")

    @classmethod
    def booked(cls, number: str, booking_reference: str) -> Seat:
        return Seat(number, booking_reference=booking_reference)

    @property
    def number(self) -> str:
        return self._number

    @property
    def booking_reference(self) -> str:
        return self._booking_reference

    @property
    def is_free(self) -> bool:
        return self._booking_reference == ""

    @property
    def is_booked(self) -> bool:
        return self._booking_reference != ""

    def book(self, booking_reference: str) -> None:
        if self._booking_reference and self._booking_reference != booking_reference:
            raise AlreadyBooked(
                self._number, self._booking_reference, booking_reference
            )
        self._booking_reference = booking_reference


class Train:
    def __init__(self, name: str, *, seats: list[Seat]) -> None:
        self.name = name
        self._seats = {seat.number: seat for seat in seats}

    @classmethod
    def empty(cls, name: str, *, seat_numbers: list[str]) -> Train:
        seats = [Seat.free(number) for number in seat_numbers]
        return cls(name, seats=seats)

    def get_seat(self, seat_number: str) -> Seat:
        return self._seats[seat_number]

    def book(self, seats: list[str], booking_reference: str) -> None:
        for number in seats:
            seat = self.get_seat(number)
        seat.book(booking_reference)

    @property
    def seats(self) -> list[Seat]:
        return list(self._seats.values())

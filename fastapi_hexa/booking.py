class Seat:
    def __init__(self, number: str) -> None:
        self._number = number
        self._booking_reference = ""

    def book(self, booking_reference: str) -> None:
        if self._booking_reference and self._booking_reference != booking_reference:
            raise ValueError()
        self._booking_reference = booking_reference

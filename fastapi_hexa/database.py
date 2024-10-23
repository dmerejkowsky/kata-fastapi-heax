import os
from pathlib import Path

from sqlalchemy import Engine, ForeignKey, String, UniqueConstraint, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    scoped_session,
)
from ulid import ULID


def get_url_from_env() -> str:
    db_path = Path(os.environ["TRAIN_DATABASE_PATH"])
    return f"sqlite:///{db_path.absolute()}"


def get_engine(*, url: str) -> Engine:
    echo = bool(os.environ.get("TRAIN_DATABASE_VERBOSE_SQL", False))
    return create_engine(
        url,
        echo=echo,
        connect_args={"check_same_thread": False},
    )


class Base(DeclarativeBase):
    pass


class TrainModel(Base):
    __tablename__ = "trains"

    name: Mapped[str] = mapped_column(String, nullable=False, primary_key=True)


class SeatModel(Base):
    __tablename__ = "seats"
    __table_args__ = (
        UniqueConstraint(
            "train_name", "number", name="unique_constraint_train_name_number"
        ),
    )

    id: Mapped[str] = mapped_column(
        String(length=26),
        primary_key=True,
        nullable=False,
    )

    number: Mapped[str] = mapped_column(String, nullable=False, primary_key=True)
    train_name: Mapped[str] = mapped_column(ForeignKey("trains.name"))
    booking_reference: Mapped[str] = mapped_column(String)


class Database:
    def __init__(self, session: Session | scoped_session[Session]) -> None:
        self._session = session

    def insert_train(self, name: str) -> None:
        model = TrainModel(name=name)
        self._session.add(model)
        self._session.commit()

    def get_train(self, name: str) -> TrainModel | None:
        row = (
            self._session.query(TrainModel)
            .filter(TrainModel.name == name)
            .one_or_none()
        )
        return row

    def get_train_names(self) -> list[str]:
        rows = self._session.query(TrainModel).all()
        return sorted(r.name for r in rows)

    def insert_seat(
        self, *, number: str, train_name: str, booking_reference: str
    ) -> None:
        id = ULID()
        seat = SeatModel(
            number=number,
            train_name=train_name,
            booking_reference=booking_reference,
            id=str(id),
        )
        self._session.add(seat)
        self._session.commit()

    def get_seats(self, *, train_name: str) -> list[SeatModel]:
        return (
            self._session.query(SeatModel)
            .filter(SeatModel.train_name == train_name)
            .order_by(SeatModel.number)
            .all()
        )

    def get_seat(self, *, train_name: str, number: str) -> SeatModel | None:
        return (
            self._session.query(SeatModel)
            .filter(SeatModel.train_name == train_name)
            .filter(SeatModel.number == number)
            .one_or_none()
        )

    def update_seat(
        self, *, train_name: str, number: str, booking_reference: str
    ) -> None:
        seat = (
            self._session.query(SeatModel)
            .filter(SeatModel.train_name == train_name)
            .filter(SeatModel.number == number)
            .one()
        )
        if seat.booking_reference and seat.booking_reference != booking_reference:
            raise ValueError("Already booked")
        seat.booking_reference = booking_reference
        self._session.commit()

    def close(self) -> None:
        self._session.close()

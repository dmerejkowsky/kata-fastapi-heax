from typing import Iterator

from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import scoped_session, sessionmaker

from fastapi_hexa.database import Database, engine


def get_database() -> Iterator[Database]:
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)
    session = Session()
    database = Database(session)
    yield database
    Session.remove()


app = FastAPI()


@app.get("/")
def index() -> str:
    return "hello"


class Seat(BaseModel):
    booking_reference: str
    seat_number: str
    coach: str


class TrainData(BaseModel):
    seats: dict[str, Seat]


@app.get("/data_for_train/{train_id}")
def get_data_for_train(train_id: int) -> TrainData:
    return TrainData(seats={})


class TrainSummary(BaseModel):
    name: str


@app.get("/trains")
def get_trains(database: Database = Depends(get_database)) -> list[TrainSummary]:
    return [TrainSummary(name=name) for name in database.get_train_names()]

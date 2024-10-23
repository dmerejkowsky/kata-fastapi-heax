from typing import Iterator

import dotenv
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session

from fastapi_hexa.database import Database, get_engine, get_url_from_env

dotenv.load_dotenv()


def get_database() -> Iterator[Database]:
    url = get_url_from_env()
    engine = get_engine(url=url)
    session = Session(engine)
    database = Database(session)
    yield database
    database.close()


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

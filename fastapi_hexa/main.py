from typing import Iterator

import dotenv
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from fastapi_hexa.database import Database, get_engine, get_url_from_env

dotenv.load_dotenv()

_engine = get_engine(url=get_url_from_env())


def get_database() -> Iterator[Database]:
    session = Session(_engine)
    database = Database(session)
    yield database
    database.close()


app = FastAPI()


@app.get("/")
def index() -> str:
    return "hello"


class TrainSummary(BaseModel):
    name: str


@app.get("/trains")
def get_trains(database: Database = Depends(get_database)) -> list[TrainSummary]:
    return [TrainSummary(name=name) for name in database.get_train_names()]


class Seat(BaseModel):
    booking_reference: str
    seat_number: str


class Train(BaseModel):
    seats: dict[str, Seat]


@app.get("/train/{train_name}")
def get_train(train_name: str, database: Database = Depends(get_database)) -> Train:
    seat_models = database.get_seats(train_name=train_name)
    seats = {
        model.number: Seat(
            booking_reference=model.booking_reference,
            seat_number=model.number,
        )
        for model in seat_models
    }
    return Train(seats=seats)


class BookingRequest(BaseModel):
    train: str
    seat_number: str
    booking_reference: str


@app.post("/train/book")
def book(
    booking_request: BookingRequest, database: Database = Depends(get_database)
) -> str:
    try:
        database.update_seat(
            train_name=booking_request.train,
            number=booking_request.seat_number,
            booking_reference=booking_request.booking_reference,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    return "ok"

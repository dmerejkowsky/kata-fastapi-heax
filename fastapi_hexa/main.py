from fastapi import FastAPI
from pydantic import BaseModel

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

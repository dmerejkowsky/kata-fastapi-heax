from typing import Iterator

import pytest
from sqlalchemy.orm import Session

from fastapi_hexa.database import Base, Database, engine


@pytest.fixture(scope="session")
def database_session() -> Iterator[Session]:
    Base.metadata.create_all(engine)
    session = Session(engine)
    yield session
    session.close()


@pytest.fixture
def database(database_session: Session) -> Iterator[Database]:
    transaction = database_session.begin(nested=True)
    database = Database(session=database_session)
    yield database
    transaction.rollback()


def test_can_insert_a_train(database: Database) -> None:
    database.insert_train("express_2000")

    saved_train = database.get_train(name="express_2000")

    assert saved_train
    assert saved_train.name == "express_2000"


def test_train_not_found(database: Database) -> None:
    assert database.get_train(name="express_2000") is None



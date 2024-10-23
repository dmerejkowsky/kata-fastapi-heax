from typing import Iterator

import pytest
from sqlalchemy import Connection, Engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from fastapi_hexa.database import Base, Database, get_engine


@pytest.fixture(scope="session")
def engine() -> Engine:
    return get_engine(url="sqlite://")


@pytest.fixture(scope="session")
def connection(engine: Engine) -> Connection:
    return engine.connect()


@pytest.fixture(scope="session")
def setup_database(connection: Connection) -> None:
    Base.metadata.create_all(connection)


@pytest.fixture
def database_session(
    engine: Engine, setup_database: None
) -> Iterator[scoped_session[Session]]:
    connection = engine.connect()
    transaction = connection.begin()
    yield scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=connection)
    )
    if transaction.is_valid:
        transaction.rollback()


@pytest.fixture
def database(database_session: scoped_session[Session]) -> Database:
    return Database(session=database_session)

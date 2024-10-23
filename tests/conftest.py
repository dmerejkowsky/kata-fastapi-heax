from typing import Iterator

import pytest
from sqlalchemy.orm import Session

from fastapi_hexa.database import Base, Database, get_engine


@pytest.fixture(scope="session")
def database_session() -> Iterator[Session]:
    engine = get_engine(url="sqlite://")
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

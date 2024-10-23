import pytest
from sqlalchemy import Integer, String, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    scoped_session,
    sessionmaker,
)


class Base(DeclarativeBase):
    pass


class User(Base):

    __tablename__ = "trains"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)


@pytest.fixture(scope="session")
def engine():
    return create_engine("sqlite://")


@pytest.fixture(scope="session")
def connection(engine):
    return engine.connect()


@pytest.fixture(scope="session")
def setup_database(connection):
    Base.metadata.create_all(connection)


@pytest.fixture
def db_session(engine, setup_database):
    connection = engine.connect()
    transaction = connection.begin()
    yield scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=connection)
    )
    transaction.rollback()


def test_create_user(db_session):
    db_user = User(id=3, name="john")
    db_session.add(db_user)
    db_session.commit()


def test_list_users(db_session):
    assert db_session.query(User).all() == []

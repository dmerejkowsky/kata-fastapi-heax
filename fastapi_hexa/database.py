import os

import dotenv
from sqlalchemy import Engine, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

dotenv.load_dotenv()


def get_database_url_from_env() -> str:
    # db_path = os.environ['TRAIN_DATABASE_PATH"]
    return "sqlite://"


def get_engine() -> Engine:
    echo = bool(os.environ.get("TRAIN_DATABASE_VERBOSE_SQL", False))
    url = get_database_url_from_env()
    return create_engine(url, echo=echo)


engine = get_engine()


class Base(DeclarativeBase):
    pass


class TrainModel(Base):
    __tablename__ = "trains"

    name: Mapped[str] = mapped_column(String, nullable=False, primary_key=True)


class Database:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create_all(self) -> None:
        Base.metadata.create_all(engine)

    def insert_train(self, name: str) -> None:
        model = TrainModel(name=name)
        self._session.add(model)
        self._session.flush()

    def get_train(self, name: str) -> TrainModel | None:
        row = (
            self._session.query(TrainModel)
            .filter(TrainModel.name == name)
            .one_or_none()
        )
        return row

    def close(self) -> None:
        self._session.close()

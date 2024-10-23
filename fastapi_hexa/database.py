import os
from pathlib import Path

from sqlalchemy import Engine, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


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


class Database:
    def __init__(self, session: Session) -> None:
        self._session = session

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

    def get_train_names(self) -> list[str]:
        rows = self._session.query(TrainModel).all()
        return sorted(r.name for r in rows)

    def close(self) -> None:
        self._session.close()

from fastapi_hexa.database import Database


def test_can_insert_a_train(database: Database) -> None:
    database.insert_train("express_2000")

    saved_train = database.get_train(name="express_2000")

    assert saved_train
    assert saved_train.name == "express_2000"
    assert database.get_train_names() == ["express_2000"]


def test_train_not_found(database: Database) -> None:
    assert database.get_train(name="express_2000") is None
    assert database.get_train_names() == []

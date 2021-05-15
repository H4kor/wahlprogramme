from wahlprogramme.database import (
    load_text,
    load_year,
    load_db,
    Stats,
    Text,
    Year,
    Database,
)


def test_load_text():
    assert load_text("tests/fixtures/data/1001/b.party.txt") == Text(
        text="same procedure as every year", stats=Stats(size=5)
    )


def test_load_year():
    year = load_year("tests/fixtures/data/1000")
    assert type(year) == Year
    assert type(year.get("a_party")) == Text
    assert type(year.get("b.party")) == Text


def test_load_db():
    db = load_db("tests/fixtures/data")
    assert type(db) == Database
    assert type(db.get("1000")) == Year
    assert type(db.get("1001")) == Year


def test_database_years():
    db = load_db("tests/fixtures/data")
    assert db.years == ["1000", "1001"]


def test_database_partieS():
    db = load_db("tests/fixtures/data")
    assert "a_party" in db.parties
    assert "b.party" in db.parties

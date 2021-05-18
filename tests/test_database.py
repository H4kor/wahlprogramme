from wahlprogramme.database import (
    load_text_from_txt,
    load_text_from_xml,
    load_year,
    load_db,
    Stats,
    StructuredText,
    Text,
    Year,
    Database,
)


def test_load_text_from_txt():
    assert load_text_from_txt("tests/fixtures/data/1001/b.party.txt") == Text(
        text="same procedure as every year", stats=Stats(size=5)
    )


def test_load_text_from_xml():
    text = load_text_from_xml("tests/fixtures/data/1001/s-party.xml")
    assert (
        text.text == "this is a structured document.\nWith multiple pages.\n3 actually!"
    )
    assert type(text.stats) == Stats
    assert text.stats.size == 10


def test_load_year():
    year = load_year("tests/fixtures/data/1000")
    assert type(year) == Year
    assert type(year.get("a_party")) == Text
    assert type(year.get("b.party")) == Text


def test_load_year_only_xml():
    year = load_year("tests/fixtures/data/1001", txt=False)
    assert type(year) == Year
    assert year.get("a_party") is None
    assert type(year.get("s-party")) == StructuredText


def test_load_year_xml():
    year = load_year("tests/fixtures/data/1001")
    assert type(year) == Year
    assert type(year.get("s-party")) == StructuredText


def test_structured_text_pages():
    year = load_year("tests/fixtures/data/1001")
    text = year.get("s-party")
    assert len(text.pages) == 4


def test_structured_text_paragraphs():
    year = load_year("tests/fixtures/data/1001")
    text = year.get("s-party")
    pages = text.pages
    assert len(text.pages[0].paragraphs) == 2


def test_load_db():
    db = load_db("tests/fixtures/data")
    assert type(db) == Database
    assert type(db.get("1000")) == Year
    assert type(db.get("1001")) == Year


def test_load_db_only_xml():
    db = load_db("tests/fixtures/data", txt=False)
    assert type(db) == Database
    assert type(db.get("1001")) == Year
    assert db.get("1001").get("a_party") is None
    assert type(db.get("1001").get("s-party")) == StructuredText


def test_database_years():
    db = load_db("tests/fixtures/data")
    assert db.years == ["1000", "1001"]


def test_database_parties():
    db = load_db("tests/fixtures/data")
    assert "a_party" in db.parties
    assert "b.party" in db.parties

# flake8: noqa: E501
from wahlprogramme import create_app
from wahlprogramme.database import load_db
import pytest


@pytest.fixture
def client():
    db = load_db("tests/fixtures/data")
    app = create_app(db)
    with app.test_client() as client:
        yield client


def test_home_view(client):
    rv = client.get("/")
    assert b"<h2>Parteien</h2>" in rv.data
    assert b"<h2>Jahre</h2>" in rv.data
    assert b'<a href="/year/1000">1000</a>' in rv.data
    assert b'<a href="/year/1001">1001</a>' in rv.data
    assert b'<a href="/party/a_party">a_party</a>' in rv.data
    assert b'<a href="/party/b.party">b.party</a>' in rv.data
    assert b'<a href="/party/s-party">s-party</a>' in rv.data


def test_party_view(client):
    rv = client.get("/party/a_party")
    assert rv.status_code == 200
    assert b'<h2 class="headline">a_party</h2>' in rv.data
    assert b'<a href="/year/1000/party/a_party?">' in rv.data
    assert b'<label class="label-inline" for="relative">Relativ</label>' in rv.data
    assert (
        '<input id="query" type="text" name="query" value="" placeholder="Mehrere Begriffe können durch Kommas getrennt werden">'.encode(
            "utf-8"
        )
        in rv.data
    )


def test_year_view(client):
    rv = client.get("/year/1000")
    assert rv.status_code == 200
    assert b'<h2 class="headline">1000</h2>' in rv.data
    assert b'<a href="/year/1000/party/a_party?">' in rv.data
    assert b'<label class="label-inline" for="relative">Relativ</label>' in rv.data
    assert (
        '<input id="query" type="text" name="query" value="" placeholder="Mehrere Begriffe können durch Kommas getrennt werden">'.encode(
            "utf-8"
        )
        in rv.data
    )


def test_year_party_view(client):
    rv = client.get("/year/1000/party/a_party")
    assert rv.status_code == 200
    assert b'<h2 class="headline">1000 - a_party</h2>' in rv.data
    assert b'<label class="label-inline" for="relative">Relativ</label>' not in rv.data
    assert (
        '<input id="query" type="text" name="query" value="" placeholder="Mehrere Begriffe können durch Kommas getrennt werden">'.encode(
            "utf-8"
        )
        in rv.data
    )

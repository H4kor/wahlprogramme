import os
from collections import namedtuple


Stats = namedtuple("Stats", ["size"])
Text = namedtuple("Text", ["text", "stats"])


class Year:
    def __init__(self):
        super().__init__()
        self._texts = {}

    def set(self, name, text):
        self._texts[name] = text

    def get(self, party):
        return self._texts.get(party)

    @property
    def parties(self):
        return set(self._texts.keys())


class Database:
    def __init__(self):
        super().__init__()
        self._years = {}

    def set(self, name, year):
        self._years[name] = year

    def get(self, year):
        return self._years.get(year)

    @property
    def years(self):
        return sorted(list(self._years.keys()))

    @property
    def parties(self):
        parties = set()
        for year in self._years.values():
            parties |= year.parties
        return parties


def load_text(path):
    with open(path, "r") as f:
        text = f.read().lower()
        stats = Stats(size=len(text.split()))
        return Text(text=text, stats=stats)


def load_year(path):
    year = Year()
    for text in os.listdir(path):
        text_path = os.path.join(path, text)
        if os.path.isfile(text_path) and text.endswith(".txt"):
            text_name = ".".join(text.split(".")[:-1])
            year.set(text_name, load_text(text_path))
    return year


def load_db(path):
    db = Database()
    for year in os.listdir(path):
        year_path = os.path.join(path, year)
        if os.path.isdir(year_path):
            db.set(year, load_year(year_path))
    return db

import os
from collections import namedtuple
import xml.etree.ElementTree as ET


Stats = namedtuple("Stats", ["size"])
Text = namedtuple("Text", ["text", "stats"])


class Paragraph:
    def __init__(self, el):
        self._text = ET.tostring(el, encoding="unicode", method="text")

    @property
    def text(self):
        return self._text.strip()

    @property
    def stats(self):
        return Stats(size=len([t for t in self.text.split(" ") if t != ""]))


class Page:
    def __init__(self, el):
        self._paragraphs = [Paragraph(p) for p in el.findall("{*}p")]

    @property
    def text(self):
        return "\n".join(p.text for p in self._paragraphs).strip()

    @property
    def stats(self):
        return Stats(size=sum(p.stats.size for p in self._paragraphs))


class StructuredText:
    def __init__(self, xml_string):
        root = ET.fromstring(xml_string)
        body = root.find("{*}body")
        self._pages = [
            Page(p)
            for p in body.findall("{*}div")
            if p.attrib.get("class", "") == "page"
        ]

    @property
    def text(self):
        return "\n".join(p.text for p in self._pages).strip()

    @property
    def stats(self):
        return Stats(size=sum(p.stats.size for p in self._pages))


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


def load_text_from_xml(path):
    print(path)
    with open(path, "r") as f:
        xml = f.read()
        return StructuredText(xml)


def load_text_from_txt(path):
    with open(path, "r") as f:
        text = f.read().lower()
        stats = Stats(size=len(text.split()))
        return Text(text=text, stats=stats)


def load_year(path, txt=True):
    year = Year()
    for text in os.listdir(path):
        text_path = os.path.join(path, text)
        if txt and os.path.isfile(text_path) and text.endswith(".txt"):
            text_name = ".".join(text.split(".")[:-1])
            year.set(text_name, load_text_from_txt(text_path))

        if os.path.isfile(text_path) and text.endswith(".xml"):
            text_name = ".".join(text.split(".")[:-1])
            year.set(text_name, load_text_from_xml(text_path))

    return year


def load_db(path, txt=True):
    db = Database()
    for year in os.listdir(path):
        year_path = os.path.join(path, year)
        if os.path.isdir(year_path):
            db.set(year, load_year(year_path, txt=txt))
    return db

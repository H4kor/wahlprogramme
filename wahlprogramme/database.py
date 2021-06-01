import os
from collections import namedtuple
import xml.etree.ElementTree as ET
import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

Stats = namedtuple("Stats", ["size"])
Text = namedtuple("Text", ["text", "stats"])
Meta = namedtuple("Meta", ["parties"])
MetaParty = namedtuple("MetaParty", ["name", "color"])


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

    @property
    def paragraphs(self):
        return self._paragraphs


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

    @property
    def pages(self):
        return self._pages


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
        self._meta = None

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

    @property
    def meta(self):
        return self._meta

    @property
    def party_colors(self):
        return {party: data.color for party, data in self._meta.parties.items()}

    @property
    def party_names(self):
        return {party: data.name for party, data in self._meta.parties.items()}

    def set_meta(self, data):
        self._meta = data


def load_text_from_xml(path):
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


def load_metadata(path):
    yaml_data = yaml.load(open(path, "r"), Loader=Loader)
    return Meta(
        parties={
            k: MetaParty(name=v["name"], color=v["color"])
            for k, v in yaml_data["parties"].items()
        }
    )


def load_db(path, txt=True):
    db = Database()
    meta_path = os.path.join(path, "meta.yml")

    # load meta data
    if os.path.isfile(meta_path):
        db.set_meta(load_metadata(meta_path))

    # load data
    for year in os.listdir(path):
        year_path = os.path.join(path, year)
        if os.path.isdir(year_path):
            db.set(year, load_year(year_path, txt=txt))
    return db

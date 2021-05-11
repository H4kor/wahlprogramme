# Wahlprogramme

(Braucht noch eine catchy Namen)

## Datenstruktur

* Ordner `2017` und `2021` enthalten die Wahlprogramme in Textformat
  * Jede Partei hat eine `.txt` Datei
  * Alle Daten werden beim Start der App geladen

## Daten Extraktion

* `python extract.py` transformiert alle PDFs in den Ordnern `2017` und `2021` in .txt Dateien

## Development Setup

Umgebung einrichten:

```
python3 venv venv
. venv/bin/activate
pip install -r requirements.txt
```

Debug Server starten:

```
FLASK_ENV=development flask run --reload
```
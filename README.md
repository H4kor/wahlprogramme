# [Wahlprogramme](https://wahlprogramme.rerere.org/)

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
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

Debug Server starten:

```
FLASK_ENV=development flask run --reload
```

## Quellen

### 2017

* [CDU](https://www.cdu.de/system/tdf/media/dokumente/170703regierungsprogramm2017.pdf?file=1])
* [SPD](https://www.spd.de/fileadmin/Dokumente/Bundesparteitag_2017/Es_ist_Zeit_fuer_mehr_Gerechtigkeit-Unser_Regierungsprogramm.pdf])
* [Die Grünen](https://www.gruene.de/fileadmin/user_upload/Dokumente/BUENDNIS_90_DIE_GRUENEN_Bundestagswahlprogramm_2017.pdf])
* [Die Linke](https://www.die-linke.de/fileadmin/download/wahlen2017/wahlprogramm2017/die_linke_wahlprogramm_2017.pdf])
* [FDP](https://www.fdp.de/sites/default/files/uploads/2017/08/07/20170807-wahlprogramm-wp-2017-v16.pdf])
* [AfD](https://www.afd.de/wp-content/uploads/sites/111/2017/06/2017-06-01_AfD-Bundestagswahlprogramm_Onlinefassung.pdf])

### 2021

* CDU noch nicht veröffentlicht.
* [SPD](https://www.spd.de/fileadmin/Dokumente/Beschluesse/Programm/SPD-Zukunftsprogramm.pdf)
* [Die Grünen](https://cms.gruene.de/uploads/documents/2021_Wahlprogrammentwurf.pdf)
* [Die Linke](https://www.die-linke.de/fileadmin/download/wahlen2021/BTWP21_Entwurf_Vorsitzende.pdf)
* [FDP](https://www.fdp.de/content/entwurf-fdp-bundestagswahlprogramm-2021)
* AfD noch nicht veröffentlicht.

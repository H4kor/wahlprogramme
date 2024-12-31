# [Wahlprogramme](https://wahlprogramme.rerere.org/)

(Braucht noch eine catchy Namen)

## Datenstruktur

* Ordner `2017` und `2021` enthalten die Wahlprogramme in Textformat
  * Jede Partei hat eine `.txt` Datei
  * Alle Daten werden beim Start der App geladen

## Daten Extraktion

* `pip install tika` tika installieren
* `python extract.py` transformiert alle PDFs in den Ordnern `2017` und `2021` in .txt Dateien

## Development Setup

Umgebung einrichten:

```
pipenv install
pipenv shell
```

Debug Server starten:

```
FLASK_APP=wahlprogramme FLASK_ENV=development flask run --reload
```

Tests:

```
pytest
```

## Quellen

### 2017

* [Union](https://www.cdu.de/system/tdf/media/dokumente/170703regierungsprogramm2017.pdf?file=1])
* [SPD](https://www.spd.de/fileadmin/Dokumente/Bundesparteitag_2017/Es_ist_Zeit_fuer_mehr_Gerechtigkeit-Unser_Regierungsprogramm.pdf])
* [Die Grünen](https://www.gruene.de/fileadmin/user_upload/Dokumente/BUENDNIS_90_DIE_GRUENEN_Bundestagswahlprogramm_2017.pdf])
* [Die Linke](https://www.die-linke.de/fileadmin/download/wahlen2017/wahlprogramm2017/die_linke_wahlprogramm_2017.pdf])
* [FDP](https://www.fdp.de/sites/default/files/uploads/2017/08/07/20170807-wahlprogramm-wp-2017-v16.pdf])
* [AfD](https://www.afd.de/wp-content/uploads/sites/111/2017/06/2017-06-01_AfD-Bundestagswahlprogramm_Onlinefassung.pdf])

### 2021

* [Union](https://www.csu.de/common/download/Regierungsprogramm.pdf)
* [SPD](https://www.spd.de/fileadmin/Dokumente/Beschluesse/Programm/SPD-Zukunftsprogramm.pdf)
* [Die Grünen](https://cms.gruene.de/uploads/documents/2021_Wahlprogrammentwurf.pdf)
* [Die Linke](https://www.die-linke.de/fileadmin/download/wahlen2021/BTWP21_Entwurf_Vorsitzende.pdf)
* [FDP](https://www.fdp.de/content/entwurf-fdp-bundestagswahlprogramm-2021)
* [AfD](https://www.afd.de/wp-content/uploads/2021/06/20210611_AfD_Programm_2021.pdf)


### 2025

* [SPD](https://www.bundestagswahl-bw.de/fileadmin/bundestagswahl-bw/2025/Wahlprogramme/BTW_2025_Wahlprogramm_SPD_Entwurf.pdf) (Entwurf)
* [Union](https://www.bundestagswahl-bw.de/fileadmin/bundestagswahl-bw/2025/Parteien_und_Spitzenkandidierende/btw_2025_wahlprogramm-cdu-csu.pdf)
* [Grüne](https://www.bundestagswahl-bw.de/fileadmin/bundestagswahl-bw/2025/Wahlprogramme/BTW_2025_Wahlprogramm_Gr%C3%BCne_Entwurf.pdf) (Entwurf)
* [FDP](https://www.bundestagswahl-bw.de/fileadmin/bundestagswahl-bw/2025/Wahlprogramme/BTW_2025_Wahlprogramm_FDP_Entwurf.pdf) (Entwurf)
* [Die Linke](https://www.bundestagswahl-bw.de/fileadmin/bundestagswahl-bw/2025/Parteien_und_Spitzenkandidierende/btw_2025_wahlprogramm_die_linke.pdf) (Entwurf)
* [AfD](https://www.bundestagswahl-bw.de/fileadmin/bundestagswahl-bw/2025/Wahlprogramme/AfD_Leitantrag-Bundestagswahlprogramm-2025.pdf) (Entwurf)
* [BSW](https://www.bundestagswahl-bw.de/fileadmin/bundestagswahl-bw/2025/Wahlprogramme/BTW_2025_BSW_Kurzwahlprogramm.pdf) (Entwurf)

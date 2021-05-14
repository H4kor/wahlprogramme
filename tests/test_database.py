from wahlprogramme import db, stats


def test_db_existence():
    assert db
    assert stats


def test_structure():
    for party in db:
        for year in db[party]:
            assert type(db[party][year]) is str
            assert type(stats[party][year]) is dict


def test_stats():
    for party in db:
        for year in db[party]:
            assert stats[party][year]["size"] != 0

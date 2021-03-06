# flake8: noqa: E712
from wahlprogramme.query import (
    parse_search_queries,
    count_query,
    count_search,
    Term,
    Query,
    Search,
)


def test_relative_true():
    assert parse_search_queries({"relative": "true"}).relative == True
    assert parse_search_queries({"relative": "True"}).relative == True


def test_relative_false():
    assert parse_search_queries({"relative": "false"}).relative == False
    assert parse_search_queries({"relative": None}).relative == False
    assert parse_search_queries({"relative": "False"}).relative == False
    assert parse_search_queries({"relative": ""}).relative == False
    assert parse_search_queries({"relative": "foo"}).relative == False
    assert parse_search_queries({}).relative == False


def test_queries_is_list():
    assert type(parse_search_queries({}).queries) is list
    assert type(parse_search_queries({"query": ""}).queries) is list
    assert type(parse_search_queries({"query": "foo"}).queries) is list
    assert type(parse_search_queries({"query": "foo,bar"}).queries) is list


def test_search_raw_query():
    assert parse_search_queries({}).raw_query == ""
    assert parse_search_queries({"query": ""}).raw_query == ""
    assert parse_search_queries({"query": "foo"}).raw_query == "foo"
    assert parse_search_queries({"query": "foo,bar"}).raw_query == "foo,bar"


def test_queries_len():
    assert len(parse_search_queries({}).queries) == 0
    assert len(parse_search_queries({"query": ""}).queries) == 0
    assert len(parse_search_queries({"query": "foo"}).queries) == 1
    assert len(parse_search_queries({"query": "foo,bar"}).queries) == 2


def test_exact_term():
    assert parse_search_queries({"query": "foo"}).queries[0].terms[0].exact == False
    assert parse_search_queries({"query": "'foo'"}).queries[0].terms[0].exact == True
    assert parse_search_queries({"query": '"foo"'}).queries[0].terms[0].exact == True


def test_query_raw_query():
    assert parse_search_queries({"query": "foo"}).queries[0].raw_query == "foo"
    assert parse_search_queries({"query": "'foo'"}).queries[0].raw_query == "'foo'"
    assert parse_search_queries({"query": '"foo"'}).queries[0].raw_query == '"foo"'


def test_multi_term():
    assert len(parse_search_queries({"query": "foo"}).queries[0].terms) == 1
    assert len(parse_search_queries({"query": "foo+bar"}).queries[0].terms) == 2
    assert len(parse_search_queries({"query": "foo+bar+foo"}).queries[0].terms) == 2
    assert len(parse_search_queries({"query": "foo+bar+baz"}).queries[0].terms) == 3
    assert len(parse_search_queries({"query": "'foo'+'bar'+baz"}).queries[0].terms) == 3


def test_terms_lower():
    assert parse_search_queries({"query": "Foo"}).queries[0].terms[0].term == "foo"
    assert parse_search_queries({"query": "'Foo'"}).queries[0].terms[0].term == "foo"
    assert parse_search_queries({"query": '"Foo"'}).queries[0].terms[0].term == "foo"
    assert (
        parse_search_queries({"query": '"FooBar"'}).queries[0].terms[0].term == "foobar"
    )


def test_multi_term_terms():
    terms = [
        t.term
        for t in parse_search_queries({"query": "'foo'+'bar'+baz"}).queries[0].terms
    ]
    assert "foo" in terms
    assert "bar" in terms
    assert "baz" in terms


def test_count_query():
    text = """
    Foo foobar,
    foofoo barbar
    foo.
    """
    assert (
        count_query(
            Query(
                raw_query="not_part_of_test",
                terms=[
                    Term(exact=False, term="foo"),
                    Term(exact=False, term="bar"),
                    Term(exact=True, term="barbar"),
                ],
            ),
            text,
        )
        == 9
    )


def test_count_search():
    text = """
    Foo foobar,
    foofoo barbar
    foo.
    """
    assert count_search(
        Search(
            relative=False,
            raw_query="not_part_of_test",
            queries=[
                Query(
                    raw_query="not_part_of_test",
                    terms=[
                        Term(exact=False, term="foo"),
                        Term(exact=False, term="bar"),
                        Term(exact=True, term="barbar"),
                    ],
                ),
                Query(
                    raw_query="not_part_of_test",
                    terms=[
                        Term(exact=True, term="bar"),
                        Term(exact=True, term="foobar"),
                    ],
                ),
            ],
        ),
        text,
    ) == [9, 1]


def test_term_found_in_text():
    text = """
    Foo foobar,
    foofoo barbar
    foo.
    """
    assert Term(exact=False, term="foo").found_in_text(text) == True
    assert Term(exact=False, term="baz").found_in_text(text) == False
    assert Term(exact=True, term="foobar").found_in_text(text) == True
    assert Term(exact=True, term="bar").found_in_text(text) == False


def test_term_count_in_text():
    text = """
    Foo foobar,
    foofoo barbar
    foo.
    """
    assert Term(exact=False, term="foo").count_in_text(text) == 5
    assert Term(exact=True, term="foo").count_in_text(text) == 2
    assert Term(exact=False, term="bar").count_in_text(text) == 3
    assert Term(exact=True, term="bar").count_in_text(text) == 0
    assert Term(exact=True, term="barbar").count_in_text(text) == 1
    assert Term(exact=True, term="foobar").count_in_text(text) == 1


def test_query_found_in_text():
    text = """
    Foo foobar,
    foofoo barbar
    foo.
    """
    # Empty -> False
    assert Query(raw_query="not_part_of_test", terms=[]).found_in_text(text) == False
    # False, True -> True
    assert (
        Query(
            raw_query="not_part_of_test",
            terms=[Term(exact=False, term="baz"), Term(exact=False, term="foo")],
        ).found_in_text(text)
        == True
    )
    # False, False -> False
    assert (
        Query(
            raw_query="not_part_of_test",
            terms=[Term(exact=False, term="baz"), Term(exact=True, term="bar")],
        ).found_in_text(text)
        == False
    )

# flake8: noqa: E712
from wahlprogramme.query import (
    parse_search_queries,
    count_term,
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


def test_count_term():
    text = """
    Foo foobar,
    foofoo barbar
    foo.
    """
    assert count_term(Term(exact=False, term="foo"), text) == 5
    assert count_term(Term(exact=True, term="foo"), text) == 2
    assert count_term(Term(exact=False, term="bar"), text) == 3
    assert count_term(Term(exact=True, term="bar"), text) == 0
    assert count_term(Term(exact=True, term="barbar"), text) == 1
    assert count_term(Term(exact=True, term="foobar"), text) == 1


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

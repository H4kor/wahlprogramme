import re
from collections import namedtuple


Term = namedtuple("Term", ["exact", "term"])
Query = namedtuple("Query", ["terms", "raw_query"])
Search = namedtuple("Search", ["relative", "queries", "raw_query"])


def str_to_term(s):
    exact = False
    if s[0] == "'" and s[-1] == "'":
        exact = True
    if s[0] == '"' and s[-1] == '"':
        exact = True

    term = s
    if exact:
        term = term[1:-1]

    return Term(exact=exact, term=term)


def str_to_query(s):
    terms = [str_to_term(t) for t in set(s.split("+")) if t != ""]

    return Query(terms=terms, raw_query=s)


def parse_search_queries(args):
    relative = args.get("relative", "false")
    if relative:
        relative = relative.strip().lower() == "true"
    else:
        relative = False

    queries = [str_to_query(q) for q in args.get("query", "").split(",") if q != ""]
    return Search(relative=relative, queries=queries, raw_query=args.get("query", ""))


def _count_exact_term(term, text):
    words = re.findall(r"[\w']+|[.,!?;]", text)
    return sum([1 for word in words if word == term])


def count_term(term, text):
    if term.exact:
        return _count_exact_term(term.term, text.lower())
    else:
        return len(re.findall(f"(?={term.term})", text.lower()))


def count_query(query, text):
    return sum([count_term(t, text) for t in query.terms])


def count_search(search, text):
    return [count_query(q, text) for q in search.queries]

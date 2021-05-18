import re
from collections import namedtuple

Search = namedtuple("Search", ["relative", "queries", "raw_query"])


class Term:
    def __init__(self, exact, term):
        self._exact = exact
        self._term = term

    @property
    def exact(self):
        return self._exact

    @property
    def term(self):
        return self._term

    def _count_exact_term(self, text):
        words = re.findall(r"[\w']+|[.,!?;]", text)
        return sum([1 for word in words if word == self._term])

    def count_in_text(self, text):
        if self._exact:
            return self._count_exact_term(text.lower())
        else:
            return len(re.findall(f"(?={self._term})", text.lower()))

    def found_in_text(self, text):
        # TODO: can be optimized
        return self.count_in_text(text) > 0


class Query:
    def __init__(self, terms, raw_query):
        self._terms = terms
        self._raw_query = raw_query

    @property
    def terms(self):
        return self._terms

    @property
    def raw_query(self):
        return self._raw_query

    def found_in_text(self, text):
        # TODO: can be optimized
        return any(t.found_in_text(text) for t in self._terms)


def str_to_term(s):
    exact = False
    if s[0] == "'" and s[-1] == "'":
        exact = True
    if s[0] == '"' and s[-1] == '"':
        exact = True

    term = s
    if exact:
        term = term[1:-1]

    return Term(exact=exact, term=term.lower())


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


def count_query(query, text):
    return sum([t.count_in_text(text) for t in query.terms])


def count_search(search, text):
    return [count_query(q, text) for q in search.queries]

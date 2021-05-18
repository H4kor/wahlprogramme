import io
import os
from collections import defaultdict
from flask import Flask, render_template, request, Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import seaborn as sns
from .query import parse_search_queries, count_query
from .database import load_db

sns.set()

DOMAIN = os.environ.get("WAHL_DOMAIN", "https://wahlprogramme.rerere.org")


def create_app(test_config=None):
    # load database
    db = load_db("data/", txt=False)

    party_names = {
        "union": "Union",
        "fdp": "FDP",
        "freiewähler": "Freie Wähler",
        "spd": "SPD",
        "afd": "AfD",
        "grüne": "Die Grünen",
        "linke": "Die Linke",
        "piraten": "Piraten",
    }

    party_colors = {
        "union": "#222222",
        "fdp": "#fbee31",
        "freiewähler": "#f59900",
        "spd": "#e2001a",
        "afd": "#009ee0",
        "grüne": "#46962b",
        "linke": "#d00060",
        "piraten": "#FF820A",
    }

    app = Flask(__name__)

    @app.route("/")
    def index_view():
        return render_template(
            "index.html",
            parties=db.parties,
            years=db.years,
            party_names=party_names,
            DOMAIN=DOMAIN,
        )

    @app.route("/party/<string:party>")
    def party_view(party):
        if party not in party_names:
            return "Not Found", 404

        search = parse_search_queries(request.args)
        image_url = f"/party/{party}.png?" + request.query_string.decode("utf-8")

        return render_template(
            "party.html",
            image_url=image_url,
            party_names=party_names,
            party=party,
            query=search.raw_query,
            relative=search.relative,
            DOMAIN=DOMAIN,
        )

    @app.route("/year/<string:year>")
    def year_view(year):
        if year not in db.years:
            return "Not Found", 404

        search = parse_search_queries(request.args)
        image_url = f"/year/{year}.png?" + request.query_string.decode("utf-8")

        return render_template(
            "year.html",
            image_url=image_url,
            year=year,
            query=search.raw_query,
            relative=search.relative,
            DOMAIN=DOMAIN,
        )

    @app.route("/year/<string:year>.png")
    def year_png(year):
        if year not in db.years:
            return "Not Found", 404
        search = parse_search_queries(request.args)

        data = {"x": [], "y": [], "hue": []}
        for query in search.queries:
            for party in db.get(year).parties:
                count = count_query(query, db.get(year).get(party).text)
                if search.relative:
                    count /= db.get(year).get(party).stats.size

                data["x"].append(query.raw_query)
                data["y"].append(count)
                data["hue"].append(party_names[party])

        fig = Figure(figsize=(12, 6))
        fig.suptitle(f"Wahlprogramme {year}")
        axis = fig.add_subplot(1, 1, 1)
        g = sns.barplot(
            data=data,
            x="x",
            y="y",
            hue="hue",
            hue_order=[party_names[p] for p in db.get(year).parties],
            palette=[party_colors[p] for p in db.get(year).parties],
            ax=axis,
        )
        # place the legend outside the figure/plot
        g.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        fig.tight_layout()
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype="image/png")

    @app.route("/party/<string:party>.png")
    def party_png(party):
        if party not in party_names:
            return "Not Found", 404
        search = parse_search_queries(request.args)

        data = {"x": [], "y": [], "hue": []}
        for query in search.queries:
            for year in db.years:
                if db.get(year).get(party):
                    count = count_query(query, db.get(year).get(party).text)
                    if search.relative:
                        count /= db.get(year).get(party).stats.size

                    data["hue"].append(query.raw_query)
                    data["y"].append(count)
                    data["x"].append(year)

        fig = Figure(figsize=(12, 6))
        fig.suptitle(f"Wahlprogramme {party_names[party]}")
        axis = fig.add_subplot(1, 1, 1)
        g = sns.barplot(data=data, x="x", y="y", hue="hue", ax=axis)
        g.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        fig.tight_layout()
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype="image/png")

    @app.route("/year/<string:year>/party/<string:party>")
    def year_party_view(year, party):
        search = parse_search_queries(request.args)

        results = []
        for query in search.queries:
            result = []
            program = db.get(year).get(party)
            for i, page in enumerate(program.pages):
                for paragraph in page.paragraphs:
                    if query.found_in_text(paragraph.text):
                        result.append((i, paragraph))

            results.append(result)

        return render_template(
            "year_party.html",
            results=list(zip(search.queries, results)),
            show_relative=False,
            year=year,
            party=party,
            party_names=party_names,
            query=search.raw_query,
            relative=search.relative,
            DOMAIN=DOMAIN,
        )

    ##
    # Return app
    ##
    return app

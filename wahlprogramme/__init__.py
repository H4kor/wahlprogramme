import io
import os
from flask import Flask, render_template, request, Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import seaborn as sns
from .query import parse_search_queries, count_query

sns.set()

DOMAIN = os.environ.get("WAHL_DOMAIN", "https://wahlprogramme.rerere.org")


def create_app(db, test_config=None):

    app = Flask(__name__)

    @app.route("/")
    def index_view():
        return render_template(
            "index.html",
            show_relative=True,
            parties=db.parties,
            years=db.years,
            party_names=db.party_names,
            DOMAIN=DOMAIN,
        )

    @app.route("/party/<string:party>")
    def party_view(party):
        if party not in db.parties:
            return "Not Found", 404

        search = parse_search_queries(request.args)
        query_params = request.query_string.decode("utf-8")
        image_url = f"/party/{party}.png?" + query_params
        years = [year for year in db.years if party in db.get(year).parties]

        return render_template(
            "party.html",
            show_relative=True,
            image_url=image_url,
            party_names=db.party_names,
            query_params=query_params,
            years=years,
            party=party,
            query=search.raw_query,
            relative=search.relative,
            DOMAIN=DOMAIN,
        )

    @app.route("/year/<string:year>")
    def year_view(year):
        if year not in db.years:
            return "Not Found", 404

        parties = db.get(year).parties

        search = parse_search_queries(request.args)
        query_params = request.query_string.decode("utf-8")
        image_url = f"/year/{year}.png?" + query_params

        return render_template(
            "year.html",
            show_relative=True,
            image_url=image_url,
            parties=parties,
            party_names=db.party_names,
            query_params=query_params,
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
                data["hue"].append(db.party_names[party])

        fig = Figure(figsize=(12, 6))
        fig.suptitle(f"Wahlprogramme {year}")
        axis = fig.add_subplot(1, 1, 1)
        g = sns.barplot(
            data=data,
            x="x",
            y="y",
            hue="hue",
            hue_order=[db.party_names[p] for p in db.get(year).parties],
            palette=[db.party_colors[p] for p in db.get(year).parties],
            ax=axis,
        )
        axis.set_xlabel("")
        axis.set_ylabel("Treffer")
        # place the legend outside the figure/plot
        g.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        fig.tight_layout()
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype="image/png")

    @app.route("/party/<string:party>.png")
    def party_png(party):
        if party not in db.party_names:
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
        fig.suptitle(f"Wahlprogramme {db.party_names[party]}")
        axis = fig.add_subplot(1, 1, 1)
        g = sns.barplot(data=data, x="x", y="y", hue="hue", ax=axis)
        g.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        fig.tight_layout()
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype="image/png")

    @app.route("/year/<string:year>/party/<string:party>")
    def year_party_view(year, party):
        if year not in db.years or party not in db.get(year).parties:
            return "Not Found", 404

        search = parse_search_queries(request.args)
        query_params = request.query_string.decode("utf-8")
        image_url = f"/year/{year}/party/{party}.png?" + query_params

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
            image_url=image_url,
            show_relative=False,
            year=year,
            party=party,
            party_names=db.party_names,
            query=search.raw_query,
            relative=search.relative,
            DOMAIN=DOMAIN,
        )

    @app.route("/year/<string:year>/party/<string:party>.png")
    def year_party_png(year, party):
        if year not in db.years or party not in db.get(year).parties:
            return "Not Found", 404

        search = parse_search_queries(request.args)

        data = {"x": [], "y": [], "hue": []}
        text = db.get(year).get(party)
        for query in search.queries:
            for i, page in enumerate(text.pages):
                count = count_query(query, page.text)

                # data["y"].append(count)
                for _ in range(count):
                    data["hue"].append(query.raw_query)
                    data["x"].append(i + 1)

        fig = Figure(figsize=(12, 3))
        fig.suptitle(f"Wahlprogramme {db.party_names[party]} {year}")
        axis = fig.add_subplot(1, 1, 1)
        g = sns.histplot(
            data=data, x="x", bins=range(len(text.pages)), hue="hue", ax=axis,
        )

        sns.move_legend(
            axis, "center left", bbox_to_anchor=(1, 0.5)
        )

        g.set(xlabel="Seite", ylabel="Anzahl")
        # g.set(xticks=range(1, len(text.pages) + 1)[2::8])
        fig.tight_layout()
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype="image/png")

    ##
    # Return app
    ##
    return app

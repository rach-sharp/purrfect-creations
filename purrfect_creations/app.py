import datetime
import os

from flask import Flask, render_template

from purrfect_creations import core, api_clients, config
from purrfect_creations.core_types import JSON

app = Flask(__name__)


@app.route("/api/health")
def health() -> str:
    return "ok"


@app.route("/api/statistics")
def statistics() -> JSON:
    airtable_client = api_clients.airtable_client.get_airtable_client(
        airtable_base=config.AIRTABLE_BASE,
        api_key=config.AIRTABLE_API_KEY,
    )
    now = datetime.datetime.now()
    aggregate_stats = core.get_aggregate_stats_from_airtable(
        airtable_client=airtable_client, now=now
    )

    return aggregate_stats.to_json()


@app.route("/dashboard")
def dashboard():
    airtable_client = api_clients.airtable_client.get_airtable_client(
        airtable_base=config.AIRTABLE_BASE,
        api_key=config.AIRTABLE_API_KEY,
    )
    now = datetime.datetime.now()
    aggregate_stats = core.get_aggregate_stats_from_airtable(
        airtable_client=airtable_client, now=now
    )

    return render_template("dashboard.html", aggregate_stats=aggregate_stats, now=now)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

"""
Route definitions for MindTrack.

Two pages: a logging form (index) and a dashboard showing trends
computed from all logged entries.
"""
from flask import Blueprint, render_template, request, redirect, url_for, current_app

from app.db import insert_entry, fetch_all_entries
from app.analytics import entries_to_dataframe, compute_trends, compute_summary
from app.charts import render_trend_chart

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET", "POST"])
def index():
    db_path = current_app.config["DATABASE"]

    if request.method == "POST":
        mood = int(request.form["mood"])
        sleep_hours = float(request.form["sleep_hours"])
        exercised = "exercised" in request.form
        notes = request.form.get("notes", "").strip()

        insert_entry(db_path, mood, sleep_hours, exercised, notes)
        return redirect(url_for("main.dashboard"))

    return render_template("index.html")


@main_bp.route("/dashboard")
def dashboard():
    db_path = current_app.config["DATABASE"]

    rows = fetch_all_entries(db_path)
    df = entries_to_dataframe(rows)
    df = compute_trends(df)
    summary = compute_summary(df)
    chart = render_trend_chart(df) if not df.empty else None

    entries = df.to_dict("records") if not df.empty else []

    return render_template(
        "dashboard.html",
        summary=summary,
        chart=chart,
        entries=list(reversed(entries)),
    )

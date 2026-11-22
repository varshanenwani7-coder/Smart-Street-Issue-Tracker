import os

from flask import Flask, redirect, render_template, request, send_from_directory, url_for

import config
from dashboard import Dashboard
from database import DatabaseManager
from detector import MLRoadDamageDetector
from duplicate import DuplicateDetector
from priority import PriorityScorer
from report_manager import ReportManager

app = Flask(__name__)

# Detector ek hi baar banta hai (model pehli prediction par load hota hai)
detector = MLRoadDamageDetector(config.MODEL_PATH)
duplicate_detector = DuplicateDetector(config.DUPLICATE_RADIUS_METERS)
priority_scorer = PriorityScorer()
dashboard = Dashboard(config.CHART_FOLDER)


def get_manager():
    """Har request ke liye naya database connection."""
    database = DatabaseManager(config.DATABASE_PATH)
    database.connect()
    manager = ReportManager(detector, duplicate_detector, priority_scorer,
                            database, config.UPLOAD_FOLDER)
    return manager, database


@app.route("/")
def home():
    manager, database = get_manager()
    reports = manager.filter_reports(request.args.get("status"), request.args.get("level"))
    database.close_connection()
    return render_template("index.html", reports=reports, statuses=config.STATUSES,
                           selected_status=request.args.get("status", ""),
                           selected_level=request.args.get("level", ""), result=None)


@app.route("/report", methods=["POST"])
def report():
    image = request.files.get("image")
    image_bytes = image.read() if image else b""
    manager, database = get_manager()
    result = manager.submit_report(
        image_bytes, image.filename if image else "",
        request.form.get("latitude"), request.form.get("longitude"),
        request.form.get("location", ""), request.form.get("description", ""))
    reports = manager.get_reports()
    database.close_connection()
    return render_template("index.html", reports=reports, statuses=config.STATUSES,
                           selected_status="", selected_level="", result=result)


@app.route("/report/<int:report_id>/status", methods=["POST"])
def update_status(report_id):
    new_status = request.form.get("status")
    if new_status in config.STATUSES:
        manager, database = get_manager()
        database.update_report(report_id, new_status)
        database.close_connection()
    return redirect(url_for("home"))


@app.route("/dashboard")
def show_dashboard():
    manager, database = get_manager()
    reports = manager.get_reports()
    database.close_connection()
    stats = dashboard.generate_statistics(reports)
    has_charts = dashboard.display_analytics(reports)
    return render_template("dashboard.html", stats=stats, has_charts=has_charts,
                           markers=dashboard.display_map(reports))


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(config.UPLOAD_FOLDER, filename)


if __name__ == "__main__":
    # TFLite apne threads banata hai, isliye reloader aur threads band rakhe hain
    app.run(debug=False, use_reloader=False, threaded=False)

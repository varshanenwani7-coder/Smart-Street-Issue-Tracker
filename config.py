import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "model", "model.tflite")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
CHART_FOLDER = os.path.join(BASE_DIR, "static", "charts")
DATABASE_PATH = os.path.join(BASE_DIR, "data", "reports.db")

DUPLICATE_RADIUS_METERS = 100
STATUSES = ["Pending", "In Progress", "Resolved"]

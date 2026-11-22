# Smart Street Issue Tracker

An AI-based street issue reporting app built for **AL-2001 Programming for AI** (Fall 2026, FAST-NUCES, Karachi).
A citizen uploads a road photo with its location, the system checks whether it really shows a pothole, rejects
duplicate reports, gives each report a priority score, and tracks it until it is resolved.

## Features

| Feature | How it works |
|---|---|
| **Report an issue** | Upload a road photo with latitude, longitude, location name and an optional description |
| **Pothole detection** | A TensorFlow Lite model classifies the photo as *Pothole* or *Normal*. The image is prepared with OpenCV and NumPy (RGB, 224x224, scaled to 0-1). Photos classified as *Normal* are not saved |
| **Duplicate detection** | A new report is rejected if an unresolved report of the same category exists within 100 m (Haversine distance between GPS points) |
| **Priority score (0-100)** | 50% model confidence + 30% safety words in the description (accident, injury, night...) + 20% important places in the location (school, hospital, highway...). 70+ is High, 40+ is Medium, otherwise Low |
| **Track and filter** | Reports are listed by priority and can be filtered by status and priority level. Status can be changed to Pending, In Progress or Resolved |
| **Dashboard** | Pandas statistics, two Matplotlib bar charts (by status and by priority level) and a map of all reports |
| **Storage** | SQLite database, created automatically on first run |

## Team and files

| Member | Files |
|---|---|
| **Bushra Batool** | `app.py`, `report.py`, `config.py`, `templates/`, `static/style.css` |
| **Varsha Nenwani** | `detector.py`, `priority.py`, `duplicate.py`, `model/model.tflite` |
| **Shanzay Rizwan** | `report_manager.py`, `database.py`, `dashboard.py` |

| File | Class | What it does |
|---|---|---|
| `report.py` | `IssueReport` | One street issue report |
| `detector.py` | `RoadDamageDetector` (abstract), `MLRoadDamageDetector` | Image processing and pothole classification |
| `duplicate.py` | `DuplicateDetector` | Distance-based duplicate check |
| `priority.py` | `PriorityScorer` | Priority score and level |
| `database.py` | `DatabaseManager` | Save, fetch and update reports in SQLite |
| `report_manager.py` | `ReportManager` | Runs the whole flow: detect, check duplicates, score, save, filter |
| `dashboard.py` | `Dashboard` | Statistics, charts and map data |
| `app.py` | Flask routes | Connects everything to the web pages |

## How to run

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser. The map on the Dashboard page needs internet (OpenStreetMap tiles).

## Credits

Developed by **Varsha Nenwani, Bushra Batool, and Shanzay Rizwan** as part of the AL-2001 Programming for AI course.

This project is our own implementation of an AI-based street issue reporting system, developed collaboratively by our team.

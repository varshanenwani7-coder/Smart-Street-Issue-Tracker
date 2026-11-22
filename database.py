import sqlite3


class DatabaseManager:
    """SQLite database: reports save, fetch aur update karta hai."""

    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                report_id      INTEGER PRIMARY KEY AUTOINCREMENT,
                image_path     TEXT,
                latitude       REAL,
                longitude      REAL,
                location       TEXT,
                description    TEXT,
                issue_category TEXT,
                confidence     REAL,
                priority_score INTEGER,
                status         TEXT,
                timestamp      TEXT
            )
        """)
        self.connection.commit()

    def save_report(self, report):
        cursor = self.connection.execute(
            "INSERT INTO reports (image_path, latitude, longitude, location, "
            "description, issue_category, confidence, priority_score, status, timestamp) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (report.image_path, report.latitude, report.longitude, report.location,
             report.description, report.issue_category, report.confidence,
             report.priority_score, report.status, report.timestamp))
        self.connection.commit()
        report.report_id = cursor.lastrowid
        return report.report_id

    def fetch_reports(self):
        rows = self.connection.execute(
            "SELECT * FROM reports ORDER BY priority_score DESC, timestamp DESC").fetchall()
        return [dict(row) for row in rows]

    def update_report(self, report_id, new_status):
        cursor = self.connection.execute(
            "UPDATE reports SET status = ? WHERE report_id = ?", (new_status, report_id))
        self.connection.commit()
        return cursor.rowcount > 0

    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None

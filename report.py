from datetime import datetime


class IssueReport:
    """Ek street issue report ka data (Lab 05: class, attributes, methods)."""

    def __init__(self, image_path, latitude, longitude, location="",
                 description="", issue_category="Pothole",
                 confidence=0.0, priority_score=0, status="Pending",
                 report_id=None, timestamp=None):
        self.report_id = report_id
        self.image_path = image_path
        self.latitude = latitude
        self.longitude = longitude
        self.location = location
        self.description = description
        self.issue_category = issue_category
        self.confidence = confidence
        self.priority_score = priority_score
        self.status = status
        self.timestamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M")

    def update_status(self, new_status):
        self.status = new_status

    def to_dict(self):
        return {
            "report_id": self.report_id,
            "image_path": self.image_path,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "location": self.location,
            "description": self.description,
            "issue_category": self.issue_category,
            "confidence": self.confidence,
            "priority_score": self.priority_score,
            "status": self.status,
            "timestamp": self.timestamp,
        }

    def display_report(self):
        return (f"Report #{self.report_id} | {self.issue_category} | "
                f"{self.location} | Priority {self.priority_score} | {self.status}")

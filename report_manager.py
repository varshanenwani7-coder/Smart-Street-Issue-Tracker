import os
import uuid

from report import IssueReport


class ReportManager:
    """Poora flow sambhalta hai: image -> detect -> duplicate check -> priority -> save."""

    def __init__(self, detector, duplicate_detector, priority_scorer, database, upload_folder):
        self.detector = detector
        self.duplicate_detector = duplicate_detector
        self.priority_scorer = priority_scorer
        self.database = database
        self.upload_folder = upload_folder

    def submit_report(self, image_bytes, filename, latitude, longitude, location, description):
        """Form se aaya data validate karke process_report() ko deta hai."""
        if not image_bytes:
            return {"ok": False, "message": "Please upload an image."}
        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except (TypeError, ValueError):
            return {"ok": False, "message": "Latitude and longitude must be numbers."}
        if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
            return {"ok": False, "message": "Latitude/longitude out of range."}
        try:
            return self.process_report(image_bytes, filename, latitude, longitude,
                                       location.strip(), description.strip())
        except (ValueError, FileNotFoundError) as error:
            return {"ok": False, "message": str(error)}

    def process_report(self, image_bytes, filename, latitude, longitude, location, description):
        result = self.detector.detect_damage(image_bytes)
        if result["label"] == "Normal":
            return {"ok": True, "saved": False,
                    "message": "No pothole detected in this image (confidence "
                               + str(result["confidence"]) + "%). Report not saved."}

        duplicates = self.duplicate_detector.check_duplicate(
            latitude, longitude, result["label"], self.database.fetch_reports())
        if duplicates:
            return {"ok": True, "saved": False, "duplicates": duplicates,
                    "message": "A similar issue is already reported nearby. Report not saved."}

        score = self.priority_scorer.calculate_priority(result["confidence"], description, location)
        extension = os.path.splitext(filename)[1].lower() or ".jpg"
        saved_name = uuid.uuid4().hex + extension
        with open(os.path.join(self.upload_folder, saved_name), "wb") as file:
            file.write(image_bytes)

        report = IssueReport(saved_name, latitude, longitude, location, description,
                             result["label"], result["confidence"], score)
        self.database.save_report(report)
        level = self.priority_scorer.assign_priority_level(score)
        return {"ok": True, "saved": True,
                "message": "Report saved: " + result["label"] + " (confidence "
                           + str(result["confidence"]) + "%), priority " + str(score)
                           + " (" + level + ")."}

    def get_reports(self):
        reports = self.database.fetch_reports()
        for r in reports:
            r["priority_level"] = self.priority_scorer.assign_priority_level(r["priority_score"])
        return reports

    def filter_reports(self, status=None, level=None):
        reports = self.get_reports()
        if status:
            reports = list(filter(lambda r: r["status"] == status, reports))
        if level:
            reports = list(filter(lambda r: r["priority_level"] == level, reports))
        return reports

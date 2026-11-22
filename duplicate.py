import math


class DuplicateDetector:
    """Same category ki report kisi purani report ke 100m ke andar ho to duplicate."""

    def __init__(self, distance_threshold=100):
        self.distance_threshold = distance_threshold  # meters

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """Haversine formula: do GPS points ke beech distance (meters)."""
        radius = 6371000
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        d_phi = math.radians(lat2 - lat1)
        d_lambda = math.radians(lon2 - lon1)
        a = (math.sin(d_phi / 2) ** 2
             + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2)
        return 2 * radius * math.asin(math.sqrt(a))

    def check_duplicate(self, latitude, longitude, category, existing_reports):
        duplicates = []
        for r in existing_reports:
            if r["issue_category"] != category or r["status"] == "Resolved":
                continue
            distance = self.calculate_distance(latitude, longitude,
                                               r["latitude"], r["longitude"])
            if distance <= self.distance_threshold:
                duplicates.append({"report_id": r["report_id"],
                                   "location": r["location"],
                                   "distance_m": round(distance, 1)})
        return duplicates

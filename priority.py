class PriorityScorer:
    """Priority score (0-100) = severity + safety risk + location importance."""

    def __init__(self, severity_weight=0.5, safety_weight=0.3, location_weight=0.2):
        self.severity_weight = severity_weight
        self.safety_weight = safety_weight
        self.location_weight = location_weight
        self.safety_words = ["accident", "danger", "dangerous", "injury", "bike",
                             "night", "deep", "car", "child", "fell"]
        self.important_places = ["school", "hospital", "main road", "highway",
                                 "market", "bridge", "chowk"]

    def _safety_score(self, description):
        text = description.lower()
        matches = sum(1 for word in self.safety_words if word in text)
        return min(matches * 25, 100)

    def _location_score(self, location):
        text = location.lower()
        matches = sum(1 for place in self.important_places if place in text)
        return min(matches * 50, 100)

    def calculate_priority(self, confidence, description, location):
        score = (confidence * self.severity_weight
                 + self._safety_score(description) * self.safety_weight
                 + self._location_score(location) * self.location_weight)
        return round(score)

    def assign_priority_level(self, score):
        if score >= 70:
            return "High"
        if score >= 40:
            return "Medium"
        return "Low"

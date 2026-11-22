import os

import matplotlib
matplotlib.use("Agg")  # bina window ke chart file mein save karne ke liye
import matplotlib.pyplot as plt
import pandas as pd


class Dashboard:
    """Pandas se statistics, Matplotlib se charts, aur map ka data."""

    def __init__(self, chart_folder):
        self.chart_folder = chart_folder

    def _to_dataframe(self, reports):
        return pd.DataFrame(reports)

    def generate_statistics(self, reports):
        if not reports:
            return {"total": 0, "pending": 0, "in_progress": 0, "resolved": 0}
        df = self._to_dataframe(reports)
        counts = df.groupby("status").size()
        return {"total": len(df),
                "pending": int(counts.get("Pending", 0)),
                "in_progress": int(counts.get("In Progress", 0)),
                "resolved": int(counts.get("Resolved", 0))}

    def display_analytics(self, reports):
        """Do charts banata hai: status ke hisaab se aur priority level ke hisaab se."""
        if not reports:
            return False
        df = self._to_dataframe(reports)
        self._bar_chart(df.groupby("status").size(), "Reports by status", "status.png")
        self._bar_chart(df.groupby("priority_level").size(), "Reports by priority level", "priority.png")
        return True

    def _bar_chart(self, series, title, filename):
        plt.figure(figsize=(5, 3.2))
        plt.bar(series.index, series.values, color="#2b6cb0")
        plt.title(title)
        plt.ylabel("Number of reports")
        plt.tight_layout()
        plt.savefig(os.path.join(self.chart_folder, filename))
        plt.close()

    def display_map(self, reports):
        """Leaflet map ke liye simple list of markers."""
        return [{"lat": r["latitude"], "lon": r["longitude"],
                 "label": r["issue_category"] + " - " + r["status"]
                          + " (priority " + str(r["priority_score"]) + ")"}
                for r in reports]

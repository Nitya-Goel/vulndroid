SEVERITY_WEIGHTS = {
    "Low": 2,
    "Medium": 5,
    "High": 8,
    "Critical": 10
}


class SeverityEngine:

    def calculate_risk_score(self, issues):
        total_score = 0

        for issue in issues:
            severity = issue.get("severity", "Low")
            total_score += SEVERITY_WEIGHTS.get(severity, 1)

        return total_score
    

    def normalize_risk_level(self, score):
        if score > 70:
            return "Critical"
        elif score > 40:
            return "High"
        elif score > 20:
            return "Medium"
        else:
            return "Low"

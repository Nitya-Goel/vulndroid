import re
import math

API_KEY_PATTERNS = [
    r'AIza[0-9A-Za-z\-_]{35}',          # Google API Key
    r'AKIA[0-9A-Z]{16}',                # AWS Access Key
    r'sk_live_[0-9a-zA-Z]{24}',         # Stripe live key
    r'eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+'  # JWT
]


def shannon_entropy(data):
    if not data:
        return 0
    prob = [float(data.count(c)) / len(data) for c in set(data)]
    entropy = - sum([p * math.log2(p) for p in prob])
    return entropy


class SecretDetector:

    def __init__(self, dx):
        self.dx = dx
        self.issues = []

    def detect_pattern_keys(self, source_code):
        for pattern in API_KEY_PATTERNS:
            matches = re.findall(pattern, source_code)
            for match in matches:
                self.issues.append({
                    "title": "Hardcoded API Key Detected",
                    "severity": "High",
                    "description": f"Possible secret found: {match[:10]}..."
                })

    def detect_high_entropy_strings(self, source_code):
        strings = re.findall(r'"(.*?)"', source_code)

        for s in strings:
            if len(s) > 20:
                entropy = shannon_entropy(s)
                if entropy > 4.5:
                    self.issues.append({
                        "title": "High Entropy String",
                        "severity": "Medium",
                        "description": "Suspicious high entropy string detected."
                    })

    def analyze(self):
        for method in self.dx.get_methods():
            try:
                source = method.get_source()
                if source:
                    self.detect_pattern_keys(source)
                    self.detect_high_entropy_strings(source)
            except:
                continue

        return self.issues
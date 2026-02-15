from androguard.misc import AnalyzeAPK

class CodeAnalyzer:
    def __init__(self, apk_path):
        self.apk_path = apk_path
        self.issues = []

    def analyze(self):
        try:
            a, d, dx = AnalyzeAPK(self.apk_path)

            for method in dx.get_methods():
                if method.is_external():
                    continue

                source = method.get_source()
                if source and "http://" in source:
                    self.issues.append({
                        "title": "Insecure HTTP Usage",
                        "severity": "Medium",
                        "description": f"HTTP usage found in {method.name}"
                    })

        except Exception as e:
            print("Code analysis error:", e)

        return self.issues
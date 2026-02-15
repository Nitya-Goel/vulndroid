OWASP_MAPPING = {
    "Hardcoded API Key Detected": "M1 - Improper Credential Usage",
    "High Entropy String": "M1 - Improper Credential Usage",
    "Weak Cryptography Used": "M5 - Insufficient Cryptography",
    "Insecure HTTP Usage": "M3 - Insecure Communication",
    "Exported Activity": "M2 - Insecure Communication",
    "App is Debuggable": "M7 - Reverse Engineering",
    "Allow Backup Enabled": "M9 - Insecure Data Storage",
    "Dangerous Permission Used": "M8 - Security Misconfiguration"
}


class OWASPMapper:

    def map_issues(self, issues):
        for issue in issues:
            title = issue.get("title")
            issue["owasp_category"] = OWASP_MAPPING.get(
                title,
                "M10 - Insufficient Security Controls"
            )
        return issues

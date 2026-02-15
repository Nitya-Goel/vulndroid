class ManifestAnalyzer:

    def __init__(self, apk):
        self.apk = apk

    def analyze(self):
        issues = []

        try:
            # Get AndroidManifest.xml as XML string
            manifest_xml = self.apk.get_android_manifest_xml()

            # Convert to string
            manifest_str = manifest_xml.toxml()

            # Check debuggable
            if 'android:debuggable="true"' in manifest_str:
                issues.append({
                    "title": "App is debuggable",
                    "severity": "High",
                    "description": "Application is built with android:debuggable=true",
                    "owasp_category": "M1: Improper Platform Usage"
                })

            # Check allowBackup
            if 'android:allowBackup="true"' in manifest_str:
                issues.append({
                    "title": "allowBackup Enabled",
                    "severity": "Medium",
                    "description": "Application allows backup of app data",
                    "owasp_category": "M2: Insecure Data Storage"
                })

        except Exception as e:
            print("Manifest parsing error:", e)

        return issues

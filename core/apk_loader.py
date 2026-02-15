from androguard.misc import AnalyzeAPK


class APKLoader:
    def __init__(self, apk_path):
        self.apk_path = apk_path
        self.apk = None
        self.dex = None
        self.analysis = None

    def load(self):
        try:
            self.apk, self.dex, self.analysis = AnalyzeAPK(self.apk_path)
            return True
        except Exception as e:
            print(f"[!] Failed to load APK: {e}")
            return False

    def get_basic_info(self):
        if not self.apk:
            return {}

        return {
            "package_name": self.apk.get_package(),
            "version_name": self.apk.get_androidversion_name(),
            "min_sdk": self.apk.get_min_sdk_version(),
            "target_sdk": self.apk.get_target_sdk_version(),
        }

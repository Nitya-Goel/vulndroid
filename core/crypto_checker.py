WEAK_CRYPTO = [
    "MD5",
    "SHA1",
    "DES",
    "AES/ECB",
]


class CryptoChecker:

    def __init__(self, dx):
        self.dx = dx
        self.issues = []

    def analyze(self):
        for method in self.dx.get_methods():
            try:
                source = method.get_source()
                if source:
                    for weak in WEAK_CRYPTO:
                        if weak in source:
                            self.issues.append({
                                "title": "Weak Cryptography Used",
                                "severity": "High",
                                "description": f"Weak algorithm detected: {weak}"
                            })
            except:
                continue

        return self.issues

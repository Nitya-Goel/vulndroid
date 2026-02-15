from flask import Flask, render_template, request, redirect, url_for
import os
from flask import send_file
from core.apk_loader import APKLoader
from core.manifest_analyzer import ManifestAnalyzer
from core.code_analyzer import CodeAnalyzer
from core.severity_engine import SeverityEngine

app = Flask(__name__, template_folder="templates")

print("TEMPLATE FOLDER:", app.template_folder)
print("CURRENT WORKING DIR:", os.getcwd())

app.config["UPLOAD_FOLDER"] = "uploads"

os.makedirs("uploads", exist_ok=True)




@app.route("/download")
def download():
    return send_file("report.html", as_attachment=True)

@app.route("/")
def index():
    return render_template("upload.html")


@app.route("/scan", methods=["POST"])
def scan():
    try:
        file = request.files["apkfile"]

        if file.filename == "":
            return "No file selected", 400

        if not file.filename.endswith('.apk'):
            return "Please upload a valid APK file", 400

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)
        
        print(f"[*] Saved APK to: {filepath}")
        print(f"[*] File exists: {os.path.exists(filepath)}")
        print(f"[*] File size: {os.path.getsize(filepath)} bytes")

        # Load APK
        loader = APKLoader(filepath)
        if not loader.load():
            return "Failed to load APK. Please ensure it's a valid APK file.", 500
            
        info = loader.get_basic_info()
        print(f"[*] APK Info: {info}")

        issues = []

        # Manifest Analysis
        try:
            manifest = ManifestAnalyzer(loader.apk)
            manifest_issues = manifest.analyze()
            issues.extend(manifest_issues)
            print(f"[*] Manifest issues found: {len(manifest_issues)}")
        except Exception as e:
            print(f"[!] Manifest analysis error: {e}")

        # Code Analysis
        try:
            code = CodeAnalyzer(filepath)
            code_issues = code.analyze()
            issues.extend(code_issues)
            print(f"[*] Code issues found: {len(code_issues)}")
        except Exception as e:
            print(f"[!] Code analysis error: {e}")

        print(f"[*] Total issues found: {len(issues)}")

        # Risk Score Calculation
        risk_score = min(len(issues) * 10, 100)  # Cap at 100
        
        if risk_score >= 80:
            risk_level = "Very High Risk 🔴"
        elif risk_score >= 60:
            risk_level = "High Risk 🟠"
        elif risk_score >= 40:
            risk_level = "Medium Risk 🟡"
        elif risk_score >= 20:
            risk_level = "Low Risk 🟢"
        else:
            risk_level = "Very Low Risk 💚"

        print(f"[*] Risk Score: {risk_score}")
        print(f"[*] Risk Level: {risk_level}")

        return render_template(
            "result.html",
            info=info,
            issues=issues,
            risk_score=risk_score,
            risk_level=risk_level
        )
        
    except Exception as e:
        print(f"[!] CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        return f"Error processing APK: {str(e)}", 500


if __name__ == "__main__":
    app.run(debug=True)
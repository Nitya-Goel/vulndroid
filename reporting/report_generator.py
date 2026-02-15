import os
from jinja2 import Environment, FileSystemLoader


class ReportGenerator:
    def __init__(self):
        template_path = os.path.join(
            os.path.dirname(__file__),
            "templates"
        )
        self.env = Environment(loader=FileSystemLoader(template_path))

    def generate_html(self, app_info, issues, risk_score, risk_level):
        template = self.env.get_template("report.html")

        html_content = template.render(
            app_info=app_info,
            issues=issues,
            risk_score=risk_score,
            risk_level=risk_level
        )

        output_path = "report.html"

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        return output_path

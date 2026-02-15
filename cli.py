import click
from rich.console import Console
from rich.table import Table

from core import manifest_analyzer
from core.apk_loader import APKLoader
from core.manifest_analyzer import ManifestAnalyzer
from core.code_analyzer import CodeAnalyzer
from core.secret_detector import SecretDetector
from core.crypto_checker import CryptoChecker
from core.owasp_mapper import OWASPMapper
from core.severity_engine import SeverityEngine
from reporting.report_generator import ReportGenerator


console = Console()


@click.command()
@click.argument("apk_path")
def scan(apk_path):
    console.print("[bold cyan]VulnDroid - Mobile App Security Analyzer[/bold cyan]")

    # ----------------------------
    # Load APK
    # ----------------------------
    loader = APKLoader(apk_path)

    if not loader.load():
        console.print("[red]Failed to load APK.[/red]")
        return

    info = loader.get_basic_info()

    console.print("\n[bold]App Information[/bold]")
    for key, value in info.items():
        console.print(f"{key}: {value}")

    # ----------------------------
    # 🔥 ADD THIS LINE HERE
    # ----------------------------
    issues = []

    # ----------------------------
    # Manifest Analysis
    # ----------------------------
    manifest_analyzer = ManifestAnalyzer(loader.apk)
    manifest_issues = manifest_analyzer.analyze()
    issues.extend(manifest_issues)


    # ----------------------------
    # Code Analysis
    # ----------------------------
    console.print("\n[bold cyan]Running Code Analysis...[/bold cyan]")

    code_analyzer = CodeAnalyzer(loader.analysis)
    secret_detector = SecretDetector(loader.analysis)
    crypto_checker = CryptoChecker(loader.analysis)

    code_issues = []
    code_issues += code_analyzer.analyze()
    code_issues += secret_detector.analyze()
    code_issues += crypto_checker.analyze()

    issues.extend(code_issues)

    # ----------------------------
    # OWASP Mapping
    # ----------------------------
    mapper = OWASPMapper()
    issues = mapper.map_issues(issues)

    # ----------------------------
    # Risk Calculation
    # ----------------------------
    severity_engine = SeverityEngine()

    risk_score = severity_engine.calculate_risk_score(issues)
    risk_level = severity_engine.normalize_risk_level(risk_score)

    console.print("\n[bold magenta]Overall Risk Assessment[/bold magenta]")
    console.print(f"Total Risk Score: {risk_score}")
    console.print(f"Risk Level: {risk_level}")

    # ----------------------------
    # Display Issues Table
    # ----------------------------
    if issues:
        table = Table(title="Detected Issues")

        table.add_column("Title")
        table.add_column("Severity")
        table.add_column("OWASP Category")
        table.add_column("Description")

        for issue in issues:
            table.add_row(
                issue.get("title", ""),
                issue.get("severity", ""),
                issue.get("owasp_category", ""),
                issue.get("description", "")
            )

        console.print(table)
    else:
        console.print("\n[green]No issues detected.[/green]")

    # ----------------------------
    # Generate HTML Report
    # ----------------------------
    report_gen = ReportGenerator()

    html_file = report_gen.generate_html(
        app_info=info,
        issues=issues,
        risk_score=risk_score,
        risk_level=risk_level
    )

    console.print(f"\n[bold green]Report Generated:[/bold green] {html_file}")


if __name__ == "__main__":
    scan()

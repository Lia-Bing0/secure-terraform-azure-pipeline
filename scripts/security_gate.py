import json
from pathlib import Path

CHECKOV_REPORT = Path("reports/checkov-report.json")
TRIVY_REPORT = Path("reports/trivy-report.json")
SUMMARY_REPORT = Path("reports/security-summary.md")


def load_json_report(report_path):
    if not report_path.exists():
        raise FileNotFoundError(f"Missing report: {report_path}")

    with report_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def extract_trivy_misconfigurations(trivy_report):
    findings = []

    for result in trivy_report.get("Results", []):
        for misconfig in result.get("Misconfigurations", []):
            findings.append({
                "id": misconfig.get("ID"),
                "title": misconfig.get("Title"),
                "severity": misconfig.get("Severity"),
                "resource": misconfig.get("CauseMetadata", {}).get("Resource"),
                "file": result.get("Target"),
                "description": misconfig.get("Description"),
                "resolution": misconfig.get("Resolution"),
            })

    return findings


def main():
    checkov_report = load_json_report(CHECKOV_REPORT)
    trivy_report = load_json_report(TRIVY_REPORT)

    checkov_summary = checkov_report.get("summary", {})
    checkov_results = checkov_report.get("results", {})

    passed = checkov_summary.get("passed", 0)
    failed = checkov_summary.get("failed", 0)
    skipped = checkov_summary.get("skipped", 0)

    checkov_failed_checks = checkov_results.get("failed_checks", [])
    trivy_findings = extract_trivy_misconfigurations(trivy_report)
    trivy_critical = sum(1 for finding in trivy_findings if finding.get("severity") == "CRITICAL")
    trivy_high = sum(1 for finding in trivy_findings if finding.get("severity") == "HIGH")
    trivy_medium = sum(1 for finding in trivy_findings if finding.get("severity") == "MEDIUM")
    trivy_low = sum(1 for finding in trivy_findings if finding.get("severity") == "LOW")

    markdown = [
        "# Security Gate Summary",
        "",
        "## Checkov Results",
        "",
        f"- Passed checks: {passed}",
        f"- Failed checks: {failed}",
        f"- Skipped checks: {skipped}",
        "",
        "## Checkov Failed Findings",
        "",
    ]

    if checkov_failed_checks:
        for finding in checkov_failed_checks:
          markdown.extend([
            "## Trivy IaC Findings",
            "",
            f"- Total findings: {len(trivy_findings)}",
            f"- Critical: {trivy_critical}",
            f"- High: {trivy_high}",
            f"- Medium: {trivy_medium}",
            f"- Low: {trivy_low}",
            "",
        ])
    else:
        markdown.append("No Checkov failed findings detected.")
        markdown.append("")

    markdown.extend([
        "## Trivy IaC Findings",
        "",
        f"- Total findings: {len(trivy_findings)}",
        "",
    ])

    if trivy_findings:
        for finding in trivy_findings:
            markdown.extend([
                f"### {finding.get('id')} - {finding.get('title')}",
                f"- Severity: `{finding.get('severity')}`",
                f"- Resource: `{finding.get('resource')}`",
                f"- File: `{finding.get('file')}`",
                f"- Resolution: {finding.get('resolution')}",
                "",
            ])
    else:
        markdown.append("No Trivy misconfiguration findings detected.")
        markdown.append("")

    SUMMARY_REPORT.write_text("\n".join(markdown), encoding="utf-8")

    print("Security gate summary generated.")
    print(f"Checkov Passed: {passed}")
    print(f"Checkov Failed: {failed}")
    print(f"Checkov Skipped: {skipped}")
    print(f"Trivy Findings: {len(trivy_findings)}")
    print(f"Trivy Critical: {trivy_critical}")
    print(f"Trivy High: {trivy_high}")
    print(f"Trivy Medium: {trivy_medium}")
    print(f"Trivy Low: {trivy_low}")

    if failed > 0 or trivy_critical > 0 or trivy_high > 0:
        print("Security gate failed due to Checkov failures or Trivy HIGH/CRITICAL findings.")
        exit(1)

    print("Security gate passed.")
    exit(0)


if __name__ == "__main__":
    main()
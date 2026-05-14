import json
from pathlib import Path

CHECKOV_REPORT = Path("reports/checkov-report.json")
SUMMARY_REPORT = Path("reports/security-summary.md")


def load_checkov_report():
    if not CHECKOV_REPORT.exists():
        raise FileNotFoundError(f"Missing report: {CHECKOV_REPORT}")

    with CHECKOV_REPORT.open("r", encoding="utf-8") as file:
        return json.load(file)


def main():
    report = load_checkov_report()

    summary = report.get("summary", {})
    results = report.get("results", {})

    passed = summary.get("passed", 0)
    failed = summary.get("failed", 0)
    skipped = summary.get("skipped", 0)

    failed_checks = results.get("failed_checks", [])

    markdown = [
        "# Security Gate Summary",
        "",
        "## Checkov Results",
        "",
        f"- Passed checks: {passed}",
        f"- Failed checks: {failed}",
        f"- Skipped checks: {skipped}",
        "",
        "## Failed Findings",
        "",
    ]

    if failed_checks:
        for finding in failed_checks:
            markdown.extend([
                f"### {finding.get('check_id')} - {finding.get('check_name')}",
                f"- Resource: `{finding.get('resource')}`",
                f"- File: `{finding.get('repo_file_path')}`",
                f"- Guideline: {finding.get('guideline')}",
                "",
            ])
    else:
        markdown.append("No failed findings detected.")

    SUMMARY_REPORT.write_text("\n".join(markdown), encoding="utf-8")

    print("Security gate summary generated.")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Skipped: {skipped}")

    if failed > 0:
        print("Security gate failed due to Checkov findings.")
        exit(1)

    print("Security gate passed.")
    exit(0)


if __name__ == "__main__":
    main()
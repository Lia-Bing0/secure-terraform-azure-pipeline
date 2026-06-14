import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKOV_REPORT = Path("reports/checkov-report.json")
TRIVY_REPORT = Path("reports/trivy-report.json")
SARIF_OUTPUT = Path("artifacts/sarif/security-results.sarif")


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        print(f"Skipping missing input file: {path}")
        return {}

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def severity_to_level(severity: str | None) -> str:
    severity = (severity or "").lower()

    if severity in {"critical", "high"}:
        return "error"
    if severity in {"medium", "moderate"}:
        return "warning"
    return "note"


def checkov_results_to_sarif(checkov_data: dict[str, Any]) -> list[dict[str, Any]]:
    results = []
    failed_checks = checkov_data.get("results", {}).get("failed_checks", [])

    for check in failed_checks:
        check_id = check.get("check_id", "UNKNOWN_CHECK")
        check_name = check.get("check_name", "Checkov finding")
        file_path = check.get("file_path", "unknown")
        line_range = check.get("file_line_range") or [1, 1]

        start_line = line_range[0] if len(line_range) > 0 else 1
        end_line = line_range[1] if len(line_range) > 1 else start_line

        results.append(
            {
                "ruleId": check_id,
                "level": severity_to_level(check.get("severity")),
                "message": {"text": check_name},
                "locations": [
                    {
                        "physicalLocation": {
                            "artifactLocation": {
                                "uri": file_path.lstrip("/")
                            },
                            "region": {
                                "startLine": start_line,
                                "endLine": end_line
                            },
                        }
                    }
                ],
                "properties": {
                    "source": "checkov",
                    "resource": check.get("resource"),
                    "guideline": check.get("guideline"),
                },
            }
        )

    return results


def trivy_results_to_sarif(trivy_data: dict[str, Any]) -> list[dict[str, Any]]:
    results = []

    for target in trivy_data.get("Results", []):
        file_path = target.get("Target", "unknown")

        for misconfiguration in target.get("Misconfigurations", []) or []:
            rule_id = misconfiguration.get("ID", "UNKNOWN_TRIVY_CHECK")
            title = misconfiguration.get("Title", "Trivy misconfiguration")
            severity = misconfiguration.get("Severity", "UNKNOWN")

            cause_metadata = misconfiguration.get("CauseMetadata", {}) or {}
            start_line = cause_metadata.get("StartLine", 1)
            end_line = cause_metadata.get("EndLine", start_line)

            results.append(
                {
                    "ruleId": rule_id,
                    "level": severity_to_level(severity),
                    "message": {
                        "text": title
                    },
                    "locations": [
                        {
                            "physicalLocation": {
                                "artifactLocation": {
                                    "uri": file_path
                                },
                                "region": {
                                    "startLine": start_line,
                                    "endLine": end_line
                                },
                            }
                        }
                    ],
                    "properties": {
                        "source": "trivy",
                        "severity": severity,
                        "description": misconfiguration.get("Description"),
                        "resolution": misconfiguration.get("Resolution"),
                        "status": misconfiguration.get("Status"),
                    },
                }
            )

    return results


def build_sarif(
    checkov_data: dict[str, Any],
    trivy_data: dict[str, Any],
) -> dict[str, Any]:
    checkov_results = checkov_results_to_sarif(checkov_data)
    trivy_results = trivy_results_to_sarif(trivy_data)

    combined_results = checkov_results + trivy_results

    return {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "secure-terraform-python-gate",
                        "informationUri": "https://github.com/",
                        "rules": [],
                    }
                },
                "automationDetails": {
                    "id": "secure-terraform-delivery-pipeline/phase-4a-sarif"
                },
                "invocations": [
                    {
                        "executionSuccessful": True,
                        "endTimeUtc": datetime.now(timezone.utc).isoformat(),
                    }
                ],
                "properties": {
                    "checkov_result_count": len(checkov_results),
                    "trivy_result_count": len(trivy_results),
                    "total_result_count": len(combined_results),
                },
                "results": combined_results,
            }
        ],
    }


def main() -> None:
    checkov_data = load_json(CHECKOV_REPORT)
    trivy_data = load_json(TRIVY_REPORT)

    SARIF_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    sarif = build_sarif(checkov_data, trivy_data)

    with SARIF_OUTPUT.open("w", encoding="utf-8") as file:
        json.dump(sarif, file, indent=2)

    total = sarif["runs"][0]["properties"]["total_result_count"]
    print(f"SARIF report generated: {SARIF_OUTPUT}")
    print(f"Total SARIF results: {total}")


if __name__ == "__main__":
    main()
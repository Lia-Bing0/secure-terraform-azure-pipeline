# Security Gate Summary

## Checkov Results

- Passed checks: 9
- Failed checks: 4
- Skipped checks: 1

## Checkov Failed Findings

## Trivy IaC Findings

- Total findings: 3
- Critical: 1
- High: 0
- Medium: 2
- Low: 0

## Trivy IaC Findings

- Total findings: 3
- Critical: 1
- High: 0
- Medium: 2
- Low: 0

## Trivy IaC Findings

- Total findings: 3
- Critical: 1
- High: 0
- Medium: 2
- Low: 0

## Trivy IaC Findings

- Total findings: 3
- Critical: 1
- High: 0
- Medium: 2
- Low: 0

## Trivy IaC Findings

- Total findings: 3

### AZU-0012 - The default action on Storage account network rules should be set to deny
- Severity: `CRITICAL`
- Resource: `azurerm_storage_account.sa`
- File: `main.tf`
- Resolution: Set network rules to deny

### AZU-0057 - Storage account should have logging enabled
- Severity: `MEDIUM`
- Resource: `azurerm_storage_account.sa`
- File: `main.tf`
- Resolution: Enable logging for at least one storage service (Queue, Table, or Blob)

### AZU-0061 - Storage account should have infrastructure encryption enabled
- Severity: `MEDIUM`
- Resource: `azurerm_storage_account.sa`
- File: `main.tf`
- Resolution: Enable infrastructure encryption for storage account

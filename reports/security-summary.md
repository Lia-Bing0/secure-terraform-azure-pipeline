# Security Gate Summary

## Checkov Results

- Passed checks: 9
- Failed checks: 4
- Skipped checks: 1

## Checkov Failed Findings

### CKV_AZURE_33 - Ensure Storage logging is enabled for Queue service for read, write and delete requests
- Resource: `azurerm_storage_account.sa`
- File: `/infra/main.tf`
- Guideline: https://docs.prismacloud.io/en/enterprise-edition/policy-reference/azure-policies/azure-logging-policies/enable-requests-on-storage-logging-for-queue-service

### CKV2_AZURE_33 - Ensure storage account is configured with private endpoint
- Resource: `azurerm_storage_account.sa`
- File: `/infra/main.tf`
- Guideline: https://docs.prismacloud.io/en/enterprise-edition/policy-reference/azure-policies/azure-general-policies/bc-azure-2-33

### CKV2_AZURE_38 - Ensure soft-delete is enabled on Azure storage account
- Resource: `azurerm_storage_account.sa`
- File: `/infra/main.tf`
- Guideline: https://docs.prismacloud.io/en/enterprise-edition/policy-reference/azure-policies/azure-general-policies/bc-azure-2-38

### CKV2_AZURE_1 - Ensure storage for critical data are encrypted with Customer Managed Key
- Resource: `azurerm_storage_account.sa`
- File: `/infra/main.tf`
- Guideline: https://docs.prismacloud.io/en/enterprise-edition/policy-reference/azure-policies/azure-general-policies/ensure-storage-for-critical-data-are-encrypted-with-customer-managed-key

## Trivy IaC Findings

- Total findings: 3
- Critical: 1
- High: 0
- Medium: 2
- Low: 0

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

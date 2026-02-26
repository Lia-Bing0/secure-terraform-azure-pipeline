# 00-env.ps1
# Shared variables for bootstrap scripts

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# === Edit these if you ever rename things ===
$env:AZ_RG_NAME           = "rg-lia-secure-tf-pipeline"
$env:AZ_LOCATION          = "eastus"
$env:TFSTATE_SA_NAME      = "liatfstateprod01"
$env:TFSTATE_CONTAINER    = "tfstate"

# GitHub repo coordinates - set these to your own repo where the GH Actions workflow lives
$env:GITHUB_OWNER         = "Lia-Bing0"
$env:GITHUB_REPO          = "secure-terraform-azure-pipeline"
$env:GITHUB_BRANCH        = "main"

# Entra app display name
$env:ENTRA_APP_NAME       = "gh-oidc-secure-tf-pipeline"

# Read subscription + tenant from current az context
$env:AZ_TENANT_ID         = (az account show --query tenantId -o tsv)
$env:AZ_SUBSCRIPTION_ID   = (az account show --query id -o tsv)
$env:AZ_SUBSCRIPTION_NAME = (az account show --query name -o tsv)

Write-Host "`n[env] Subscription: $($env:AZ_SUBSCRIPTION_NAME)"
Write-Host "[env] SubscriptionId: $($env:AZ_SUBSCRIPTION_ID)"
Write-Host "[env] TenantId: $($env:AZ_TENANT_ID)"
Write-Host "[env] RG: $($env:AZ_RG_NAME) ($($env:AZ_LOCATION))"
Write-Host "[env] Backend SA: $($env:TFSTATE_SA_NAME) / container: $($env:TFSTATE_CONTAINER)"
Write-Host "[env] GitHub: $($env:GITHUB_OWNER)/$($env:GITHUB_REPO) branch: $($env:GITHUB_BRANCH)`n"
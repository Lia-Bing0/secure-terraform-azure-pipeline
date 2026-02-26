# 01-backend-state.ps1
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

. "$PSScriptRoot\00-env.ps1"

$rg = $env:AZ_RG_NAME
$loc = $env:AZ_LOCATION
$sa = $env:TFSTATE_SA_NAME
$container = $env:TFSTATE_CONTAINER

Write-Host "[01] Ensuring resource group exists..."
az group create -n $rg -l $loc | Out-Null

Write-Host "[01] Ensuring backend storage account exists..."
$existing = az storage account show -n $sa -g $rg 2>$null
if (-not $existing) {
  az storage account create `
    -n $sa -g $rg -l $loc `
    --sku Standard_LRS `
    --kind StorageV2 `
    --https-only true `
    --min-tls-version TLS1_2 `
    --allow-blob-public-access false | Out-Null
  Write-Host "[01] Created storage account: $sa"
} else {
  Write-Host "[01] Storage account already exists: $sa"
}

Write-Host "[01] Ensuring tfstate container exists..."
# Use key mode for creation to avoid RBAC friction early; later RBAC handles login mode.
az storage container create `
  --name $container `
  --account-name $sa `
  --auth-mode key | Out-Null

Write-Host "[01] Done. Backend ready: $sa/$container"
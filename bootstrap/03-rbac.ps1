# 03-rbac.ps1 Permissions for Entra app to manage infra and backend state
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

. "$PSScriptRoot\00-env.ps1"

$appName = $env:ENTRA_APP_NAME
$rg      = $env:AZ_RG_NAME
$sa      = $env:TFSTATE_SA_NAME

# Find appId (client id)
$appId = az ad app list --filter "displayName eq '$appName'" --query "[0].appId" -o tsv
if (-not $appId) { throw "Entra app '$appName' not found. Run 02-oidc-entra.ps1 first." }

$rgId = az group show -n $rg --query id -o tsv
$saId = az storage account show -n $sa -g $rg --query id -o tsv

Write-Host "[03] Assigning Contributor on RG (scope: $rg)..."
# Ignore errors if assignment exists
az role assignment create --assignee $appId --role "Contributor" --scope $rgId 2>$null | Out-Null

Write-Host "[03] Assigning Storage Blob Data Contributor on backend state SA..."
az role assignment create --assignee $appId --role "Storage Blob Data Contributor" --scope $saId 2>$null | Out-Null

Write-Host "[03] Done."
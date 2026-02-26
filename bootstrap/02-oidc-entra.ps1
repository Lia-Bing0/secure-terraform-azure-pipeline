# 02-oidc-entra.ps1 where OIDC gets created
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

. "$PSScriptRoot\00-env.ps1"

$appName = $env:ENTRA_APP_NAME
$owner   = $env:GITHUB_OWNER
$repo    = $env:GITHUB_REPO
$branch  = $env:GITHUB_BRANCH

Write-Host "[02] Creating (or finding) Entra App Registration: $appName"

# Try to find existing app by display name
$appId = az ad app list --filter "displayName eq '$appName'" --query "[0].appId" -o tsv
if (-not $appId) {
  $appId = az ad app create --display-name $appName --query appId -o tsv
  Write-Host "[02] Created app. clientId(appId): $appId"
} else {
  Write-Host "[02] App already exists. clientId(appId): $appId"
}

Write-Host "[02] Ensuring Service Principal exists..."
$spId = az ad sp list --filter "appId eq '$appId'" --query "[0].id" -o tsv
if (-not $spId) {
  az ad sp create --id $appId | Out-Null
  $spId = az ad sp list --filter "appId eq '$appId'" --query "[0].id" -o tsv
  Write-Host "[02] Created service principal."
} else {
  Write-Host "[02] Service principal already exists."
}

# Build federated credential JSON (GitHub OIDC trust)
$tempJson = Join-Path $env:TEMP "federated-cred.json"
@"
{
  "name": "github-oidc-main",
  "issuer": "https://token.actions.githubusercontent.com",
  "subject": "repo:$owner/$repo:ref:refs/heads/$branch",
  "description": "GitHub Actions OIDC for $owner/$repo on branch $branch",
  "audiences": ["api://AzureADTokenExchange"]
}
"@ | Out-File $tempJson -Encoding utf8

Write-Host "[02] Creating federated credential (OIDC trust) if missing..."
# If already exists, don't duplicate
$fcExists = az ad app federated-credential list --id $appId --query "[?name=='github-oidc-main'] | length(@)" -o tsv
if ($fcExists -eq "0") {
  az ad app federated-credential create --id $appId --parameters $tempJson | Out-Null
  Write-Host "[02] Federated credential created."
} else {
  Write-Host "[02] Federated credential already exists."
}

Write-Host "`n[02] OUTPUTS (add these to GitHub Actions secrets):"
Write-Host "AZURE_CLIENT_ID=$appId"
Write-Host "AZURE_TENANT_ID=$($env:AZ_TENANT_ID)"
Write-Host "AZURE_SUBSCRIPTION_ID=$($env:AZ_SUBSCRIPTION_ID)`n"

# Save the client id for other scripts
$env:AZURE_CLIENT_ID = $appId
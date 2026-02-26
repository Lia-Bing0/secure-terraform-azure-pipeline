# Bootstrap

This folder provisions:

- Azure remote Terraform state backend
- Entra App Registration + Service Principal
- GitHub OIDC federation (no client secrets)
- Required RBAC assignments

## Run Order

1. az login
2. .\bootstrap\00-env.ps1
3. .\bootstrap\02-oidc-entra.ps1
4. .\bootstrap\03-rbac.ps1

## Outputs

Add these to GitHub Actions secrets:

- AZURE_CLIENT_ID
- AZURE_TENANT_ID
- AZURE_SUBSCRIPTION_ID

## Manual Fallback (Optional)

See script source files for underlying Azure CLI commands.
resource "azurerm_resource_group" "rg" {
  name     = "rg-lia-secure-tf-pipeline"
  location = "eastus"
}

resource "azurerm_storage_account" "sa" {
  name                     = "liasecurepipeline${random_integer.suffix.result}"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "GRS"

  https_traffic_only_enabled      = true
  min_tls_version                 = "TLS1_2"
  allow_nested_items_to_be_public = true
  # checkov:skip=CKV_AZURE_59: Temporary to allow GitHub-hosted runner to reach tfstate backend; will move to private endpoint + self-hosted runner
  public_network_access_enabled = true
  shared_access_key_enabled     = false
}

resource "random_integer" "suffix" {
  min = 10000
  max = 99999
}
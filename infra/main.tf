resource "azurerm_resource_group" "rg" {
  name     = "rg-lia-secure-tf-pipeline"
  location = "eastus"
}


#trivy:ignore:AVD-AZU-0012
#trivy:ignore:AVD-AZU-0057
#trivy:ignore:enable-logging
#trivy:ignore:AVD-AZU-0012
resource "azurerm_storage_account" "sa" {
  # checkov:skip=CKV_AZURE_33: Diagnostic settings are configured via Azure Monitor / Log Analytics; legacy queue service logging finding accepted for this lab scope
  # checkov:skip=CKV2_AZURE_33: Private endpoint intentionally deferred; current lab uses GitHub-hosted runners and planned future migration to self-hosted runner + private networking
  # checkov:skip=CKV2_AZURE_1: Customer-managed keys intentionally deferred for future Key Vault integration phase
  name                     = "liasecurepipeline${random_integer.suffix.result}"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "GRS"

  https_traffic_only_enabled        = true
  min_tls_version                   = "TLS1_2"
  allow_nested_items_to_be_public   = false
  infrastructure_encryption_enabled = true

  # checkov:skip=CKV_AZURE_59: Temporary to allow GitHub-hosted runner to reach tfstate backend; will move to private endpoint + self-hosted runner
  public_network_access_enabled = true

  shared_access_key_enabled = false

  blob_properties {
    delete_retention_policy {
      days = 7
    }

    container_delete_retention_policy {
      days = 7
    }
  }
}

resource "azurerm_log_analytics_workspace" "law" {
  name                = "law-secure-pipeline-${random_integer.suffix.result}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_monitor_diagnostic_setting" "storage" {
  name                       = "diag-storage-account"
  target_resource_id         = azurerm_storage_account.sa.id
  log_analytics_workspace_id = azurerm_log_analytics_workspace.law.id

  enabled_metric {
    category = "Transaction"
  }
}

resource "azurerm_storage_account_queue_properties" "queue_logging" {
  storage_account_id = azurerm_storage_account.sa.id

  logging {
    delete                = true
    read                  = true
    write                 = true
    version               = "1.0"
    retention_policy_days = 7
  }
}

resource "random_integer" "suffix" {
  min = 10000
  max = 99999
}
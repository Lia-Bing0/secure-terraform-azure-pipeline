terraform {
  required_version = ">= 1.6.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }

  backend "azurerm" {
    resource_group_name  = "rg-lia-secure-tf-pipeline"
    storage_account_name = "liatfstateprod01"
    container_name       = "tfstate"
    key                  = "secure-terraform-azure-pipeline.tfstate"
  }

}

provider "azurerm" {
  features {}
}
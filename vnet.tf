terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "3.11.0"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
  client_id       = var.client_id
  client_secret   = var.client_secret
  tenant_id       = var.tenant_id
}

resource "azurerm_resource_group" "rg-1" {
  name     = "vnet-RG"
  location = "East US"
}

resource "azurerm_virtual_network" "vnet-1" {
  name                = "vnet"
  location            = "East US"
  resource_group_name = azurerm_resource_group.rg-1.name
  address_space       = ["10.0.0.0/16"]
}

resource "azurerm_subnet" "subnet-1" {
  name                 = "subnet-1"
  virtual_network_name = azurerm_virtual_network.vnet-1.name
  resource_group_name  = azurerm_resource_group.rg-1.name
  address_prefixes     = ["10.0.1.0/24"]
}

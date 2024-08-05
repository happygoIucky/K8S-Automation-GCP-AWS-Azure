  variable "resource_group_name" {
  description = "jl-aks-rg"
  type        = string
}

variable "location" {
  description = "Location of the resources"
  type        = string
  default     = "Southeast Asia"
}

variable "storage_account_name" {
  description = "jlaksstorage"
  type        = string
}

variable "container_name" {
  description = "jlaksstoragecontainer"
  type        = string
}

provider "azurerm" {
  features {}
}

data "azurerm_resource_group" "existing" {
  name = var.resource_group_name
}

data "azurerm_storage_account" "existing" {
  name                = "jlaksstorage"
  resource_group_name = data.azurerm_resource_group.existing.name
}

data "azurerm_storage_container" "existing" {
  name                 = "jlaksstoragecontainer"
  storage_account_name = data.azurerm_storage_account.existing.name
}

# Retrieve the storage account key
data "azurerm_storage_account" "tfstate" {
  name                = "jlaksstorage"
  resource_group_name = data.azurerm_resource_group.existing.name
}

# Local value to store the access key
locals {
  storage_account_key = data.azurerm_storage_account.tfstate.primary_access_key
}

terraform {
  backend "azurerm" {
    resource_group_name   = "jl-aks-rg"
    storage_account_name  = "jlaksstorage"
    container_name        = "jlaksstoragecontainer"
    key                   = "terraform.tfstate"
  }
}

resource "azurerm_virtual_network" "vnet" {
  name                = "aks-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = data.azurerm_resource_group.existing.location
  resource_group_name = data.azurerm_resource_group.existing.name
}

resource "azurerm_subnet" "subnet" {
  name                 = "aks-subnet"
  resource_group_name  = data.azurerm_resource_group.existing.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.100.0/24"]
}

resource "azurerm_network_security_group" "nsg" {
  name                = "aks-nsg"
  location            = data.azurerm_resource_group.existing.location
  resource_group_name = data.azurerm_resource_group.existing.name
}

resource "azurerm_network_security_rule" "allow_inbound" {
  name                        = "Allow_HTTP_Inbound"
  priority                    = 100
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "80"
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  network_security_group_name = azurerm_network_security_group.nsg.name
  resource_group_name         = data.azurerm_resource_group.existing.name
}

resource "azurerm_kubernetes_cluster" "aks" {
  name                = "aks-cluster"
  location            = data.azurerm_resource_group.existing.location
  resource_group_name = data.azurerm_resource_group.existing.name
  dns_prefix          = "aksdns"

  default_node_pool {
    name       = "default"
    node_count = 1
    vm_size    = "Standard_DS2_v2"

    vnet_subnet_id = azurerm_subnet.subnet.id
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin = "azure"
    network_policy = "azure"
    service_cidr   = "10.1.0.0/16"
    dns_service_ip = "10.1.0.10"
  }
}

resource "azurerm_kubernetes_cluster_node_pool" "agentpool" {
  name                  = "agentpool"
  kubernetes_cluster_id = azurerm_kubernetes_cluster.aks.id
  vm_size               = "Standard_DS2_v2"
  node_count            = 1
  vnet_subnet_id        = azurerm_subnet.subnet.id
}

resource "random_string" "random" {
  length  = 8
  special = false
}
  

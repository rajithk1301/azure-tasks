from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.storage import StorageManagementClient


tenant_id = "0000-0000-0000-0000"
client_id = "0000-0000-0000-0000"
client_secret = "0000-0000-0000-0000"
subscription_id = "0000-0000-0000-0000"

credential = ClientSecretCredential(tenant_id, client_id, client_secret)

resource_client = ResourceManagementClient(credential, subscription_id)

RESOURCE_GROUP_NAME = "demo-rg"
LOCATION = "eastus"

rg = resource_client.resource_groups.create_or_update(RESOURCE_GROUP_NAME,
    {
        "location": LOCATION
    }
)

print(f"Resource Group {rg.name} created.")


network_client = NetworkManagementClient(credential, subscription_id)

VNET_NAME = "vnet-1"

poller = network_client.virtual_networks.begin_create_or_update(RESOURCE_GROUP_NAME,
    VNET_NAME,
    {
        "location": LOCATION,
        "address_space": {
            "address_prefixes": ["10.0.0.0/16"]
        }
    }
)
vnet = poller.result()
print(f"Virtual Network {vnet.name} created.")


SUBNET_NAME = "subnet-1"

poller = network_client.subnets.begin_create_or_update(RESOURCE_GROUP_NAME,
    VNET_NAME,
    SUBNET_NAME,
    {
        "address_prefix": "10.0.1.0/24"
    }
)
subnet = poller.result()
print(f"Subnet {subnet.name} created.")

PUBLIC_IP_NAME = "vm-ip"
IP_PARAMETERS = {
        "location": LOCATION,
        "sku": {"name": "Standard"},
        "public_ip_allocation_method": "Static",
        "public_ip_address_version": "IPV4"
    }

poller = network_client.public_ip_addresses.begin_create_or_update(RESOURCE_GROUP_NAME, PUBLIC_IP_NAME, IP_PARAMETERS)
public_ip = poller.result()
print(f"Public IP Address: {public_ip.ip_address}")


NIC_NAME = "vm-nic"
NIC_PARAMETERS = {
        "location": LOCATION,
        "ip_configurations": [{
            "name": "ip-config",
            "subnet": {"id": subnet.id},
            "public_ip_address": {"id": public_ip.id}
        }]
    }

poller = network_client.network_interfaces.begin_create_or_update(RESOURCE_GROUP_NAME, NIC_NAME, NIC_PARAMETERS)
nic = poller.result()
print(f"Network Interface {nic.name} created.")


compute_client = ComputeManagementClient(credential, subscription_id)

VM_NAME = "my-vm"
VM_PARAMETERS = {
        "location": LOCATION,
        "storage_profile": {
            "image_reference": {
                "publisher": "Canonical",
                "offer": "UbuntuServer",
                "sku": "16.04.0-LTS",
                "version": "latest"
            }
        },
        "hardware_profile": {
            "vm_size": "Standard_DS1_v2"
        },
        "os_profile": {
            "computer_name": VM_NAME,
            "admin_username": "azureuser",
            "admin_password": "P@33word"
        },
        "network_profile": {
            "network_interfaces": [{
                "id": nic.id,
            }]
        }
    }

poller = compute_client.virtual_machines.begin_create_or_update(RESOURCE_GROUP_NAME, VM_NAME, VM_PARAMETERS)
vm = poller.result()
print(f"Virtual machine {vm.name} created.")


storage_client = StorageManagementClient(credential, subscription_id)

STORAGE_ACCOUNT_NAME = "mystrgacnt1122py"
STORAGE_PARAMETERS = {
    "location": LOCATION,
    "kind": "StorageV2",
    "sku": {"name": "Standard_LRS"}
}

poller = storage_client.storage_accounts.begin_create(RESOURCE_GROUP_NAME, STORAGE_ACCOUNT_NAME, STORAGE_PARAMETERS)
storage_account = poller.result()
print(f"Storage Account {storage_account.name} created.")

CONTAINER_NAME = "blob-container"
container = storage_client.blob_containers.create(RESOURCE_GROUP_NAME, STORAGE_ACCOUNT_NAME, CONTAINER_NAME,
    {
        "container_access_type": "Private"
    }
)
print(f"Blob Container {container.name} created.")
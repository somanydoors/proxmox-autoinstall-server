# Proxmox Autoinstall Answer Server

Containerized Proxmox Autoinstall answer file server. Created using code sourced from the [Proxmox wiki](https://pve.proxmox.com/wiki/Automated_Installation#Serving_Answer_Files_via_HTTP).

## Building

To build the image, run:

`docker build -t proxmox-autoinstall-server .`

## Usage

1. [Create a Proxmox install ISO pointed at your server's IP or hostname]()
2. `mkdir config`
3. Create `config/default.toml`
4. For each host, create `answer-files/answers/${MAC_ADDRESS}.toml`
5. Run `docker run --name proxmox-autoinstall-server -p 8000:8000 -d somanydoors/proxmox-autoinstall-server`

### Template Answer File

More information on answer file formatting and capabilities can be found in the [Proxmox wiki](https://pve.proxmox.com/wiki/Automated_Installation#Answer_File_Format_2).

```toml
[global]
keyboard = "de"
country = "at"
fqdn = "pveauto.testinstall"
mailto = "mail@no.invalid"
timezone = "Europe/Vienna"
root_password = "123456"
root_ssh_keys = [
    "ssh-ed25519 AAAA..."
]

[network]
source = "from-dhcp"

[disk-setup]
filesystem = "zfs"
zfs.raid = "raid1"
disk_list = ["sda", "sdb"]
```
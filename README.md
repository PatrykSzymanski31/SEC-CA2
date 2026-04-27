# SEC-CA2 README

## Prerequisites

Before running the solution, make sure the following are in place:

- VirtualBox VM running Ubuntu Server LTS
- Docker installed
- Docker Compose installed
- Internet access for pulling container images
- VirtualBox NAT port forwarding configured for the required ports
- Optional: SSH access enabled for easier management

## Connect to the VM

From the host machine terminal, connect to the Ubuntu VM using:

```bash
ssh -p 2222 vboxuser@127.0.0.1

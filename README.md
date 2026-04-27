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


## Begin
Move into the project folder

```bash
cd ~/SEC-CA2

To build and start the environment, run:

```bash
docker compose up -d --build

To confirm that all services are running:

```bash
docker compose ps

## Access the services

After the stack has started, the services can be accessed from the host machine using the following URLs.

### Main Web Application
- URL: [https://127.0.0.1:8443](https://127.0.0.1:8443)  
- Login method: Keycloak SSO  
- User account: `marc`  
- Admin account: `eve`  
- Note: Use the credentials configured in Keycloak for these users.

### Keycloak Admin Console
- URL: [https://127.0.0.1:8443/keycloak/admin/](https://127.0.0.1:8443/keycloak/admin/)  
- Username: `admin`  
- Password: `admin123!`

### Dozzle
- URL: [http://127.0.0.1:9999](http://127.0.0.1:9999)  
- Login: none required

### Prometheus
- URL: [http://127.0.0.1:9090](http://127.0.0.1:9090)  
- Login: none required

### Grafana
- URL: [http://127.0.0.1:3000](http://127.0.0.1:3000)  
- Username: `admin`  
- Password: `admin123`

### Traefik Dashboard
- URL: [http://127.0.0.1:8080](http://127.0.0.1:8080)  
- Login: none required

## HTTPS Note

The solution uses a self-signed certificate for local HTTPS access. When opening the HTTPS services in a browser, a certificate warning may appear. This is expected in the lab environment. Continue past the warning to access the service.

## External Access

External access was demonstrated using a Cloudflare Quick Tunnel. When the tunnel is started, a temporary `trycloudflare.com` URL is generated in the terminal. This URL can be used to access the main web application externally for testing and screencast purposes.

## Logs and Monitoring

### Dozzle
Dozzle is used to view live Docker container logs.

### Prometheus
Prometheus is used to collect metrics from the monitoring stack.

### Grafana
Grafana is used to visualise Prometheus metrics through dashboards.

## Security Testing Artefacts

Trivy image scan outputs are stored in:

```text
security/trivy/

OWASP ZAP baseline scan outputs are stored in:

```text
security/zap/

## Stopping the Solution

To stop the running containers, use:

```bash
docker compose down

Do not use "docker compose down -v" unless you intentionally want to remove persisted volumes.

## Troubleshooting

If the containers are not running correctly, use the following commands to inspect the stack:

```bash
docker compose ps
docker compose logs

To restart the environment, run:

```bash
docker compose up -d

If Keycloak is slow to start, wait for it to finish booting before attempting login through the main application.

If services are inaccessible from the host machine, confirm that the required VirtualBox NAT port forwarding rules are configured correctly for the relevant ports.


#!/bin/bash

set -e

echo "Verifying SEC-CA2 environment..."

echo ""
echo "Checking running containers:"
docker compose ps

echo ""
echo "Checking main web application:"
curl -k -I https://127.0.0.1:8443 || echo "Main web application check failed."

echo ""
echo "Checking Dozzle:"
curl -I http://127.0.0.1:9999 || echo "Dozzle check failed."

echo ""
echo "Checking Prometheus:"
curl -I http://127.0.0.1:9090 || echo "Prometheus check failed."

echo ""
echo "Checking Grafana:"
curl -I http://127.0.0.1:3000 || echo "Grafana check failed."

echo ""
echo "Checking Traefik dashboard:"
curl -I http://127.0.0.1:8080 || echo "Traefik dashboard check failed."

echo ""
echo "Verification complete."

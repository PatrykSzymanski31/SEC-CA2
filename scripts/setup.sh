#!/bin/bash

set -e

echo "Starting SEC-CA2 setup..."

echo "Checking Docker..."
docker --version

echo "Checking Docker Compose..."
docker compose version

echo "Building and starting containers..."
docker compose up -d --build

echo "Waiting for services to start..."
sleep 10

echo "Current container status:"
docker compose ps

echo "Setup complete."
echo "Main application should be available at:"
echo "https://127.0.0.1:8443"

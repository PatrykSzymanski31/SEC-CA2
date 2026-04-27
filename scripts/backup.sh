#!/bin/bash

set -e

BACKUP_DIR="backups/backup-$(date +%Y%m%d-%H%M%S)"

echo "Creating backup in $BACKUP_DIR..."

mkdir -p "$BACKUP_DIR"

echo "Backing up project configuration files..."

cp docker-compose.yml "$BACKUP_DIR/" 2>/dev/null || true
cp .env "$BACKUP_DIR/" 2>/dev/null || true

if [ -d "security" ]; then
    cp -r security "$BACKUP_DIR/"
fi

if [ -d "traefik" ]; then
    cp -r traefik "$BACKUP_DIR/"
fi

if [ -d "keycloak" ]; then
    cp -r keycloak "$BACKUP_DIR/"
fi

echo "Backing up Docker volumes..."

mkdir -p "$BACKUP_DIR/volumes"

for volume in $(docker volume ls --format "{{.Name}}" | grep "sec-ca2" || true); do
    echo "Backing up volume: $volume"

    docker run --rm \
        -v "$volume":/volume \
        -v "$(pwd)/$BACKUP_DIR/volumes":/backup \
        alpine \
        tar czf "/backup/$volume.tar.gz" -C /volume .
done

echo "Backup complete:"
echo "$BACKUP_DIR"

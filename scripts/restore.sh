#!/bin/bash

set -e

if [ -z "$1" ]; then
    echo "Usage: ./scripts/restore.sh backups/backup-folder-name"
    exit 1
fi

BACKUP_DIR="$1"

if [ ! -d "$BACKUP_DIR" ]; then
    echo "Backup directory does not exist: $BACKUP_DIR"
    exit 1
fi

echo "Restoring backup from $BACKUP_DIR..."

echo "Stopping containers..."
docker compose down

echo "Restoring project configuration files..."

cp "$BACKUP_DIR/docker-compose.yml" . 2>/dev/null || true
cp "$BACKUP_DIR/.env" . 2>/dev/null || true

if [ -d "$BACKUP_DIR/security" ]; then
    rm -rf security
    cp -r "$BACKUP_DIR/security" .
fi

if [ -d "$BACKUP_DIR/traefik" ]; then
    rm -rf traefik
    cp -r "$BACKUP_DIR/traefik" .
fi

if [ -d "$BACKUP_DIR/keycloak" ]; then
    rm -rf keycloak
    cp -r "$BACKUP_DIR/keycloak" .
fi

echo "Restoring Docker volumes..."

if [ -d "$BACKUP_DIR/volumes" ]; then
    for archive in "$BACKUP_DIR"/volumes/*.tar.gz; do
        [ -e "$archive" ] || continue

        volume_name=$(basename "$archive" .tar.gz)

        echo "Restoring volume: $volume_name"

        docker volume create "$volume_name"

        docker run --rm \
            -v "$volume_name":/volume \
            -v "$(pwd)/$BACKUP_DIR/volumes":/backup \
            alpine \
            sh -c "cd /volume && tar xzf /backup/$(basename "$archive")"
    done
fi

echo "Starting containers again..."
docker compose up -d

echo "Restore complete."
docker compose ps


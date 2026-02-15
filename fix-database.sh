#!/bin/bash
# Database Fix Script for Cyber Vault

echo "╔════════════════════════════════════════════════════════════╗"
echo "║         DATABASE INITIALIZATION FIX SCRIPT                 ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Stop the container
echo "1. Stopping container..."
docker-compose -f docker-compose-python.yml down

# Remove the old volume (this will delete existing data!)
echo ""
echo "⚠️  WARNING: This will delete any existing data!"
read -p "Do you want to continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Aborted."
    exit 1
fi

echo ""
echo "2. Removing old database volume..."
docker volume rm cyber-vault-python_vault-data 2>/dev/null || echo "   (No existing volume found)"

# Rebuild and start
echo ""
echo "3. Rebuilding and starting container..."
docker-compose -f docker-compose-python.yml up -d --build

# Wait for container to start
echo ""
echo "4. Waiting for container to start..."
sleep 5

# Check health
echo ""
echo "5. Checking database health..."
curl -s http://localhost:8080/health | python3 -m json.tool || echo "   (Health check failed - container may still be starting)"

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                    FIX COMPLETE!                           ║"
echo "╠════════════════════════════════════════════════════════════╣"
echo "║  Try accessing: http://localhost:8080                     ║"
echo "║  Check logs: docker-compose -f docker-compose-python.yml logs -f"
echo "╚════════════════════════════════════════════════════════════╝"

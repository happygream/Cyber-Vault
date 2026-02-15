#!/bin/bash

# Cyber Vault - Easy Deployment Script
# This script makes deployment even easier

echo "╔════════════════════════════════════════════════════════════╗"
echo "║           ⚡ CYBER VAULT - DEPLOYMENT SYSTEM ⚡             ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ ERROR: Docker is not installed"
    echo "   Please install Docker first: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is available
if ! docker compose version &> /dev/null; then
    echo "❌ ERROR: Docker Compose is not available"
    echo "   Please install Docker Compose"
    exit 1
fi

echo "✓ Docker is installed"
echo "✓ Docker Compose is available"
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    
    # Generate a random secret key
    if command -v python3 &> /dev/null; then
        SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
        sed -i.bak "s/change-this-to-a-random-secret-key/$SECRET_KEY/" .env
        rm .env.bak 2>/dev/null
        echo "✓ Generated random SECRET_KEY"
    else
        echo "⚠ Please manually set SECRET_KEY in .env file"
    fi
fi

echo ""
echo "🚀 Starting Cyber Vault..."
echo ""

# Build and start the container
docker compose -f docker-compose-python.yml up -d --build

# Check if successful
if [ $? -eq 0 ]; then
    echo ""
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║                  ✓ DEPLOYMENT SUCCESSFUL                   ║"
    echo "╠════════════════════════════════════════════════════════════╣"
    echo "║                                                            ║"
    echo "║  🌐 Access your vault at: http://localhost:8080           ║"
    echo "║                                                            ║"
    echo "║  📊 View logs:      docker compose -f docker-compose-python.yml logs -f"
    echo "║  🛑 Stop vault:     docker compose -f docker-compose-python.yml down"
    echo "║  🔄 Restart vault:  docker compose -f docker-compose-python.yml restart"
    echo "║                                                            ║"
    echo "╚════════════════════════════════════════════════════════════╝"
else
    echo ""
    echo "❌ Deployment failed. Check the logs above for errors."
    exit 1
fi

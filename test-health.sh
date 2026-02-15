#!/bin/bash

echo "╔════════════════════════════════════════════════════════════╗"
echo "║           CYBER VAULT - HEALTH CHECK SCRIPT                ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if container is running
echo "1. Checking container status..."
if docker ps | grep -q cyber-vault-python; then
    echo "   ✓ Container is running"
else
    echo "   ✗ Container is NOT running"
    echo ""
    echo "   Start it with: docker-compose -f docker-compose-python.yml up -d"
    exit 1
fi

echo ""
echo "2. Checking application logs..."
echo "   Last 10 lines:"
echo "   ─────────────────────────────────────────────────────────"
docker-compose -f docker-compose-python.yml logs --tail=10 | sed 's/^/   /'
echo "   ─────────────────────────────────────────────────────────"

echo ""
echo "3. Testing HTTP endpoint..."
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/ 2>/dev/null)

if [ "$response" = "200" ]; then
    echo "   ✓ HTTP endpoint responding (Status: $response)"
else
    echo "   ✗ HTTP endpoint not responding properly (Status: $response)"
fi

echo ""
echo "4. Testing health endpoint..."
health=$(curl -s http://localhost:8080/health 2>/dev/null)

if [ -n "$health" ]; then
    echo "   Response: $health"
    if echo "$health" | grep -q "healthy"; then
        echo "   ✓ Health check PASSED"
    else
        echo "   ⚠ Health check returned response but may have issues"
    fi
else
    echo "   ✗ No response from health endpoint"
fi

echo ""
echo "5. Checking database file..."
if docker exec cyber-vault-python test -f /data/vault.db 2>/dev/null; then
    echo "   ✓ Database file exists"
    echo ""
    echo "   Database tables:"
    docker exec cyber-vault-python sqlite3 /data/vault.db ".tables" 2>/dev/null | sed 's/^/      /'
else
    echo "   ✗ Database file not found"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                      SUMMARY                               ║"
echo "╠════════════════════════════════════════════════════════════╣"

if [ "$response" = "200" ] && echo "$health" | grep -q "healthy"; then
    echo "║  ✓ Cyber Vault is WORKING!                                ║"
    echo "║                                                            ║"
    echo "║  Access it at: http://localhost:8080                      ║"
    echo "╚════════════════════════════════════════════════════════════╝"
else
    echo "║  ⚠ Cyber Vault may have issues                            ║"
    echo "║                                                            ║"
    echo "║  View full logs with:                                     ║"
    echo "║  docker-compose -f docker-compose-python.yml logs -f      ║"
    echo "╚════════════════════════════════════════════════════════════╝"
fi

echo ""

#!/bin/bash
set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   CYBER VAULT - SECURE DEPLOYMENT SCRIPT                  ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Get custom port
echo -e "${YELLOW}Enter port number (press Enter for default 8080):${NC}"
read -r CUSTOM_PORT
PORT=${CUSTOM_PORT:-8080}

echo ""
echo -e "${GREEN}✓ Using port: $PORT${NC}"
echo ""

echo -e "${YELLOW}[1/5] Checking dependencies...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker not installed${NC}"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Error: Docker Compose not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker and Docker Compose found${NC}"
echo ""

echo -e "${YELLOW}[2/5] Configuring port...${NC}"
# Update docker-compose.yml with custom port
sed -i "s/\"[0-9]*:5000\"/\"$PORT:5000\"/" docker-compose.yml
echo -e "${GREEN}✓ Port configured to $PORT${NC}"
echo ""

echo -e "${YELLOW}[3/5] Generating secure secrets...${NC}"
if [ ! -f .env ]; then
    SECRET_KEY=$(openssl rand -hex 32)
    cat > .env << EOF
SECRET_KEY=$SECRET_KEY
EOF
    echo -e "${GREEN}✓ Generated new SECRET_KEY${NC}"
else
    echo -e "${GREEN}✓ Using existing .env${NC}"
fi
echo ""

echo -e "${YELLOW}[4/5] Stopping old containers...${NC}"
docker-compose down 2>/dev/null || true
echo -e "${GREEN}✓ Old containers stopped${NC}"
echo ""

echo -e "${YELLOW}[5/5] Building and starting...${NC}"
docker-compose up -d --build
echo -e "${GREEN}✓ Cyber Vault started${NC}"
echo ""

# Wait and verify
sleep 3

if docker-compose ps | grep -q "Up"; then
    echo -e "${GREEN}✓ Service is running${NC}"
    echo ""
    
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║              DEPLOYMENT SUCCESSFUL!                        ║"
    echo "╠════════════════════════════════════════════════════════════╣"
    echo "║                                                            ║"
    echo "║  🌐 Access your vault at:                                  ║"
    echo "║     http://localhost:$PORT                                  "
    echo "║                                                            ║"
    echo "║  🔒 Security Features:                                     ║"
    echo "║     ✓ AES-256-GCM encryption (Web Crypto API)              ║"
    echo "║     ✓ PBKDF2 with 250,000 iterations                       ║"
    echo "║     ✓ Flask session cookies (HTTPOnly, SameSite)           ║"
    echo "║     ✓ Rate limiting (5 login attempts/min)                 ║"
    echo "║     ✓ Security headers (CSP, X-Frame-Options)              ║"
    echo "║     ✓ Zero-knowledge architecture                          ║"
    echo "║     ✓ No CORS (same-origin only)                           ║"
    echo "║                                                            ║"
    echo "║  📝 Useful Commands:                                       ║"
    echo "║     View logs:  docker-compose logs -f                     ║"
    echo "║     Stop:       docker-compose down                        ║"
    echo "║     Restart:    docker-compose restart                     ║"
    echo "║                                                            ║"
    echo "║  ⚠️  IMPORTANT:                                             ║"
    echo "║     - Master password never stored anywhere                ║"
    echo "║     - Page refresh = must re-login (by design)             ║"
    echo "║     - All encryption happens in your browser               ║"
    echo "║     - Server never sees your passwords                     ║"
    echo "║                                                            ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
else
    echo -e "${RED}✗ Service failed to start${NC}"
    echo ""
    echo "Check logs with: docker-compose logs"
    exit 1
fi

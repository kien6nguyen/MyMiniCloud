#!/bin/bash
# ============================================================
# MyMiniCloud - Deploy script for Ubuntu EC2
# Usage: bash deploy.sh
# ============================================================

set -e  # Exit immediately on error

REPO_URL="https://github.com/YOUR_USERNAME/MyMiniCloud.git"  # <-- đổi lại
APP_DIR="$HOME/MyMiniCloud"

echo "========================================"
echo "  MyMiniCloud - EC2 Deploy Script"
echo "========================================"

# ── 1. Update system ─────────────────────────────────────────
echo "[1/5] Updating system packages..."
sudo apt-get update -y && sudo apt-get upgrade -y

# ── 2. Install Docker ────────────────────────────────────────
echo "[2/5] Installing Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com | sudo bash
    sudo usermod -aG docker $USER
    echo "Docker installed. You may need to re-login for group changes."
else
    echo "Docker already installed: $(docker --version)"
fi

# ── 3. Install Docker Compose ────────────────────────────────
echo "[3/5] Installing Docker Compose..."
if ! command -v docker compose &> /dev/null; then
    sudo apt-get install -y docker-compose-plugin
else
    echo "Docker Compose already installed."
fi

# ── 4. Clone / Pull repo ─────────────────────────────────────
echo "[4/5] Pulling latest code..."
if [ -d "$APP_DIR" ]; then
    echo "Repo exists, pulling latest changes..."
    cd "$APP_DIR" && git pull
else
    echo "Cloning repo..."
    git clone "$REPO_URL" "$APP_DIR"
    cd "$APP_DIR"
fi

# ── 5. Start services ────────────────────────────────────────
echo "[5/5] Starting all containers..."
cd "$APP_DIR"
sudo docker compose down --remove-orphans
sudo docker compose up --build -d

echo ""
echo "========================================"
echo "  ✅ Deploy completed!"
echo "========================================"
echo ""
PUBLIC_IP=$(curl -s http://checkip.amazonaws.com)
echo "  🌐 Public IP: $PUBLIC_IP"
echo ""
echo "  Services accessible at:"
echo "  → Reverse Proxy : http://$PUBLIC_IP:8080"
echo "  → Web Server    : http://$PUBLIC_IP:8080"
echo "  → App API       : http://$PUBLIC_IP:8085/health"
echo "  → Auth Server   : http://$PUBLIC_IP:8081"
echo "  → MinIO Console : http://$PUBLIC_IP:9001"
echo "  → Prometheus    : http://$PUBLIC_IP:9090"
echo "  → Grafana       : http://$PUBLIC_IP:3000"
echo "========================================"

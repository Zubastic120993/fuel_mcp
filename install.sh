#!/usr/bin/env bash
set -euo pipefail

# ==========================================================
# 🧩 Fuel MCP (Gradio Edition) — Universal Installer
# ==========================================================
# Can be run from *anywhere*, even on a clean system.
#
# Optional environment variables:
#   REPO_URL   → GitHub repo (default: Zubastic120993/fuel_mcp)
#   BRANCH     → branch to checkout (default: feature/docker-gradio-package)
#   TARGET_DIR → clone folder (default: fuel_mcp_gradio)
#
# Example:
#   REPO_URL=https://github.com/Zubastic120993/fuel_mcp.git \
#   BRANCH=feature/docker-gradio-package \
#   TARGET_DIR=fuel_mcp_gradio \
#   ./install.sh
# ==========================================================

REPO_URL="${REPO_URL:-https://github.com/Zubastic120993/fuel_mcp.git}"
BRANCH="${BRANCH:-feature/docker-gradio-package}"
TARGET_DIR="${TARGET_DIR:-fuel_mcp_gradio}"

# ----------------------------------------------------------
# 1️⃣  Helper — Check for required commands
# ----------------------------------------------------------
need_cmd() {
  local cmd="$1"
  command -v "$cmd" >/dev/null 2>&1 || {
    echo "❌ Missing required command: $cmd" >&2
    exit 1
  }
}

need_cmd git
need_cmd docker
need_cmd docker-compose

# ----------------------------------------------------------
# 2️⃣  Clone or Update Repository
# ----------------------------------------------------------
if [ -d "$TARGET_DIR/.git" ]; then
  echo "🔄 Updating existing repository in $TARGET_DIR ..."
  git -C "$TARGET_DIR" fetch --tags --prune
  git -C "$TARGET_DIR" checkout "$BRANCH"
  git -C "$TARGET_DIR" pull --ff-only origin "$BRANCH"
else
  echo "📥 Cloning $REPO_URL (branch: $BRANCH) → $TARGET_DIR"
  git clone --branch "$BRANCH" "$REPO_URL" "$TARGET_DIR"
fi

cd "$TARGET_DIR"
echo "📂 Current directory: $(pwd)"

# ----------------------------------------------------------
# 3️⃣  Clean Up Old Containers (if any)
# ----------------------------------------------------------
echo "🧹 Checking for old Fuel MCP containers..."
OLD_CONTAINERS=$(docker ps -aq --filter "name=fuel_mcp" || true)
if [ -n "$OLD_CONTAINERS" ]; then
  echo "   Removing old containers..."
  docker rm -f $OLD_CONTAINERS >/dev/null 2>&1 || true
else
  echo "   No old containers found."
fi

# ----------------------------------------------------------
# 4️⃣  Start Dockerized Environment
# ----------------------------------------------------------
if [ ! -x "./start-docker.sh" ]; then
  echo "🔧 Making start-docker.sh executable..."
  chmod +x start-docker.sh
fi

echo "🚀 Launching Fuel MCP (Gradio + FastAPI stack)..."
./start-docker.sh start

# ----------------------------------------------------------
# 5️⃣  Summary
# ----------------------------------------------------------
echo
echo "✅ Fuel MCP successfully deployed!"
echo "🌐 Access Points:"
echo "   • Gradio Frontend → http://localhost:7860"
echo "   • FastAPI Backend → http://localhost:8000"
echo "   • API Docs        → http://localhost:8000/docs"
echo
echo "🧪 Test system:  ./start-docker.sh test"
echo "🛑 Stop system:  ./start-docker.sh stop"
echo
echo "📦 Repository Path: $(pwd)"
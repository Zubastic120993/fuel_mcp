#!/usr/bin/env bash
set -euo pipefail

# ==========================================================
# 🧩 Fuel MCP (Gradio Edition) — Installer
# ==========================================================
# Clones or updates the repository and builds the Docker image.
# Run this once, then start the system with:
#   ./start-docker.sh start
# ==========================================================

REPO_URL="${REPO_URL:-https://github.com/Zubastic120993/fuel_mcp.git}"
BRANCH="${BRANCH:-feature/docker-gradio-package}"
TARGET_DIR="${TARGET_DIR:-fuel_mcp_gradio}"

# ----------------------------------------------------------
# 1️⃣  Helpers
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
# 3️⃣  Build Docker Image
# ----------------------------------------------------------
echo
echo "🛠️  Building Docker image: fuel-mcp-gradio:latest ..."
echo "⏳ This may take a few minutes on the first run."
echo "💡 Tip: If Docker prompts for authentication, ensure you're logged in to Docker Hub."
echo

docker build -f Dockerfile.gradio -t fuel-mcp-gradio:latest .

# ----------------------------------------------------------
# 4️⃣  Completion Message
# ----------------------------------------------------------
echo
echo "✅ Installation complete!"
echo
echo "Next steps:"
echo "   ./start-docker.sh start   → Launch Fuel MCP"
echo "   ./start-docker.sh test    → Verify installation"
echo "   ./start-docker.sh stop    → Stop containers"
echo
echo "📦 Repository Path: $(pwd)"
echo "🚀 You’re ready to go!"
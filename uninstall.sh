#!/usr/bin/env bash
set -euo pipefail

# ==========================================================
# 🧩 Fuel MCP (Gradio Edition) — Universal Uninstaller
# ==========================================================
# Removes all Docker containers, images, and optionally
# deletes the cloned repository directory.
#
# Optional environment variables:
#   TARGET_DIR → directory to remove (default: fuel_mcp_gradio)
#   KEEP_CODE  → set to 1 to keep cloned code (default: 0)
# ==========================================================

TARGET_DIR="${TARGET_DIR:-fuel_mcp_gradio}"
KEEP_CODE="${KEEP_CODE:-0}"

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

need_cmd docker
need_cmd docker-compose

echo "============================================="
echo "🧩 Fuel MCP — Uninstallation Started"
echo "============================================="

# ----------------------------------------------------------
# 2️⃣  Stop Docker Compose Services
# ----------------------------------------------------------
if [ -f "$TARGET_DIR/docker-compose-gradio.yml" ]; then
  echo "🛑 Stopping running containers via Docker Compose..."
  (cd "$TARGET_DIR" && docker-compose -f docker-compose-gradio.yml down --remove-orphans || true)
else
  echo "⚠️  No docker-compose file found in $TARGET_DIR — skipping compose stop."
fi

# ----------------------------------------------------------
# 3️⃣  Remove Orphaned Containers
# ----------------------------------------------------------
echo "🧹 Checking for orphaned containers..."
OLD_CONTAINERS=$(docker ps -aq --filter "name=fuel_mcp" || true)
if [ -n "$OLD_CONTAINERS" ]; then
  echo "   Removing containers..."
  docker rm -f $OLD_CONTAINERS >/dev/null 2>&1 || true
else
  echo "   No orphaned containers found."
fi

# ----------------------------------------------------------
# 4️⃣  Remove Docker Images
# ----------------------------------------------------------
echo "🧩 Removing Fuel MCP Docker images..."
IMAGES=$(docker images -q "fuel-mcp-gradio" || true)
if [ -n "$IMAGES" ]; then
  docker rmi -f $IMAGES >/dev/null 2>&1 || true
  echo "✅ Images removed."
else
  echo "   No Fuel MCP images found."
fi

# ----------------------------------------------------------
# 5️⃣  Remove Docker Networks (if any)
# ----------------------------------------------------------
echo "🌐 Cleaning up old networks..."
NETWORKS=$(docker network ls --filter "name=fuel_mcp" -q || true)
if [ -n "$NETWORKS" ]; then
  docker network rm $NETWORKS >/dev/null 2>&1 || true
  echo "✅ Networks removed."
else
  echo "   No old networks found."
fi

# ----------------------------------------------------------
# 6️⃣  Optionally Remove Repository Directory
# ----------------------------------------------------------
if [ "$KEEP_CODE" -eq 0 ]; then
  if [ -d "$TARGET_DIR" ]; then
    echo "🗑️  Removing cloned repository: $TARGET_DIR"
    rm -rf "$TARGET_DIR"
    echo "✅ Repository removed."
  else
    echo "   No repository folder found — skipping."
  fi
else
  echo "💾 KEEP_CODE=1 → keeping cloned directory ($TARGET_DIR)."
fi

# ----------------------------------------------------------
# 7️⃣  Final Summary
# ----------------------------------------------------------
echo
echo "✅ Uninstallation complete!"
echo "💡 To reinstall, run:  ./install.sh"
echo "📦 Removed project folder: $TARGET_DIR"
echo "============================================="
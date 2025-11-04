#!/usr/bin/env bash
set -euo pipefail

# =====================================================
# 🧩 Fuel MCP — Docker Entrypoint
# =====================================================
# Usage:
#   docker run fuel-mcp-gradio api   → start FastAPI backend
#   docker run fuel-mcp-gradio gui   → start Gradio unified app
# =====================================================

MODE="${1:-api}"

echo "🚀 Starting Fuel MCP in mode: ${MODE}"
echo "📂 Working directory: $(pwd)"
echo "👤 Running as: $(whoami)"

# -----------------------------------------------------
# Prepare environment
# -----------------------------------------------------
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1

# -----------------------------------------------------
# Launch selected mode
# -----------------------------------------------------
case "$MODE" in
  api)
    echo "🌐 Launching FastAPI backend on port 8000..."
    exec uvicorn fuel_mcp.api.mcp_api:app --host 0.0.0.0 --port 8000
    ;;
  gui)
    echo "🧠 Launching Gradio unified interface on port 7860..."
    exec python -m fuel_mcp.gui_astm.app_astm_unified
    ;;
  *)
    echo "❌ Unknown mode: $MODE"
    echo "Usage: docker run fuel-mcp-gradio [api|gui]"
    exit 1
    ;;
esac
#!/usr/bin/env bash
set -euo pipefail

# ==========================================================
# 🧩 Fuel MCP — Docker Deployment Manager (v2.2)
# ==========================================================
# Usage:
#   ./start-docker.sh start     → Build and start all services
#   ./start-docker.sh stop      → Stop and remove services
#   ./start-docker.sh restart   → Restart all containers
#   ./start-docker.sh test      → Run API health tests
#   ./start-docker.sh logs      → Follow container logs
#   ./start-docker.sh clean     → Remove stack resources safely
# ==========================================================

COMPOSE_FILE="docker-compose-gradio.yml"
PROJECT_NAME="fuel_mcp"

# ----------------------------------------------------------
# 🪧 Banner
# ----------------------------------------------------------
show_banner() {
  echo "============================================="
  echo "🧩 Fuel MCP — Docker Deployment"
  echo "============================================="
  echo
}

# ----------------------------------------------------------
# 🚀 Start Services
# ----------------------------------------------------------
start() {
  show_banner
  echo "🚀 Starting Fuel MCP services..."
  docker compose -p "$PROJECT_NAME" -f "$COMPOSE_FILE" up -d --build --remove-orphans

  echo
  echo "✅ Services started successfully!"
  echo
  echo "📍 Access Points:"
  echo "   Gradio Frontend: http://localhost:7860"
  echo "   FastAPI Backend: http://localhost:8000"
  echo "   API Docs:        http://localhost:8000/docs"
  echo
  echo "📊 View logs: docker compose -p $PROJECT_NAME -f $COMPOSE_FILE logs -f"
  echo "🛑 Stop:      ./start-docker.sh stop"
}

# ----------------------------------------------------------
# 🛑 Stop Services
# ----------------------------------------------------------
stop() {
  show_banner
  echo "🛑 Stopping services..."
  docker compose -p "$PROJECT_NAME" -f "$COMPOSE_FILE" down --remove-orphans
  echo "✅ Services stopped"
}

# ----------------------------------------------------------
# 🔁 Restart Services
# ----------------------------------------------------------
restart() {
  show_banner
  echo "🔁 Restarting services..."
  docker compose -p "$PROJECT_NAME" -f "$COMPOSE_FILE" down --remove-orphans
  docker compose -p "$PROJECT_NAME" -f "$COMPOSE_FILE" up -d --build --remove-orphans
  echo "✅ Restart complete"
}

# ----------------------------------------------------------
# 🧪 Test Deployment (with exit codes for CI)
# ----------------------------------------------------------
test_services() {
  show_banner
  echo "🧪 Testing deployment..."
  sleep 5
  echo

  local status=0

  echo "Testing backend API..."
  if curl -sf http://localhost:8000/status | grep -q "ok"; then
    echo "✅ Backend API is working"
  else
    echo "❌ Backend API test failed"
    status=1
  fi

  echo "Testing VCF calculation..."
  if curl -sf "http://localhost:8000/vcf?rho15=850&tempC=25" | grep -q "result"; then
    echo "✅ VCF calculation is working"
  else
    echo "❌ VCF test failed"
    status=1
  fi

  echo "Testing unit conversion..."
  if curl -sf "http://localhost:8000/convert?value=1&from_unit=barrel&to_unit=litre" | grep -q "result"; then
    echo "✅ Unit conversion is working"
  else
    echo "❌ Unit conversion test failed"
    status=1
  fi

  echo
  if [ "$status" -eq 0 ]; then
    echo "✅ All tests passed!"
  else
    echo "❌ One or more tests failed!"
  fi
  exit "$status"
}

# ----------------------------------------------------------
# 📜 Logs
# ----------------------------------------------------------
logs() {
  show_banner
  echo "📜 Streaming logs..."
  docker compose -p "$PROJECT_NAME" -f "$COMPOSE_FILE" logs -f
}

# ----------------------------------------------------------
# 🧹 Clean Environment (safe scoped cleanup)
# ----------------------------------------------------------
clean() {
  show_banner
  echo "🧹 Cleaning Docker resources for project '$PROJECT_NAME'..."

  # Remove containers, networks, and volumes for this stack
  docker compose -p "$PROJECT_NAME" -f "$COMPOSE_FILE" down -v --remove-orphans

  # Optional: Warn before global prune
  echo
  echo "⚠️  The next step removes *dangling images only* (no running ones)."
  echo "   To skip, press Ctrl+C within 5 seconds..."
  sleep 5
  docker image prune -af --filter "dangling=true" >/dev/null 2>&1 || true

  echo "✅ Cleanup complete — project resources removed safely."
}

# ----------------------------------------------------------
# ❓ Usage
# ----------------------------------------------------------
usage() {
  echo "Usage: ./start-docker.sh [start|stop|restart|test|logs|clean]"
  exit 1
}

# ----------------------------------------------------------
# 🧠 Command Dispatcher
# ----------------------------------------------------------
case "${1:-}" in
  start) start ;;
  stop) stop ;;
  restart) restart ;;
  test) test_services ;;
  logs) logs ;;
  clean) clean ;;
  *) usage ;;
esac
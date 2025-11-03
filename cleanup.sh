#!/bin/bash
# =============================================================================
# 🧹 Fuel MCP — Cleanup Script for Docker Package
# =============================================================================
# This script removes unnecessary files for Docker Gradio deployment
# Run this AFTER committing your changes to git
# =============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                               ║${NC}"
echo -e "${BLUE}║        🧹 Fuel MCP — Docker Package Cleanup                   ║${NC}"
echo -e "${BLUE}║                                                               ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Safety check: ensure we're in the right directory
if [ ! -f "Dockerfile.gradio" ] || [ ! -f "docker-compose-gradio.yml" ]; then
    echo -e "${RED}❌ ERROR: Must run from project root directory${NC}"
    echo -e "${RED}   (Directory with Dockerfile.gradio and docker-compose-gradio.yml)${NC}"
    exit 1
fi

# Check git status
echo -e "${YELLOW}🔍 Checking git status...${NC}"
if ! git diff-index --quiet HEAD -- 2>/dev/null; then
    echo -e "${YELLOW}⚠️  WARNING: You have uncommitted changes!${NC}"
    echo -e "${YELLOW}   It's recommended to commit changes before cleanup.${NC}"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}Cleanup cancelled.${NC}"
        exit 0
    fi
fi

echo ""
echo -e "${BLUE}📊 Current project size:${NC}"
du -sh . 2>/dev/null || echo "Unable to calculate"
echo ""

# Create backup directory
BACKUP_DIR="cleanup_backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
echo -e "${GREEN}📦 Created backup directory: $BACKUP_DIR${NC}"
echo ""

# Function to safely remove directory/file
safe_remove() {
    local item="$1"
    local description="$2"
    
    if [ -e "$item" ]; then
        local size=$(du -sh "$item" 2>/dev/null | cut -f1)
        echo -e "${YELLOW}Removing:${NC} $item ($size) — $description"
        rm -rf "$item"
        echo -e "${GREEN}✅ Removed${NC}"
    else
        echo -e "${BLUE}⊘ Already absent:${NC} $item"
    fi
}

echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}Starting cleanup...${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# 1. Virtual Environment (LARGEST)
echo -e "${YELLOW}1. Removing Virtual Environment (venv/)...${NC}"
safe_remove "venv" "Not needed in Docker"
echo ""

# 2. Tests
echo -e "${YELLOW}2. Removing Test Files...${NC}"
safe_remove "fuel_mcp/tests" "Not needed for production"
safe_remove ".pytest_cache" "Test cache"
echo ""

# 3. RAG Features
echo -e "${YELLOW}3. Removing RAG Features...${NC}"
safe_remove "fuel_mcp/rag" "Not used by Gradio apps"
safe_remove "fuel_mcp/models" "Empty models directory"
echo ""

# 4. Build Artifacts
echo -e "${YELLOW}4. Removing Build Artifacts...${NC}"
safe_remove "dist" "Built packages"
safe_remove "fuel_mcp.egg-info" "Build metadata"
safe_remove "build" "Build directory"
echo ""

# 5. Python Cache
echo -e "${YELLOW}5. Removing Python Cache Files...${NC}"
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true
find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
echo -e "${GREEN}✅ Cleaned Python cache${NC}"
echo ""

# 6. CLI Tools
echo -e "${YELLOW}6. Removing CLI Tools...${NC}"
safe_remove "fuel_mcp/cli" "Not used in web deployment"
echo ""

# 7. Flowise Integration
echo -e "${YELLOW}7. Removing Flowise Integration...${NC}"
safe_remove "fuel_mcp/flowise" "Not used in Gradio"
echo ""

# 8. Old Logs
echo -e "${YELLOW}8. Cleaning Old Logs...${NC}"
if [ -d "logs" ]; then
    # Backup database if exists
    if [ -f "fuel_mcp/data/mcp_history.db" ]; then
        cp fuel_mcp/data/mcp_history.db "$BACKUP_DIR/"
        echo -e "${GREEN}✅ Backed up database to $BACKUP_DIR/${NC}"
    fi
    
    # Clean logs but keep directory
    rm -f logs/*.log logs/*.json 2>/dev/null || true
    rm -f fuel_mcp/logs/*.log fuel_mcp/logs/*.json 2>/dev/null || true
    echo -e "${GREEN}✅ Cleaned old logs${NC}"
fi
safe_remove "docker-build.log" "Temporary build log"
echo ""

# 9. Extra Documentation
echo -e "${YELLOW}9. Removing Extra Documentation...${NC}"
safe_remove "docs/CHANGELOG_v1.0.3.md" "Internal changelog"
safe_remove "docs/Fuel_MCP_v1.0.3_Consolidated_Report.md" "Internal report"
echo ""

# 10. Old Docker Files
echo -e "${YELLOW}10. Handling Old Docker Files...${NC}"
if [ -f "Dockerfile" ] && [ -f "Dockerfile.gradio" ]; then
    echo -e "${YELLOW}⚠️  Found old Dockerfile (API-only)${NC}"
    echo -e "   Keeping as Dockerfile.old for reference"
    mv Dockerfile Dockerfile.old 2>/dev/null || true
fi
if [ -f "docker-compose.yml" ] && [ -f "docker-compose-gradio.yml" ]; then
    echo -e "${YELLOW}⚠️  Found old docker-compose.yml (API-only)${NC}"
    echo -e "   Keeping as docker-compose.old.yml for reference"
    mv docker-compose.yml docker-compose.old.yml 2>/dev/null || true
fi
echo ""

# 11. Old Scripts
echo -e "${YELLOW}11. Handling Old Scripts...${NC}"
if [ -f "launch_gui.sh" ]; then
    echo -e "${YELLOW}⚠️  Found old launch_gui.sh (local dev)${NC}"
    echo -e "   Keeping as launch_gui.old.sh for reference"
    mv launch_gui.sh launch_gui.old.sh 2>/dev/null || true
fi
echo ""

# 12. Optional: Requirements lock file
echo -e "${YELLOW}12. Handling Development Requirements...${NC}"
if [ -f "requirements-lock.txt" ]; then
    echo -e "${YELLOW}⚠️  Found requirements-lock.txt (full dev dependencies)${NC}"
    echo -e "   Keeping as requirements-dev.txt for reference"
    mv requirements-lock.txt requirements-dev.txt 2>/dev/null || true
fi
echo ""

# Summary
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Cleanup Complete!${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

echo -e "${BLUE}📊 New project size:${NC}"
du -sh . 2>/dev/null || echo "Unable to calculate"
echo ""

echo -e "${GREEN}✅ Kept (Required for Docker):${NC}"
echo "   - fuel_mcp/api/          (Backend API)"
echo "   - fuel_mcp/gui_astm/     (Gradio frontends)"
echo "   - fuel_mcp/core/         (Calculation engine)"
echo "   - fuel_mcp/tables/       (ASTM data)"
echo "   - fuel_mcp/data/         (Database)"
echo "   - Docker files           (Dockerfile.gradio, docker-compose-gradio.yml)"
echo "   - Documentation          (README-DOCKER.md, etc.)"
echo ""

echo -e "${YELLOW}📦 Backup created:${NC} $BACKUP_DIR/"
echo "   Contains: mcp_history.db (if existed)"
echo ""

echo -e "${BLUE}🚀 Next Steps:${NC}"
echo "   1. Test Docker build:  docker build -f Dockerfile.gradio -t fuel-mcp-gradio:latest ."
echo "   2. Test deployment:    ./start-docker.sh start"
echo "   3. Commit changes:     git add -A && git commit -m 'chore: Clean up unnecessary files'"
echo "   4. If everything works, you can delete: $BACKUP_DIR/"
echo ""

echo -e "${GREEN}🎉 Your Docker package is now clean and ready for deployment!${NC}"


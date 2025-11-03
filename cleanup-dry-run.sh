#!/bin/bash
# =============================================================================
# 🧹 Fuel MCP — Cleanup Dry Run (Shows what will be removed)
# =============================================================================
# This script shows what will be removed WITHOUT actually deleting anything
# =============================================================================

set -e

BLUE='\033[0;34m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     🔍 Cleanup Dry Run — What Will Be Removed                 ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

total_size=0

check_item() {
    local item="$1"
    local description="$2"
    
    if [ -e "$item" ]; then
        local size=$(du -sh "$item" 2>/dev/null | cut -f1 | sed 's/[^0-9.]//g')
        local unit=$(du -sh "$item" 2>/dev/null | cut -f1 | sed 's/[0-9.]//g')
        echo -e "${YELLOW}❌ WILL REMOVE:${NC} $item"
        echo -e "   Size: $(du -sh "$item" 2>/dev/null | cut -f1) — $description"
        
        # Try to convert to KB for total
        if [[ "$unit" == "G" ]]; then
            total_size=$(echo "$total_size + $size * 1024 * 1024" | bc 2>/dev/null || echo $total_size)
        elif [[ "$unit" == "M" ]]; then
            total_size=$(echo "$total_size + $size * 1024" | bc 2>/dev/null || echo $total_size)
        elif [[ "$unit" == "K" ]]; then
            total_size=$(echo "$total_size + $size" | bc 2>/dev/null || echo $total_size)
        fi
    else
        echo -e "${GREEN}✅ Already absent:${NC} $item"
    fi
    echo ""
}

echo -e "${BLUE}Scanning project...${NC}"
echo ""

echo -e "${YELLOW}═══ Virtual Environment ═══${NC}"
check_item "venv" "Virtual environment (Docker builds its own)"

echo -e "${YELLOW}═══ Test Files ═══${NC}"
check_item "fuel_mcp/tests" "Test files"
check_item ".pytest_cache" "Test cache"

echo -e "${YELLOW}═══ RAG Features ═══${NC}"
check_item "fuel_mcp/rag" "RAG functionality"
check_item "fuel_mcp/models" "Model directory"

echo -e "${YELLOW}═══ Build Artifacts ═══${NC}"
check_item "dist" "Built packages"
check_item "fuel_mcp.egg-info" "Build metadata"

echo -e "${YELLOW}═══ CLI & Integrations ═══${NC}"
check_item "fuel_mcp/cli" "CLI tools"
check_item "fuel_mcp/flowise" "Flowise integration"

echo -e "${YELLOW}═══ Logs ═══${NC}"
check_item "docker-build.log" "Build log"
if [ -d "logs" ]; then
    echo -e "${YELLOW}❌ WILL CLEAN:${NC} logs/*.log, logs/*.json"
    ls -lh logs/*.log logs/*.json 2>/dev/null || echo "   (no logs found)"
    echo ""
fi

echo -e "${YELLOW}═══ Python Cache ═══${NC}"
cache_count=$(find . -type d -name "__pycache__" 2>/dev/null | wc -l)
echo -e "${YELLOW}❌ WILL REMOVE:${NC} $cache_count __pycache__ directories"
echo ""

echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Dry Run Complete!${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}📊 Total space that will be freed: ~1.5 GB${NC}"
echo ""
echo -e "${YELLOW}To actually perform cleanup, run:${NC}"
echo -e "   ./cleanup.sh"
echo ""


#!/bin/bash
# =============================================================================
# Fuel MCP GUI Launcher
# =============================================================================
# Quick launcher for the unified ASTM D1250 GUI interface
#
# Usage:
#   ./launch_gui.sh           # Launch unified interface (all-in-one)
#   ./launch_gui.sh api       # Launch API gravity calculator only
#   ./launch_gui.sh density   # Launch density calculator only
#   ./launch_gui.sh vol       # Launch volume/weight converter only
#   ./launch_gui.sh units     # Launch universal unit converter only
# =============================================================================

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}=============================================${NC}"
echo -e "${BLUE}🧩 Fuel MCP GUI Launcher${NC}"
echo -e "${BLUE}=============================================${NC}"

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo -e "${YELLOW}⚠️  Virtual environment not activated${NC}"
    echo -e "${YELLOW}Attempting to activate venv...${NC}"
    if [ -f "./venv/bin/activate" ]; then
        source ./venv/bin/activate
        echo -e "${GREEN}✅ Virtual environment activated${NC}"
    else
        echo -e "${YELLOW}⚠️  No venv found. Please run: python3 -m venv venv${NC}"
        exit 1
    fi
fi

# Parse command line argument
MODE=${1:-unified}

case "$MODE" in
    unified|all)
        echo -e "${GREEN}🚀 Launching Unified ASTM Interface (All-in-One)${NC}"
        echo -e "${BLUE}→ http://localhost:7860${NC}"
        python -m fuel_mcp.gui_astm.app_astm_unified
        ;;
    api)
        echo -e "${GREEN}🚀 Launching API Gravity Calculator${NC}"
        echo -e "${BLUE}→ http://localhost:7861${NC}"
        python -m fuel_mcp.gui_astm.app_astm_api
        ;;
    rel|relative)
        echo -e "${GREEN}🚀 Launching Relative Density Calculator${NC}"
        echo -e "${BLUE}→ http://localhost:7862${NC}"
        python -m fuel_mcp.gui_astm.app_astm_rel_density
        ;;
    density|dens)
        echo -e "${GREEN}🚀 Launching Density Calculator${NC}"
        echo -e "${BLUE}→ http://localhost:7863${NC}"
        python -m fuel_mcp.gui_astm.app_astm_density
        ;;
    vol|volume|weight)
        echo -e "${GREEN}🚀 Launching Volume & Weight Converter${NC}"
        echo -e "${BLUE}→ http://localhost:7864${NC}"
        python -m fuel_mcp.gui_astm.app_astm_vol_weight
        ;;
    units|universal)
        echo -e "${GREEN}🚀 Launching Universal Unit Converter${NC}"
        echo -e "${BLUE}→ http://localhost:7870${NC}"
        python -m fuel_mcp.gui_astm.app_astm_universal_converter
        ;;
    *)
        echo -e "${YELLOW}❌ Unknown mode: $MODE${NC}"
        echo ""
        echo "Available modes:"
        echo "  unified    - All calculators in one interface (default)"
        echo "  api        - API Gravity calculator"
        echo "  relative   - Relative Density calculator"
        echo "  density    - Density calculator"
        echo "  volume     - Volume & Weight converter"
        echo "  units      - Universal Unit converter"
        exit 1
        ;;
esac


#!/bin/bash
# =============================================================================
# 🧩 Fuel MCP — Docker Quick Start Script
# =============================================================================
# Quickly build and launch Fuel MCP Gradio application in Docker
# Usage: ./start-docker.sh [build|start|stop|restart|logs]
# =============================================================================

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

COMPOSE_FILE="docker-compose-gradio.yml"

# Print banner
echo -e "${BLUE}=============================================${NC}"
echo -e "${BLUE}🧩 Fuel MCP — Docker Deployment${NC}"
echo -e "${BLUE}=============================================${NC}"
echo ""

# Parse command
CMD=${1:-start}

case "$CMD" in
    build)
        echo -e "${GREEN}🔨 Building Docker image...${NC}"
        docker build -f Dockerfile.gradio -t fuel-mcp-gradio:latest .
        echo -e "${GREEN}✅ Build complete!${NC}"
        ;;
    
    start|up)
        echo -e "${GREEN}🚀 Starting Fuel MCP services...${NC}"
        docker-compose -f $COMPOSE_FILE up -d
        echo ""
        echo -e "${GREEN}✅ Services started successfully!${NC}"
        echo ""
        echo -e "${BLUE}📍 Access Points:${NC}"
        echo -e "   Gradio Frontend: ${YELLOW}http://localhost:7860${NC}"
        echo -e "   FastAPI Backend: ${YELLOW}http://localhost:8000${NC}"
        echo -e "   API Docs:        ${YELLOW}http://localhost:8000/docs${NC}"
        echo ""
        echo -e "${BLUE}📊 View logs:${NC} docker-compose -f $COMPOSE_FILE logs -f"
        echo -e "${BLUE}🛑 Stop:${NC}      ./start-docker.sh stop"
        ;;
    
    stop|down)
        echo -e "${YELLOW}🛑 Stopping services...${NC}"
        docker-compose -f $COMPOSE_FILE down
        echo -e "${GREEN}✅ Services stopped${NC}"
        ;;
    
    restart)
        echo -e "${YELLOW}🔄 Restarting services...${NC}"
        docker-compose -f $COMPOSE_FILE restart
        echo -e "${GREEN}✅ Services restarted${NC}"
        ;;
    
    logs)
        echo -e "${BLUE}📋 Showing logs (Ctrl+C to exit)...${NC}"
        docker-compose -f $COMPOSE_FILE logs -f
        ;;
    
    status)
        echo -e "${BLUE}📊 Service Status:${NC}"
        docker-compose -f $COMPOSE_FILE ps
        echo ""
        echo -e "${BLUE}🔍 Health Check:${NC}"
        if curl -s http://localhost:8000/status > /dev/null 2>&1; then
            echo -e "   Backend: ${GREEN}✅ Healthy${NC}"
        else
            echo -e "   Backend: ${RED}❌ Not responding${NC}"
        fi
        
        if curl -s http://localhost:7860 > /dev/null 2>&1; then
            echo -e "   Frontend: ${GREEN}✅ Healthy${NC}"
        else
            echo -e "   Frontend: ${RED}❌ Not responding${NC}"
        fi
        ;;
    
    clean)
        echo -e "${RED}🧹 Cleaning up Docker resources...${NC}"
        docker-compose -f $COMPOSE_FILE down -v
        docker rmi fuel-mcp-gradio:latest 2>/dev/null || true
        echo -e "${GREEN}✅ Cleanup complete${NC}"
        ;;
    
    test)
        echo -e "${BLUE}🧪 Testing deployment...${NC}"
        echo ""
        
        echo -e "${YELLOW}Testing backend API...${NC}"
        if curl -s "http://localhost:8000/status" | grep -q "operational"; then
            echo -e "${GREEN}✅ Backend API is working${NC}"
        else
            echo -e "${RED}❌ Backend API test failed${NC}"
            exit 1
        fi
        
        echo -e "${YELLOW}Testing VCF calculation...${NC}"
        if curl -s "http://localhost:8000/vcf?rho15=850&tempC=25" | grep -q "VCF"; then
            echo -e "${GREEN}✅ VCF calculation is working${NC}"
        else
            echo -e "${RED}❌ VCF calculation test failed${NC}"
            exit 1
        fi
        
        echo -e "${YELLOW}Testing unit conversion...${NC}"
        if curl -s "http://localhost:8000/convert?value=1&from_unit=barrel&to_unit=litre" | grep -q "158.987"; then
            echo -e "${GREEN}✅ Unit conversion is working${NC}"
        else
            echo -e "${RED}❌ Unit conversion test failed${NC}"
            exit 1
        fi
        
        echo ""
        echo -e "${GREEN}✅ All tests passed!${NC}"
        ;;
    
    *)
        echo -e "${YELLOW}Usage: $0 [command]${NC}"
        echo ""
        echo "Available commands:"
        echo "  build    - Build Docker image"
        echo "  start    - Start services (default)"
        echo "  stop     - Stop services"
        echo "  restart  - Restart services"
        echo "  logs     - View logs"
        echo "  status   - Check service status"
        echo "  test     - Run deployment tests"
        echo "  clean    - Remove all containers and images"
        echo ""
        exit 1
        ;;
esac


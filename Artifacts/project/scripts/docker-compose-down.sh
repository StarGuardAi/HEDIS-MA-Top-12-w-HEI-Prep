#!/bin/bash
# HEDIS Portfolio Optimizer - Docker Compose Down Script

set -e  # Exit on error

echo "🛑 Stopping HEDIS Portfolio Optimizer..."
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Change to project root
cd "$PROJECT_ROOT"

# Parse arguments
MODE="${1:-dev}"
REMOVE_VOLUMES="${2:-}"

if [ "$MODE" == "prod" ]; then
    COMPOSE_FILE="docker-compose.prod.yml"
elif [ "$MODE" == "dev" ]; then
    COMPOSE_FILE="docker-compose.yml"
else
    echo "❌ Invalid mode: $MODE"
    echo "Usage: $0 [dev|prod] [--volumes]"
    exit 1
fi

# Stop and remove containers
if [ "$REMOVE_VOLUMES" == "--volumes" ]; then
    echo "🗑️  Removing containers, networks, and volumes..."
    docker-compose -f "$COMPOSE_FILE" down -v
else
    echo "🛑 Stopping containers and removing networks..."
    docker-compose -f "$COMPOSE_FILE" down
fi

echo ""
echo "✅ Services stopped successfully!"
echo ""

if [ "$REMOVE_VOLUMES" != "--volumes" ]; then
    echo "💡 Note: Data volumes were preserved."
    echo "   To remove volumes as well, run:"
    echo "   $0 $MODE --volumes"
    echo ""
fi




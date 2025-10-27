#!/bin/bash
# HEDIS Portfolio Optimizer - Docker Compose Up Script

set -e  # Exit on error

echo "🐳 Starting HEDIS Portfolio Optimizer with Docker Compose..."
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Change to project root
cd "$PROJECT_ROOT"

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose not found. Please install it first."
    echo "   https://docs.docker.com/compose/install/"
    exit 1
fi

# Parse arguments
MODE="${1:-dev}"
PROFILE="${2:-}"

if [ "$MODE" == "prod" ]; then
    COMPOSE_FILE="docker-compose.prod.yml"
    echo "🚀 Starting in PRODUCTION mode..."
elif [ "$MODE" == "dev" ]; then
    COMPOSE_FILE="docker-compose.yml"
    echo "🔧 Starting in DEVELOPMENT mode..."
else
    echo "❌ Invalid mode: $MODE"
    echo "Usage: $0 [dev|prod] [profile]"
    exit 1
fi

# Build and start services
echo "🔨 Building and starting services..."
echo ""

if [ -n "$PROFILE" ]; then
    docker-compose -f "$COMPOSE_FILE" --profile "$PROFILE" up --build -d
else
    docker-compose -f "$COMPOSE_FILE" up --build -d
fi

echo ""
echo "✅ Services started successfully!"
echo ""

# Show running containers
echo "📊 Running Services:"
docker-compose -f "$COMPOSE_FILE" ps
echo ""

# Wait for API health check
echo "⏳ Waiting for API to be healthy..."
for i in {1..60}; do
    if curl -f -s http://localhost:8000/api/v1/health >/dev/null 2>&1; then
        echo "✅ API is healthy!"
        break
    fi
    if [ $i -eq 60 ]; then
        echo "❌ API health check failed after 60 seconds"
        echo "📋 Logs:"
        docker-compose -f "$COMPOSE_FILE" logs api
        exit 1
    fi
    echo -n "."
    sleep 1
done

echo ""
echo "🌐 Available Services:"
echo "  - API: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo "  - Database: localhost:5432"
echo "  - Redis: localhost:6379"
if [ "$MODE" == "dev" ] && [ "$PROFILE" == "tools" ]; then
    echo "  - pgAdmin: http://localhost:5050"
fi
echo ""

echo "📋 Useful Commands:"
echo "  - View logs: docker-compose -f $COMPOSE_FILE logs -f"
echo "  - Stop services: docker-compose -f $COMPOSE_FILE down"
echo "  - Restart API: docker-compose -f $COMPOSE_FILE restart api"
echo ""

echo "🎉 HEDIS Portfolio Optimizer is running!"



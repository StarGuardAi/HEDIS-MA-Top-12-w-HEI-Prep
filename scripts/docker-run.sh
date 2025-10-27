#!/bin/bash
# HEDIS Portfolio Optimizer - Docker Run Script

set -e  # Exit on error

echo "🐳 Starting HEDIS Portfolio Optimizer..."
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Change to project root
cd "$PROJECT_ROOT"

# Configuration
IMAGE_NAME="${IMAGE_NAME:-hedis-portfolio-api}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
CONTAINER_NAME="${CONTAINER_NAME:-hedis_api_standalone}"
PORT="${PORT:-8000}"

# Check if image exists
if ! docker images "$IMAGE_NAME:$IMAGE_TAG" | grep -q "$IMAGE_NAME"; then
    echo "❌ Docker image not found: $IMAGE_NAME:$IMAGE_TAG"
    echo "🔨 Building image first..."
    ./scripts/docker-build.sh
fi

# Stop and remove existing container if running
if docker ps -a --format '{{.Names}}' | grep -q "^$CONTAINER_NAME$"; then
    echo "🛑 Stopping existing container..."
    docker stop "$CONTAINER_NAME" >/dev/null 2>&1 || true
    docker rm "$CONTAINER_NAME" >/dev/null 2>&1 || true
fi

echo "📋 Run Configuration:"
echo "  - Image: $IMAGE_NAME:$IMAGE_TAG"
echo "  - Container: $CONTAINER_NAME"
echo "  - Port: $PORT"
echo ""

# Run the container
echo "🚀 Starting container..."
docker run -d \
  --name "$CONTAINER_NAME" \
  -p "$PORT:8000" \
  -e ENVIRONMENT=development \
  -e LOG_LEVEL=INFO \
  -e LOAD_MODELS_ON_STARTUP=false \
  -v "$(pwd)/models:/app/models" \
  -v "$(pwd)/logs:/app/logs" \
  "$IMAGE_NAME:$IMAGE_TAG"

echo ""
echo "✅ Container started successfully!"
echo ""

# Wait for health check
echo "⏳ Waiting for API to be healthy..."
for i in {1..30}; do
    if curl -f -s http://localhost:$PORT/api/v1/health >/dev/null 2>&1; then
        echo "✅ API is healthy!"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ API health check failed after 30 seconds"
        echo "📋 Container logs:"
        docker logs "$CONTAINER_NAME"
        exit 1
    fi
    echo -n "."
    sleep 1
done

echo ""
echo "📊 Container Status:"
docker ps --filter "name=$CONTAINER_NAME" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo ""

echo "🌐 API Endpoints:"
echo "  - Health: http://localhost:$PORT/api/v1/health"
echo "  - Docs: http://localhost:$PORT/docs"
echo "  - Measures: http://localhost:$PORT/api/v1/measures"
echo ""

echo "📋 To view logs:"
echo "  docker logs -f $CONTAINER_NAME"
echo ""

echo "🛑 To stop:"
echo "  docker stop $CONTAINER_NAME"
echo ""



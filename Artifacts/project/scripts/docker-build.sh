#!/bin/bash
# HEDIS Portfolio Optimizer - Docker Build Script

set -e  # Exit on error

echo "🐳 Building HEDIS Portfolio Optimizer Docker Image..."
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Change to project root
cd "$PROJECT_ROOT"

# Configuration
IMAGE_NAME="${IMAGE_NAME:-hedis-portfolio-api}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
VCS_REF=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")

echo "📋 Build Configuration:"
echo "  - Image: $IMAGE_NAME:$IMAGE_TAG"
echo "  - Build Date: $BUILD_DATE"
echo "  - Git Commit: $VCS_REF"
echo ""

# Build the Docker image
echo "🔨 Building Docker image..."
docker build \
  --build-arg BUILD_DATE="$BUILD_DATE" \
  --build-arg VCS_REF="$VCS_REF" \
  --tag "$IMAGE_NAME:$IMAGE_TAG" \
  --tag "$IMAGE_NAME:$VCS_REF" \
  --file Dockerfile \
  .

echo ""
echo "✅ Docker image built successfully!"
echo ""
echo "📦 Image Details:"
docker images "$IMAGE_NAME" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"
echo ""

# Optional: Run image size check
IMAGE_SIZE=$(docker images "$IMAGE_NAME:$IMAGE_TAG" --format "{{.Size}}")
echo "💾 Image Size: $IMAGE_SIZE"

if [[ "$IMAGE_SIZE" == *"GB"* ]]; then
    SIZE_NUM=$(echo "$IMAGE_SIZE" | grep -oE '[0-9]+\.?[0-9]*')
    if (( $(echo "$SIZE_NUM > 1.0" | bc -l) )); then
        echo "⚠️  WARNING: Image size is large (> 1GB). Consider optimization."
    fi
fi

echo ""
echo "🚀 To run the container:"
echo "  docker run -p 8000:8000 $IMAGE_NAME:$IMAGE_TAG"
echo ""
echo "🐳 Or use docker-compose:"
echo "  docker-compose up"
echo ""




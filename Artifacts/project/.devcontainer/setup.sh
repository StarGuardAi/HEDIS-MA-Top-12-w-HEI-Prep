#!/bin/bash
# HEDIS GSD Prediction Engine - Development Container Setup Script

set -e

echo "🚀 Setting up HEDIS GSD Prediction Engine development environment..."

# Update package lists
echo "📦 Updating package lists..."
sudo apt-get update

# Install additional system dependencies
echo "🔧 Installing system dependencies..."
sudo apt-get install -y \
    graphviz \
    libgraphviz-dev \
    pkg-config \
    build-essential

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Set up pre-commit hooks
echo "🔍 Setting up pre-commit hooks..."
pre-commit install

# Create necessary directories
echo "📁 Creating project directories..."
mkdir -p data/raw data/processed
mkdir -p models
mkdir -p reports/figures
mkdir -p logs

# Set up Jupyter configuration
echo "📓 Configuring Jupyter..."
jupyter lab --generate-config
echo "c.ServerApp.ip = '0.0.0.0'" >> ~/.jupyter/jupyter_lab_config.py
echo "c.ServerApp.allow_root = True" >> ~/.jupyter/jupyter_lab_config.py
echo "c.ServerApp.open_browser = False" >> ~/.jupyter/jupyter_lab_config.py

# Set environment variables
echo "🔧 Setting environment variables..."
export PYTHONPATH="/workspaces/hedis-gsd-prediction-engine:$PYTHONPATH"
echo 'export PYTHONPATH="/workspaces/hedis-gsd-prediction-engine:$PYTHONPATH"' >> ~/.bashrc

# Run initial tests
echo "🧪 Running initial tests..."
python -m pytest tests/ -v --tb=short

echo "✅ Development environment setup complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Run 'jupyter lab' to start Jupyter Lab"
echo "2. Run 'python -m pytest' to run all tests"
echo "3. Run 'bash scripts/pre-commit-checks.sh' for code quality checks"
echo ""
echo "📚 Useful commands:"
echo "- Start Jupyter: jupyter lab --ip=0.0.0.0 --port=8888 --no-browser"
echo "- Run tests: python -m pytest tests/ -v"
echo "- Format code: black . && isort ."
echo "- Lint code: flake8 . && pylint src/"

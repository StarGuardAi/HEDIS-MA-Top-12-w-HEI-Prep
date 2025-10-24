mcr.microsoft.com/devcontainers/python:3.11-bullseye

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    vim \
    wget \
    unzip \
    graphviz \
    libgraphviz-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Install additional development tools
RUN pip install --no-cache-dir \
    pre-commit \
    jupyterlab \
    notebook \
    ipywidgets

# Set up Jupyter configuration
RUN jupyter lab --generate-config
RUN echo "c.ServerApp.ip = '0.0.0.0'" >> /home/vscode/.jupyter/jupyter_lab_config.py
RUN echo "c.ServerApp.allow_root = True" >> /home/vscode/.jupyter/jupyter_lab_config.py
RUN echo "c.ServerApp.open_browser = False" >> /home/vscode/.jupyter/jupyter_lab_config.py

# Create workspace directory
RUN mkdir -p /workspaces/hedis-gsd-prediction-engine
WORKDIR /workspaces/hedis-gsd-prediction-engine

# Set environment variables
ENV PYTHONPATH=/workspaces/hedis-gsd-prediction-engine
ENV JUPYTER_ENABLE_LAB=yes

# Expose ports
EXPOSE 8888 8000

# Set the default command
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]

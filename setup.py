"""
Setup script for HEDIS Star Rating Portfolio Optimizer

An enterprise-grade AI platform for optimizing HEDIS Star Rating performance across
12 quality measures with portfolio-level ROI analysis and Health Equity Index (HEI) compliance.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

# Get version
def get_version():
    version_file = os.path.join("src", "__init__.py")
    if os.path.exists(version_file):
        with open(version_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("__version__"):
                    return line.split("=")[1].strip().strip('"').strip("'")
    return "1.0.0"

setup(
    name="hedis-star-rating-portfolio-optimizer",
    version="2.0.0",
    author="Robert Reichert",
    author_email="robert.reichert99@gmail.com",
    description="12-measure AI platform for Medicare Advantage Star Rating optimization with Health Equity Index compliance",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/bobareichert/HEDIS-MA-Top-12-w-HEI-Prep",
    project_urls={
        "Bug Reports": "https://github.com/bobareichert/HEDIS-MA-Top-12-w-HEI-Prep/issues",
        "Source": "https://github.com/bobareichert/HEDIS-MA-Top-12-w-HEI-Prep",
        "Documentation": "https://github.com/bobareichert/HEDIS-MA-Top-12-w-HEI-Prep/docs",
        "Portfolio": "https://hedis-gap-in-care-prediction-engine.my.canva.site/",
        "Live Demo": "https://hedis-ma-top-12-w-hei-prep.streamlit.app/",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Office/Business :: Financial",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "pytest-mock>=3.8.0",
            "flake8>=5.0.0",
            "black>=22.0.0",
            "isort>=5.10.0",
            "pre-commit>=2.20.0",
        ],
        "api": [
            "fastapi>=0.85.0",
            "uvicorn>=0.18.0",
            "pydantic>=1.10.0",
        ],
        "ml": [
            "shap>=0.41.0",
            "xgboost>=1.6.0",
            "lightgbm>=3.3.0",
        ],
        "viz": [
            "plotly>=5.10.0",
            "seaborn>=0.11.0",
        ],
        "jupyter": [
            "jupyter>=1.0.0",
            "ipykernel>=6.15.0",
            "nbformat>=5.4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "hedis-train=src.models.trainer:main",
            "hedis-predict=src.models.predictor:main",
            "hedis-evaluate=src.models.evaluator:main",
            "hedis-hipaa-scan=scripts.hipaa_scanner:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.yaml", "*.yml", "*.json", "*.md", "*.txt"],
    },
    data_files=[
        ("config", ["config.yaml", "config_dev.yaml", "config_prod.yaml"]),
        ("docs", ["README.md", "LICENSE"]),
        ("scripts", ["scripts/hipaa-scanner.py", "scripts/pre-commit-checks.sh"]),
    ],
    keywords=[
        "hedis",
        "star-ratings",
        "portfolio-optimization",
        "medicare-advantage",
        "health-equity",
        "healthcare",
        "machine-learning",
        "prediction",
        "roi-analysis",
        "quality-measures",
        "diabetes",
        "cardiovascular",
        "cancer-screening",
        "hipaa",
        "compliance",
        "clinical-decision-support",
        "value-based-care",
    ],
    zip_safe=False,
    test_suite="tests",
    tests_require=[
        "pytest>=7.0.0",
        "pytest-cov>=3.0.0",
        "pytest-mock>=3.8.0",
    ],
)

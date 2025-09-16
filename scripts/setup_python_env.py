#!/usr/bin/env python3
"""
Python Environment Setup Script for MMM Project

This script sets up the Python environment and installs required packages.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    print(f"   Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        return False
    
    print("✅ Python version is compatible")
    return True


def install_packages():
    """Install required packages."""
    print("📦 Installing required packages...")
    
    # Core packages first
    core_packages = [
        "pandas>=1.5.0",
        "numpy>=1.21.0", 
        "matplotlib>=3.5.0",
        "seaborn>=0.11.0",
        "scipy>=1.9.0",
        "statsmodels>=0.13.0",
        "openpyxl>=3.0.0",
        "xlrd>=2.0.0"
    ]
    
    for package in core_packages:
        if not run_command(f"pip install {package}", f"Installing {package}"):
            return False
    
    # Bayesian modeling packages
    bayesian_packages = [
        "pymc>=5.0.0",
        "arviz>=0.12.0",
        "xarray>=2022.0.0"
    ]
    
    for package in bayesian_packages:
        if not run_command(f"pip install {package}", f"Installing {package}"):
            print(f"⚠️  Warning: {package} installation failed, continuing...")
    
    # Development tools
    dev_packages = [
        "jupyter>=1.0.0",
        "ipykernel>=6.0.0",
        "notebook>=6.4.0",
        "pytest>=7.0.0"
    ]
    
    for package in dev_packages:
        if not run_command(f"pip install {package}", f"Installing {package}"):
            print(f"⚠️  Warning: {package} installation failed, continuing...")
    
    return True


def verify_installation():
    """Verify that packages are installed correctly."""
    print("🔍 Verifying installation...")
    
    packages_to_test = [
        "pandas",
        "numpy", 
        "matplotlib",
        "seaborn",
        "scipy",
        "statsmodels",
        "pymc"
    ]
    
    for package in packages_to_test:
        try:
            __import__(package)
            print(f"✅ {package} imported successfully")
        except ImportError as e:
            print(f"❌ {package} import failed: {e}")
            return False
    
    return True


def create_jupyter_kernel():
    """Create a Jupyter kernel for the project."""
    print("📓 Setting up Jupyter kernel...")
    
    kernel_name = "mmm-project"
    
    # Create kernel spec
    kernel_spec = {
        "argv": [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"],
        "display_name": "MMM Project",
        "language": "python",
        "metadata": {
            "debugger": True
        }
    }
    
    try:
        import jupyter_client
        from jupyter_client.kernelspec import KernelSpecManager
        
        ksm = KernelSpecManager()
        ksm.install_kernel_spec(
            kernel_spec=kernel_spec,
            kernel_name=kernel_name,
            user=True
        )
        
        print(f"✅ Jupyter kernel '{kernel_name}' created successfully")
        return True
        
    except Exception as e:
        print(f"⚠️  Warning: Could not create Jupyter kernel: {e}")
        return False


def main():
    """Main setup function."""
    print("🚀 Setting up Python Environment for MMM Project")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install packages
    if not install_packages():
        print("❌ Package installation failed")
        return False
    
    # Verify installation
    if not verify_installation():
        print("❌ Package verification failed")
        return False
    
    # Create Jupyter kernel
    create_jupyter_kernel()
    
    print("\n🎉 Python environment setup complete!")
    print("\nNext steps:")
    print("1. Run data transformation: python scripts/transform_hcp_to_mmm.py")
    print("2. Start Jupyter: jupyter notebook")
    print("3. Use the 'MMM Project' kernel for notebooks")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

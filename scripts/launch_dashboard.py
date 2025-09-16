#!/usr/bin/env python3
"""
Dashboard Launcher Script
========================

Simple script to launch the EDA dashboard with proper setup.

Usage:
    python scripts/launch_dashboard.py

Author: AI Assistant
Date: 2024
"""

import subprocess
import sys
import os

def install_streamlit():
    """Install Streamlit if not already installed."""
    try:
        import streamlit
        print("✅ Streamlit is already installed")
        return True
    except ImportError:
        print("📦 Installing Streamlit...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit>=1.25.0"])
            print("✅ Streamlit installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install Streamlit: {e}")
            return False

def launch_dashboard():
    """Launch the Streamlit dashboard."""
    dashboard_path = os.path.join(os.path.dirname(__file__), "eda_dashboard.py")
    
    if not os.path.exists(dashboard_path):
        print(f"❌ Dashboard file not found: {dashboard_path}")
        return False
    
    print("🚀 Launching EDA Dashboard...")
    print("📊 Dashboard will open in your browser at: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the dashboard")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", dashboard_path])
        return True
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")
        return True
    except Exception as e:
        print(f"❌ Error launching dashboard: {e}")
        return False

def main():
    """Main launcher function."""
    print("🎯 MMM EDA Dashboard Launcher")
    print("=" * 40)
    
    # Check if data files exist
    data_files = [
        "data/processed/dma_aggregated_data.csv",
        "data/processed/national_aggregated_data.csv", 
        "data/processed/dma_channel_data.csv",
        "data/processed/national_channel_data.csv"
    ]
    
    missing_files = [f for f in data_files if not os.path.exists(f)]
    if missing_files:
        print("⚠️  Warning: Some data files are missing:")
        for f in missing_files:
            print(f"   - {f}")
        print("\n💡 Run the data transformation script first:")
        print("   python scripts/run_data_transformation.py")
        print()
    
    # Install Streamlit
    if not install_streamlit():
        return False
    
    # Launch dashboard
    return launch_dashboard()

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)

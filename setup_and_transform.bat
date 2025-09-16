@echo off
echo 🚀 Setting up Python Environment for MMM Project
echo ================================================

echo.
echo 📋 Python Setup Instructions:
echo.
echo 1. Install Python from https://www.python.org/downloads/
echo    - Download Python 3.8 or higher
echo    - During installation, check "Add Python to PATH"
echo    - Choose "Install for all users" if possible
echo.
echo 2. After installation, restart this terminal
echo.
echo 3. Run this script again to continue with data transformation
echo.

echo 🔍 Checking for Python installation...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Python is installed and available
    echo.
    echo 📦 Installing required packages...
    pip install pandas numpy matplotlib seaborn scipy statsmodels openpyxl xlrd
    echo.
    echo 🔄 Running data transformation...
    python scripts/run_data_transformation.py
) else (
    echo ❌ Python not found or not in PATH
    echo.
    echo 📥 Please install Python first:
    echo    1. Go to https://www.python.org/downloads/
    echo    2. Download Python 3.8 or higher
    echo    3. Run installer and check "Add Python to PATH"
    echo    4. Restart terminal and run this script again
    echo.
    echo 🔧 Alternative: Use Anaconda/Miniconda
    echo    1. Download from https://www.anaconda.com/products/distribution
    echo    2. Install Anaconda
    echo    3. Open Anaconda Prompt
    echo    4. Navigate to this project folder
    echo    5. Run: conda install pandas numpy matplotlib seaborn scipy statsmodels openpyxl xlrd
    echo    6. Run: python scripts/run_data_transformation.py
)

echo.
echo 📋 Next Steps After Python Setup:
echo    1. ✅ Install Python and required packages
echo    2. 🔄 Run data transformation script
echo    3. 📊 Review generated visualizations
echo    4. 🏗️ Proceed with MMM model development
echo.
pause

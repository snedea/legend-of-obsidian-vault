@echo off
REM Legend of the Obsidian Vault - Game Launcher (Windows)

cd /d "%~dp0"

echo 🎮 Legend of the Obsidian Vault - Starting Game
echo ================================================

REM Check if Python 3 is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is required but not installed
    echo    Please install Python 3.7+ from python.org and try again
    pause
    exit /b 1
)

REM Check if this is first run (no saves directory or missing dependencies)
if not exist "saves" goto setup
python -c "import textual" >nul 2>&1
if errorlevel 1 goto setup
goto run

:setup
echo 🔧 First time setup - installing dependencies...
python setup.py
if errorlevel 1 (
    echo ❌ Setup failed. Please check the error messages above.
    pause
    exit /b 1
)
echo.

:run
REM Start the game
echo 🚀 Starting Legend of the Obsidian Vault...
python lov.py

REM Keep terminal open if there was an error
if errorlevel 1 (
    echo.
    echo ❌ Game exited with an error
    pause
)
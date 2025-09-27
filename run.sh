#!/bin/bash
# Legend of the Obsidian Vault - Game Launcher (Mac/Linux)

cd "$(dirname "$0")"

echo "🎮 Legend of the Obsidian Vault - Starting Game"
echo "================================================"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    echo "   Please install Python 3.7+ and try again"
    exit 1
fi

# Check if this is first run (no saves directory or missing dependencies)
echo "🔍 Checking dependencies..."

missing_deps=false

# Check for required packages
required_packages=("textual" "rich" "llama_cpp")
for package in "${required_packages[@]}"; do
    if ! python3 -c "import $package" 2>/dev/null; then
        missing_deps=true
        break
    fi
done

# Check for saves directory
if [ ! -d "saves" ]; then
    missing_deps=true
fi

if [ "$missing_deps" = true ]; then
    echo "🔧 Installing dependencies and setting up game..."
    python3 setup.py
    if [ $? -ne 0 ]; then
        echo "❌ Setup failed. Please check the error messages above."
        echo "💡 You may need to upgrade pip: python3 -m pip install --upgrade pip"
        exit 1
    fi
    echo "✅ Setup completed successfully!"
    echo ""
else
    echo "✅ All dependencies found"
fi

# Start the game
echo "🚀 Starting Legend of the Obsidian Vault..."
python3 lov.py

# Keep terminal open if there was an error
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Game exited with an error"
    echo "Press Enter to close..."
    read
fi
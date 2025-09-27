#!/usr/bin/env python3
"""
Setup script for Legend of the Obsidian Vault
Automatically installs dependencies and prepares the game for first run
"""
import subprocess
import sys
import os
from pathlib import Path

def check_python_version():
    """Ensure Python 3.7+ is being used"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detected")

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")

    requirements_file = Path(__file__).parent / "requirements.txt"
    if not requirements_file.exists():
        print("❌ requirements.txt not found")
        sys.exit(1)

    try:
        # Try pip3 first, then pip
        pip_cmd = "pip3" if subprocess.run(["which", "pip3"], capture_output=True).returncode == 0 else "pip"

        # Install requirements
        cmd = [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)]
        print(f"   Running: {' '.join(cmd)}")

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print("❌ Failed to install dependencies")
            print(f"Error: {result.stderr}")

            # Try alternative installation methods
            print("🔄 Trying alternative installation...")
            alt_cmd = [pip_cmd, "install", "-r", str(requirements_file)]
            alt_result = subprocess.run(alt_cmd, capture_output=True, text=True)

            if alt_result.returncode != 0:
                print("❌ Alternative installation also failed")
                print("Please install dependencies manually:")
                print(f"   {pip_cmd} install -r requirements.txt")
                sys.exit(1)

        print("✅ Dependencies installed successfully")

    except Exception as e:
        print(f"❌ Installation error: {e}")
        print("Please install dependencies manually:")
        print("   pip3 install -r requirements.txt")
        sys.exit(1)

def check_game_files():
    """Verify all game files are present"""
    required_files = [
        "lov.py",
        "game_data.py",
        "obsidian.py",
        "brainbot.py"
    ]

    missing_files = []
    game_dir = Path(__file__).parent

    for file in required_files:
        if not (game_dir / file).exists():
            missing_files.append(file)

    if missing_files:
        print(f"❌ Missing game files: {', '.join(missing_files)}")
        sys.exit(1)

    print("✅ All game files present")

def create_saves_directory():
    """Create saves directory if it doesn't exist"""
    saves_dir = Path(__file__).parent / "saves"
    if not saves_dir.exists():
        saves_dir.mkdir()
        print("✅ Created saves directory")
    else:
        print("✅ Saves directory exists")

def main():
    """Main setup process"""
    print("🎮 Legend of the Obsidian Vault - Setup")
    print("=" * 50)

    check_python_version()
    check_game_files()
    install_dependencies()
    create_saves_directory()

    print()
    print("🎉 Setup complete!")
    print()
    print("To start the game:")
    print("   python3 lov.py")
    print()
    print("Or use the convenience scripts:")
    print("   ./run.sh      (Mac/Linux)")
    print("   run.bat       (Windows)")

if __name__ == "__main__":
    main()
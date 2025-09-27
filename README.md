# Legend of the Obsidian Vault (LOV) v0.0.1

> **Pre-Alpha Release**: An exact clone of Legend of the Red Dragon (LORD) v4.00a with intelligent Obsidian vault integration

Transform your forgotten notes into epic forest battles! This authentic BBS door game recreates the classic LORD experience while your Obsidian vault becomes a living dungeon of knowledge-based enemies.

![Game Status: Pre-Alpha](https://img.shields.io/badge/Status-Pre--Alpha-orange)
![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-green)

## 🎮 What Works (v0.0.1)

### ✅ **Core Features**
- **Authentic BBS Interface**: VGA/ANSI color terminal with exact LORD styling
- **Character Creation**: All 3 classes (Death Knight, Mystical, Thieving)
- **Forest Combat**: Note-based enemies with intelligent quiz attacks
- **Obsidian Integration**: Auto-detects vault, converts 1700+ notes to enemies
- **TinyLlama AI**: Local AI generates contextual quiz questions from note content
- **Town Square**: Navigation and basic menu system
- **Player Stats**: Leveling, hitpoints, attack/defense progression
- **Save System**: SQLite database with persistent character data

### 🧠 **AI-Enhanced Combat**
- **Note-Based Enemies**: "Mosquito of Machine Learning" instead of generic monsters
- **Intelligent Questions**: AI analyzes note content for contextual quiz generation
- **Knowledge Combat**: Answer correctly for 2x damage critical hits
- **Smart Fallback**: Regex-based questions when AI unavailable
- **Answer Validation**: Accepts variations of correct answers

### 📝 **Obsidian Features**
- **Auto-Detection**: Finds vault in common locations including iCloud
- **1700+ Notes Supported**: Handles large vaults efficiently
- **Difficulty Scaling**: Note age influences enemy strength
- **Real-time Display**: Shows vault status and note count in forest

## 🚧 What's Missing (See TODO.md)

This is a **pre-alpha release**. Major LORD features still need implementation:

- **Inn System**: Violet flirtation, Seth's songs, bar room
- **Shop Functionality**: Weapons/armor purchasing
- **Banking**: Interest, deposits, withdrawals
- **PvP Combat**: Player vs player battles
- **Daily Systems**: News, announcements, time-based events
- **Random Events**: Olivia's head, old man, fairy encounters
- **Marriage System**: Conjugality list and weddings

## 🚀 Quick Start

### Prerequisites
- **Python 3.9+**
- **Terminal with 256 color support**
- **Obsidian vault** (optional but recommended)

### Installation

```bash
# Clone the repository
git clone https://github.com/snedea/legend-of-obsidian-vault.git
cd legend-of-obsidian-vault

# Install dependencies
pip install -r requirements.txt

# Run the game
python3 lov.py
```

### First Run Setup

1. **Create Character**: Choose `(N)ew Character`
2. **Enter Details**: Name (max 20 chars), gender, class
3. **Vault Detection**: Game auto-finds your Obsidian vault
4. **Enter Forest**: Press `(F)` then `(E)` to fight note-based enemies
5. **Quiz Combat**: Use `(Q)uiz Attack` for 2x damage

## 🎯 How to Play

### Character Classes
- **Death Knight (K)**: Killing woodland creatures
- **Mystical (P)**: Dabbling in mystical forces
- **Thieving (D)**: Lying, cheating, and stealing

### Combat System
```
**FIGHT**
========================================
You have encountered Mosquito of Machine Learning!!

📝 Note-Based Enemy: 'Machine Learning Fundamentals'
🧠 AI-Enhanced Combat (intelligent questions available)

This creature guards knowledge of 'Machine Learning Fundamentals'.
Test your knowledge for bonus damage!

(A)ttack
(Q)uiz Attack (2x damage if correct)
(S)tats
(R)un
```

### Knowledge Combat
- **Quiz Questions**: AI generates questions from your note content
- **Critical Hits**: Correct answers deal 2x damage
- **Smart Validation**: Accepts variations of correct answers
- **Fallback Mode**: Works without AI using pattern matching

## 🧠 AI Integration

### TinyLlama Model
- **Local Processing**: 670MB model downloads automatically
- **Offline Operation**: No internet required after setup
- **BrainBot Compatible**: Shares model with existing BrainBot installation
- **Background Loading**: Initializes without blocking game startup

### AI vs Fallback Mode

| Feature | With TinyLlama AI | Fallback Mode |
|---------|------------------|---------------|
| Quiz Questions | Context-aware, intelligent | Regex pattern matching |
| Answer Validation | Semantic similarity | Keyword matching |
| Performance | ~2-3 seconds | Instant |
| Setup | Auto-downloads model | No setup needed |

## 📁 Obsidian Vault Setup

### Auto-Detection Locations
```bash
~/Documents/Obsidian Vault
~/Library/Mobile Documents/iCloud~md~obsidian/Documents  # iCloud
~/Obsidian
~/Notes
~/vault
```

### Manual Configuration
1. Main menu → `(V)ault Settings`
2. Enter full path to vault folder
3. Game will scan and display note count

### Difficulty Scaling
- **Recent notes** (< 7 days): Level 1-2 enemies
- **Medium age** (1-3 months): Level 3-9 enemies
- **Old notes** (3+ months): Level 10-12 enemies

## 🏗️ Architecture

### Core Files
- **`lov.py`**: Main Textual application and screens
- **`game_data.py`**: Character, weapons, armor, database
- **`obsidian.py`**: Vault scanning and note processing
- **`brainbot.py`**: TinyLlama AI integration

### Technology Stack
- **Textual**: Modern terminal UI framework
- **Rich**: Text formatting and colors
- **SQLite**: Player data persistence
- **llama-cpp-python**: Local AI inference
- **Hugging Face**: Model distribution

## 🎨 BBS Authenticity

### Visual Fidelity
- **True VGA Colors**: 16-color ANSI palette
- **Exact Layout**: Original LORD screen formatting
- **Terminal Interface**: No GUI, pure text-mode experience
- **Click + Keyboard**: Mouse support with keyboard shortcuts

### Gameplay Fidelity
- **Original Mechanics**: Same combat formulas and progression
- **Authentic Prices**: Exact LORD weapon/armor costs
- **Random Generation**: Maintains LORD's RNG patterns
- **Classic Text**: Original dialog and descriptions

## 📊 Development Status

### Version Roadmap
- **v0.0.1** (current): Core combat + Obsidian integration
- **v0.1.0**: Inn features (Violet, Seth, bar room)
- **v0.2.0**: Complete shop functionality
- **v0.3.0**: Banking and daily systems
- **v0.4.0**: PvP combat and rankings
- **v0.5.0**: Random events and special encounters
- **v1.0.0**: Feature-complete LORD clone

### Known Issues
- Shop purchasing not implemented
- Inn interactions missing
- Bank transactions non-functional
- PvP system placeholder only
- Daily news/events missing

## 🤝 Contributing

### Reporting Issues
- Use GitHub Issues for bugs and feature requests
- Include Python version, OS, and terminal type
- Provide steps to reproduce problems

### Development Setup
```bash
# Clone and setup development environment
git clone https://github.com/snedea/legend-of-obsidian-vault.git
cd legend-of-obsidian-vault
pip install -r requirements.txt

# Run in development mode
python3 lov.py
```

### Code Style
- Follow PEP 8 Python conventions
- Use type hints where appropriate
- Maintain LORD authenticity in game mechanics
- Add docstrings for new functions

## 📄 License

MIT License - see LICENSE file for details.

## 🎪 Credits

- **Original LORD**: Seth Able Robinson
- **Textual Framework**: Textualize.io
- **TinyLlama Model**: Microsoft Research
- **BrainBot Integration**: Inspired by local AI development

---

## 🎯 Ready to Battle Your Notes?

```bash
python3 lov.py
```

**Your forgotten knowledge awaits in the forest!** 🌲🗡️📚

*Will you conquer your procrastination or will it conquer you?*
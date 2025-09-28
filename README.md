# Legend of the Obsidian Vault (LOV) v0.0.4

> **Alpha Release**: Complete LORD Secrets implementation with all hidden features and authentic BBS experience

Transform your forgotten notes into epic forest battles! This authentic BBS door game recreates the classic LORD experience while your Obsidian vault becomes a living dungeon where AI generates rich, immersive encounters from your knowledge.

![Game Status: Alpha](https://img.shields.io/badge/Status-Alpha-brightgreen)
![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-green)

## 🎮 What Works (v0.0.4)

### ✅ **Core Features**
- **Authentic BBS Interface**: VGA/ANSI color terminal with exact LORD styling
- **Character Creation**: All 3 classes (Death Knight, Mystical, Thieving)
- **Forest Combat**: Note-based enemies with intelligent quiz attacks
- **Obsidian Integration**: Auto-detects vault, converts 1700+ notes to enemies
- **TinyLlama AI**: Local AI generates contextual quiz questions from note content
- **Town Square**: Navigation and basic menu system
- **Player Stats**: Leveling, hitpoints, attack/defense progression
- **Save System**: SQLite database with persistent character data

### 🏪 **Functional Shops**
- **Healer's Hut**: Full heal (level-based pricing) or partial heal (1 gold per HP)
- **Ye Old Bank**: Deposits, withdrawals, 10% daily interest compound (+ hidden robbery for thieves!)
- **Abdul's Armor**: Progressive armor upgrades with authentic LORD pricing
- **Authentic Economics**: Exact LORD pricing and progression maintained

### 🧠 **AI-Enhanced Combat**
- **Rich Dungeon Master Narratives**: AI generates immersive 4-6 sentence encounter descriptions
- **Content-Aware Stories**: Incorporates specific details from your notes (numbers, concepts, lists)
- **Atmospheric World-Building**: "You enter the Algorithm Archive where 27 mystical patterns swirl..."
- **TinyLlama Integration**: Local 1.1B parameter model for intelligent narrative generation
- **Intelligent Questions**: AI analyzes note content for contextual quiz generation
- **Knowledge Combat**: Answer correctly for 2x damage critical hits
- **Smart Fallback**: Enhanced fallback narratives when AI unavailable
- **Answer Validation**: Accepts variations of correct answers

### 🎨 **Enhanced UI/UX**
- **Final Fantasy-Style Combat**: Clean enemy/player status layout with real-time updates
- **Unicode HP Bars**: Visual health indicators (█░░░░░░░░░ 30%) with percentage display
- **Colored ASCII Art**: Immersive Forest and Armor Shop headers with vibrant themes
- **Modular Architecture**: 36% code reduction with organized screen modules
- **Fixed Navigation**: All shop and screen transitions now work correctly

### 📝 **Obsidian Features**
- **Auto-Detection**: Finds vault in common locations including iCloud
- **1700+ Notes Supported**: Handles large vaults efficiently
- **Difficulty Scaling**: Note age influences enemy strength
- **Real-time Display**: Shows vault status and note count in forest

### 🎭 **LORD Secrets Features** ⭐ NEW in v0.0.4

Experience the complete, authentic LORD underground with all hidden features and secret systems!

#### **🌟 Hidden Command Systems**
- **Jennie Codes**: 13 secret commands in Forest (LADY, BABE, SEXY, FOXY, HOTT, FAIR, DUNG, UGLY, DUMB, STAR, NICE, COOL, GIFT)
  - Requires high spirits to activate
  - Special frog transformation mechanics (DUNG code)
  - Gold, stat boosts, extra fights, and mystical rewards

#### **🏰 In-Game Modules (IGMs)**
Accessible via "Other Places" from Town Square:

- **LORD Cavern**: Daily exploration system with Riddler encounters
  - 3 daily searches for treasures and stat boosts
  - 5 unique riddles with valuable rewards
  - Random encounters with gold, gems, and ancient power

- **Barak's House**: Scholar sanctuary and gambling den
  - Read ancient books for intelligence and stat gains
  - Practice combat techniques for random improvements
  - Basement dice games with high-stakes gambling

- **Fairy Garden**: Learn mystical healing arts
  - Purchase Fairy Lore (1000 gold) for combat healing
  - Heal 25-40% max HP during battles with (H)eal command
  - Practice sessions and advanced training available

- **Xenon's Storage Facility**: Strategic resource management
  - Store gold/gems with 5% daily fees
  - Purchase and name horses (500 gold)
  - Dark trading: Exchange children for gold, gems, or stat boosts

- **WereWolf Den**: Primal transformation curse
  - Learn werewolf curse (5000 gold) for PvP enhancement
  - Transform for +50% STR/DEF during combat
  - Steal 10% of defeated opponents' stats permanently
  - Risk: 20% chance of losing control each transformation

#### **🌌 Dimensional Travel**
- **Gateway Portal**: Access to scripted adventure realms
  - **Zycho Zircus**: Carnival games, freakshow encounters, ringmaster challenges
  - **Death's Mansion**: Meet Death himself, haunted rooms, forbidden knowledge
  - **Random Portals**: Completely unpredictable adventures across infinite realms
  - Portal activation costs 1 gem per destination

#### **🦹 Advanced Criminal Activities**
- **Bank Robbery** (Thief + Fairy Lore required)
  - Hidden (R)ob command in Ye Old Bank
  - Success based on thieving skill + level
  - Steal 10-30% of total bank deposits
  - Heavy penalties for failure (lose half gold, kicked out)

## 🚧 Remaining Features (See TODO.md)

This is now an **alpha release** with all major LORD Secrets implemented! Remaining features:

- **Inn System**: Violet flirtation, Seth's songs, bar room interactions
- **Weapons Shop**: King Arthur's Weapons purchasing system
- **PvP Combat**: Player vs player battle system (framework ready for werewolf stat stealing)
- **Daily Systems**: News announcements and time-based events
- **Random Events**: Olivia's head, old man encounters
- **Marriage System**: Conjugality list and wedding ceremonies

## 🎭 AI Narrative Examples (v0.0.2)

Experience dynamic, content-aware encounters that transform your notes into rich fantasy adventures:

### Before (v0.0.1)
```
Enemy: Mosquito of Machine Learning
Location: Forest clearing
```

### After (v0.0.2)
```
You enter the Algorithm Archive, where ancient knowledge of 'Machine Learning
Basics' has crystallized into living code. The air crackles with 27 different
patterns of mystical energy, each representing a layer of understanding.
Glowing runes spell out the eternal truth: 'Machine learning automates
analytical model building' as spectral frameworks stand sentinel over
accumulated wisdom.

Enemy: Guardian of Machine Learning    Location: Algorithm Archive
```

✨ **What Makes It Special:**
- Incorporates **specific numbers** from your notes (27, 5 layers, 1000 examples)
- References **actual concepts** from content (neural networks, frameworks)
- Weaves **note text** into magical fantasy descriptions
- Creates **atmospheric world-building** unique to each note

## 🚀 Quick Start

### Prerequisites
- **Python 3.7+**
- **Terminal with 256 color support**
- **Obsidian vault** (optional but recommended)

### Easy Installation (Recommended)

```bash
# Mac/Linux - One-click setup and launch
./run.sh

# Windows - One-click setup and launch
run.bat
```

The launcher scripts automatically:
- ✅ Install all dependencies
- ✅ Download AI models
- ✅ Create save directories
- ✅ Launch the game

### Manual Installation

```bash
# Install dependencies
python3 setup.py

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
- **`lov.py`**: Main Textual application and core screens
- **`game_data.py`**: Character, weapons, armor, database
- **`obsidian.py`**: Vault scanning and note processing
- **`brainbot.py`**: TinyLlama AI integration
- **`screens/igm/`**: Complete In-Game Module system (8 IGM locations)
- **`screens/combat/`**: Combat and forest exploration
- **`screens/town/`**: Town Square and all shop systems

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
- **v0.0.1**: Core combat + Obsidian integration ✅
- **v0.0.2**: AI-powered dungeon master narratives ✅
- **v0.0.3**: Complete shop functionality ✅
- **v0.0.4** (current): Complete LORD Secrets implementation ✅
- **v0.1.0**: Inn features (Violet, Seth, bar room)
- **v0.2.0**: PvP combat system (werewolf framework ready)
- **v0.3.0**: Daily systems and random events
- **v0.4.0**: Marriage system and conjugality
- **v1.0.0**: Feature-complete LORD clone with all original content

### Known Issues
- Weapons shop purchasing not implemented (armor shop functional)
- Inn interactions missing (Violet, Seth, bar room)
- PvP system placeholder only (werewolf framework ready)
- Daily news/events missing
- Marriage system not implemented

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
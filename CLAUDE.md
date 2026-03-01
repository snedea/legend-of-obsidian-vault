# CLAUDE.md - Developer Documentation

## TL;DR

Legend of the Obsidian Vault (LOV) is an authentic LORD v4.00a clone with Obsidian vault integration and AI-powered combat narratives.

- **Tech Stack**: Python 3.9+, Textual TUI, TinyLlama 1.1B AI, SQLite
- **Quick Start**: `./run.sh` (Mac/Linux) or `run.bat` (Windows)
- **Architecture**: Modular screens in `screens/` directory
- **Current Version**: v0.0.5 (LORD Secrets + AI narratives complete)
- **Troubleshooting**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Roadmap**: See [ROADMAP.md](ROADMAP.md)
- **Version History**: See [CHANGELOG.md](CHANGELOG.md)

## Table of Contents

- [Project Overview](#project-overview)
- [Architecture & Design](#architecture--design)
- [Core Components](#core-components)
- [Combat System](#combat-system)
- [AI Integration](#ai-integration)
- [Development Guide](#development-guide)
- [Performance & Optimization](#performance--optimization)
- [Known Technical Debt](#known-technical-debt)
- [Contributing](#contributing)
- [Credits & References](#credits--references)

## Project Overview

Legend of the Obsidian Vault demonstrates how modern AI can enhance retro gaming while maintaining authentic BBS gameplay mechanics. The game transforms your Obsidian notes into enemies, using note content to generate contextual quiz questions and immersive combat narratives.

### Core Principles

1. **Authenticity First**: Exact LORD v4.00a mechanics, pricing, and feel
2. **Knowledge Integration**: Transform note-taking into active gaming
3. **AI Enhancement**: Intelligent context without replacing human gameplay
4. **Terminal Native**: Pure text-mode experience with modern tooling

### Technology Stack

**Frontend Framework**
- **Textual 0.40.0+**: Modern Python TUI framework
- **Rich 13.0.0+**: Advanced text rendering and colors
- **ANSI/VGA Colors**: Authentic 16-color BBS palette

**AI Integration**
- **TinyLlama 1.1B**: Local language model (670MB)
- **llama-cpp-python**: CPU-optimized inference
- **Hugging Face Hub**: Model distribution and caching

**Data Layer**
- **SQLite3**: Player persistence and game state
- **Markdown Parsing**: Obsidian vault integration
- **File System Scanning**: Cross-platform vault detection

## Architecture & Design

### File Structure

```
legend-of-obsidian-vault/
├── lov.py              # Main Textual application
├── game_data.py        # Core game mechanics and data structures
├── obsidian.py         # Vault integration and note processing
├── brainbot.py         # TinyLlama AI integration
├── setup.py            # Auto-installer for dependencies
├── run.sh / run.bat    # Platform-specific launchers
├── screens/            # Modular screen system
│   ├── combat/         # Forest, Combat, Quiz screens
│   ├── town/           # TownSquare, Inn, Bank, Shops, etc.
│   ├── character/      # Creation, Selection, Stats
│   └── igm/            # In-Game Modules (8 locations)
├── saves/
│   └── players.db      # SQLite player data
└── demo_vault/         # Example notes for testing
```

### Modular Screen Architecture

**v0.0.3 Refactoring**: Reduced `lov.py` from 2,197 → 1,400 lines (36% reduction) by organizing screens into logical modules:

- **Combat System**: `screens/combat/` - Forest, CombatScreen, QuizScreen
- **Town Locations**: `screens/town/` - All 18+ town locations
- **Character Management**: `screens/character/` - Creation, selection, stats
- **IGM System**: `screens/igm/` - 8 LORD Secrets locations

**Key Pattern**: Delayed imports to resolve circular dependencies between screen modules.

## Core Components

### 1. Game Engine (lov.py)

**Main Application Class**
```python
class LordApp(App):
    """Main LORD application with authentic BBS styling"""
```

**Screen Navigation**
- Textual's screen stack system for authentic BBS feel
- Keyboard shortcuts match original LORD
- Global player state with screen isolation

### 2. Game Mechanics (game_data.py)

**Character System**
```python
@dataclass
class Character:
    name: str = ""
    level: int = 1
    hitpoints: int = 10
    max_hitpoints: int = 10
    # 37+ fields for complete LORD Secrets support
```

**Weapon/Armor Progression**
- **15 Weapon Tiers**: Stick (200g) → Death Sword (400M gold)
- **15 Armor Tiers**: Coat (200g) → Shimmering Armor (400M gold)
- **Exact LORD Pricing**: Authentic economic progression

**Authentic Combat Formula (LORD v4.00a)**
```python
# Source: RT Soft LORD FAQ
# HIT_AMOUNT = (strength/2) + random(strength/2) - defence

def player_attacks_enemy(player, enemy):
    # Monsters have NO defense in LORD
    strength = player.attack_power
    hit_amount = (strength // 2) + random.randint(0, strength // 2)
    return hit_amount if hit_amount > 0 else "MISS"

def enemy_attacks_player(enemy, player):
    strength = enemy.attack
    defense = player.defense_power
    hit_amount = (strength // 2) + random.randint(0, strength // 2) - defense
    return hit_amount if hit_amount > 0 else "MISS"
```

### 3. Obsidian Integration (obsidian.py)

**Vault Detection Logic**
Searches 15+ common locations:
- Standard Obsidian folders (`~/Documents/Obsidian/`)
- iCloud sync locations
- Custom user directories
- Fallback: any folder with 3+ `.md` files

**Note Processing Pipeline**
1. **Scan**: Recursive .md file discovery
2. **Parse**: Extract title, content, tags, metadata
3. **Classify**: Age-based difficulty assignment
4. **Cache**: 5-minute memory cache for performance

**Enemy Generation** (`obsidian.py:get_enemy_for_level`)
- Selects random note from vault
- Scales stats based on note age vs player level
- Generates creative enemy names: "Mosquito of Machine Learning"

### 4. AI Integration (brainbot.py)

**Local AI Architecture**
```python
class LocalAIClient:
    def __init__(self):
        self.model = None  # TinyLlama instance
        self.cache = {}    # 5-minute response cache
        self.available = False
```

**Background Initialization**
- Threading: AI loads without blocking game startup
- Graceful Degradation: Falls back to regex if AI fails
- Model Sharing: Uses existing BrainBot model cache

**Enemy Narrative Generation** (`brainbot.py:240-329`)
- `max_tokens=400` for rich 300-400 word descriptions
- Incorporates note content (headers, lists, numbers, bold text)
- Fallback to template-based narratives when AI unavailable

## Combat System

### Traditional Combat Flow
```
Player Turn → Enemy Turn → Damage Calculation → Victory/Defeat Check
```

### Knowledge Combat Enhancement
```
Quiz Question → User Input → AI Validation → Critical Hit (2x) or Miss → Continue Combat
```

### Combat Narrative System

**Three-Stage Pipeline**:
1. **Generation** → `brainbot.py` (AI) or `obsidian.py` (templates)
2. **Storage** → `Enemy.encounter_narrative` attribute
3. **Display** → `screens/combat/combat.py:47` renders with wrapping

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed narrative debugging guide.

### Quiz System

**Question Generation** (`brainbot.py`)
```python
def generate_quiz_question(self, note_title: str, note_content: str) -> QuizQuestion:
    prompt = f"""Based on this note about "{note_title}":
    {note_content[:500]}

    Generate a quiz question that tests understanding.

    Format:
    QUESTION: [your question]
    ANSWER: [short answer]
    TYPE: [definition/concept/fact]"""
```

**Answer Validation Logic**
- Exact match check
- AI semantic matching (50% word overlap threshold)
- Fallback keyword matching

## AI Integration

### What Works Well ✅
- **TinyLlama 1.1B Integration**: Local AI model running smoothly
- **Rich Combat Narratives**: 1600+ character immersive descriptions
- **Content-Aware Generation**: Incorporates note headers, lists, numbers
- **Response Caching**: 5-minute TTL prevents redundant generation
- **Graceful Fallback**: Enhanced template narratives when AI unavailable
- **Background Initialization**: Non-blocking AI startup

### AI Narrative Features (v0.0.2)
- **Structured Content Parsing**: Extract headers, lists, numbers, bold items
- **Content-Specific Templates**: Code, meetings, recipes, etc.
- **Extension Logic**: Ensures 600+ character minimum for fallback narratives
- **Fantasy Translation**: Technical concepts → magical lore

## Development Guide

### Setup & Installation

```bash
# Clone repository
git clone https://github.com/snedea/legend-of-obsidian-vault.git
cd legend-of-obsidian-vault

# Quick start (auto-installs dependencies)
./run.sh           # Mac/Linux
run.bat            # Windows

# Manual installation
pip install -r requirements.txt
python3 lov.py
```

### Manual Testing Checklist

- [ ] Character creation completes successfully
- [ ] Obsidian vault detection finds user vault
- [ ] Forest enemies show note-based names
- [ ] Quiz attacks generate contextual questions
- [ ] AI gracefully falls back to regex when unavailable
- [ ] Combat math matches LORD formulas
- [ ] Save/load preserves all character data
- [ ] LORD Secrets features work (Jennie codes, IGMs, bank robbery)

### Testing Individual Components

**Obsidian Vault Testing**
```bash
# Test vault detection
python3 demo.py

# Check specific vault path
python3 -c "from obsidian import vault; vault.set_vault_path('/path/to/vault'); print(len(vault.scan_notes()))"
```

**AI Integration Testing**
```bash
# Test AI availability
python3 -c "from brainbot import initialize_ai, is_ai_available; initialize_ai(); import time; time.sleep(3); print(is_ai_available())"

# Test question generation
python3 -c "from brainbot import sync_generate_quiz_question; q, a = sync_generate_quiz_question('Test Note', 'Machine learning is a method of data analysis.'); print(f'Q: {q}\\nA: {a}')"
```

### Debugging Tips

**Common Issues**:
1. **Combat narratives truncated?** → Check `screens/combat/combat.py:47` (`max_lines` parameter)
2. **Changes not taking effect?** → Verify working directory (not `/ai-red-dragon/`)
3. **AI not loading?** → Check `brainbot.py` threading initialization
4. **Import errors?** → Review delayed import pattern in screen modules

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for comprehensive debugging guide.

## Performance & Optimization

### Memory Management
- **Note Caching**: 5-minute TTL prevents excessive file I/O
- **AI Response Caching**: Prevents redundant model inference
- **Lazy Loading**: AI model loads in background thread

### File System Efficiency
- **Vault Scanning**: Skips .icloud placeholders and templates
- **Recursive Globbing**: Uses pathlib for cross-platform compatibility
- **Stat Caching**: Reduces filesystem calls for large vaults

### AI Optimization
- **Model Selection**: TinyLlama 1.1B balances capability vs resource usage
- **Context Limiting**: Truncates note content to 500-800 chars for prompts
- **Thread Safety**: Background initialization with daemon threads

### Performance Benchmarks

**Target Performance**:
- **Startup Time**: < 3 seconds (excluding AI initialization)
- **AI Initialization**: < 10 seconds first run, < 5 seconds subsequent
- **Vault Scanning**: < 2 seconds for 1000 notes
- **Combat Response**: < 100ms for standard attacks
- **Quiz Generation**: < 3 seconds with AI, < 100ms fallback

**Resource Usage**:
- **Memory**: 512MB base + 1.5GB for AI model
- **Storage**: 50MB game + 670MB AI model
- **CPU**: Single-threaded, occasional bursts for AI inference
- **Network**: Only for initial model download

## Known Technical Debt

### Code Quality Issues
1. **Global State**: `current_player` should be encapsulated
2. **Screen Coupling**: Some screens directly access game_db
3. **Error Handling**: Need comprehensive exception management
4. **Type Hints**: Incomplete type annotation coverage

### Performance Concerns
1. **Large Vaults**: 10,000+ notes may slow vault scanning
2. **AI Latency**: First quiz question takes 2-3 seconds
3. **Memory Usage**: TinyLlama model requires ~1.5GB RAM
4. **File Watching**: No live vault updates (requires restart)

### Implemented Features (v0.0.5)

**Combat & Gameplay**:
- ✅ Authentic LORD v4.00a combat formula
- ✅ 15-tier weapon/armor progression
- ✅ Turgon's Warrior Training (11 masters)
- ✅ Hall of Honours for Dragon Slayers
- ✅ Enhanced combat statistics tracking

**Shops & Economy**:
- ✅ Healer's Hut (full/partial healing)
- ✅ Ye Old Bank (deposit/withdrawal/interest)
- ✅ Abdul's Armor (progressive upgrades)
- ✅ Weapon shop system

**LORD Secrets (v0.0.4)**:
- ✅ Jennie Codes System (13 authentic codes)
- ✅ 8 IGM Locations (Cavern, Barak's House, Fairy Garden, etc.)
- ✅ Bank Robbery System (thief/fairy_lore required)
- ✅ Fairy Lore combat healing
- ✅ WereWolf curse system
- ✅ Gateway Portal adventures

**AI Features (v0.0.2)**:
- ✅ Rich combat narratives (1600+ chars)
- ✅ Content-aware enemy generation
- ✅ Enhanced template fallback system

See [ROADMAP.md](ROADMAP.md) for future enhancement plans.

## Contributing

### Code Standards
- **PEP 8**: Python style guide compliance
- **Type Hints**: Add annotations for new functions
- **Docstrings**: Document all public methods
- **LORD Authenticity**: Maintain original game feel

### Pull Request Process
1. **Feature Branch**: Create from main branch
2. **Testing**: Verify on multiple platforms if possible
3. **Documentation**: Update CLAUDE.md for architectural changes
4. **Compatibility**: Ensure LORD mechanics remain authentic

### Issue Reporting
- **Environment**: Include Python version, OS, terminal type
- **Reproduction**: Clear steps to reproduce issues
- **Expected Behavior**: Reference to original LORD if applicable
- **Actual Behavior**: Detailed description of current state

## Security Considerations

### AI Safety
- **Local Processing**: No data leaves user's machine
- **Prompt Injection**: Limited by note content only
- **Model Safety**: TinyLlama has built-in safety training

### File System Access
- **Sandboxed**: Only reads Obsidian vaults and saves directory
- **No Execution**: Pure data processing, no code evaluation
- **User Control**: Vault path explicitly set by user

### Data Privacy
- **Local Storage**: SQLite database in saves/ directory
- **No Telemetry**: No analytics or usage tracking
- **Open Source**: All code visible and auditable

## Credits & References

### Original Game
- **Legend of the Red Dragon (LORD)**: Created by Seth Able Robinson
- **Combat Formula Source**: [RT Soft LORD FAQ](https://www.rtsoft.com/pages/lordfaq.php) - Provided authentic LORD v4.00a combat math formula

### Technical Implementations
- **Authentic Combat Math**: `HIT_AMOUNT = (strength/2) + random(strength/2) - defence`
  - Source: RT Soft LORD FAQ
  - Monsters have no defense in LORD combat
  - Negative hit amounts result in misses

### Development Tools
- **Textual Framework**: Modern Python TUI framework
- **TinyLlama**: Local AI integration for narrative generation
- **SQLite**: Player persistence and game state management

---

This project serves as both a nostalgic gaming experience and a demonstration of how AI can enhance classic gameplay without compromising authenticity. The architecture balances modern Python practices with faithful recreation of 1990s BBS gaming culture.

For detailed version history, see [CHANGELOG.md](CHANGELOG.md).
For future enhancement plans, see [ROADMAP.md](ROADMAP.md).
For troubleshooting and debugging, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

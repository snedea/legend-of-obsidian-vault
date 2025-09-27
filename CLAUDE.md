# CLAUDE.md - Developer Documentation

## Project Overview

Legend of the Obsidian Vault (LOV) is an exact clone of the classic BBS game "Legend of the Red Dragon" (LORD) v4.00a, enhanced with Obsidian vault integration and AI-powered quiz combat. This project demonstrates how modern AI can breathe new life into retro gaming while maintaining authentic gameplay mechanics.

## Architecture & Design Philosophy

### Core Principles

1. **Authenticity First**: Maintain exact LORD mechanics, pricing, and feel
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

## File Architecture

```
legend-of-obsidian-vault/
├── lov.py              # Main Textual application
├── game_data.py        # Core game mechanics and data structures
├── obsidian.py         # Vault integration and note processing
├── brainbot.py         # TinyLlama AI integration
├── saves/
│   └── players.db      # SQLite player data
├── demo_vault/         # Example notes for testing
├── requirements.txt    # Python dependencies
├── README.md          # User documentation
├── CLAUDE.md          # This file - developer docs
└── TODO.md            # Feature roadmap
```

## Core Components

### 1. Game Engine (lov.py)

**Main Application Class**
```python
class LordApp(App):
    """Main LORD application with authentic BBS styling"""
```

**Screen Management**
- `WelcomeScreen`: Character selection and vault setup
- `TownSquareScreen`: Central hub with 18 authentic LORD options
- `ForestScreen`: Combat initiation and daily limits
- `CombatScreen`: Real-time battle system with AI integration
- `QuizScreen`: Knowledge-based combat interface

**Key Design Patterns**
- **Screen Stack**: Textual's navigation system for authentic BBS feel
- **Event-Driven**: Keyboard shortcuts match original LORD
- **State Management**: Global player state with screen isolation

### 2. Game Mechanics (game_data.py)

**Character System**
```python
@dataclass
class Character:
    name: str = ""
    level: int = 1
    hitpoints: int = 10
    max_hitpoints: int = 10
    # ... exact LORD stat progression
```

**Weapon/Armor Progression**
- **15 Weapon Tiers**: Stick (200g) → Death Sword (400M gold)
- **15 Armor Tiers**: Coat (200g) → Shimmering Armor (400M gold)
- **Exact LORD Pricing**: Maintains authentic economic progression

**Combat Formulas**
```python
def calculate_damage(self, attacker, defender):
    # Exact LORD damage calculation
    base_damage = random.randint(1, attacker.attack_power)
    defense_reduction = defender.defense_power // 2
    return max(1, base_damage - defense_reduction)
```

### 3. Obsidian Integration (obsidian.py)

**Vault Detection Logic**
```python
class ObsidianVault:
    def find_vault(self) -> Optional[Path]:
        # Searches 15+ common locations including:
        # - Standard Obsidian folders
        # - iCloud sync locations
        # - Custom user directories
        # - Fallback to any folder with 3+ .md files
```

**Note Processing Pipeline**
1. **Scan**: Recursive .md file discovery
2. **Parse**: Extract title, content, tags, metadata
3. **Classify**: Age-based difficulty assignment
4. **Cache**: 5-minute memory cache for performance

**Enemy Generation**
```python
def get_enemy_for_level(self, level: int, notes: List[ObsidianNote] = None) -> Enemy:
    # Selects random note regardless of difficulty
    # Scales stats based on note age vs player level
    # Generates creative enemy names: "Mosquito of Machine Learning"
```

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
- **Threading**: AI loads without blocking game startup
- **Graceful Degradation**: Falls back to regex if AI fails
- **Model Sharing**: Uses existing BrainBot model cache

**Quiz Generation Pipeline**
1. **Prompt Engineering**: Structured prompts for consistent output
2. **Response Parsing**: Regex extraction of Q/A/Type
3. **Validation**: Answer matching with semantic understanding
4. **Caching**: Prevents regeneration of identical content

## Combat System Deep Dive

### Traditional Combat Flow
```
Player Turn → Enemy Turn → Damage Calculation → Victory/Defeat Check
```

### Knowledge Combat Enhancement
```
Quiz Question → User Input → AI Validation → Critical Hit (2x) or Miss → Continue Combat
```

**Quiz Question Generation**
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
```python
def validate_answer(self, user_answer: str, correct_answer: str, ai_question: bool) -> bool:
    # Exact match check
    if user_lower == correct_lower: return True

    # AI semantic matching (50% word overlap)
    if ai_question and word_overlap_ratio >= 0.5: return True

    # Fallback keyword matching
    return any(word in user_answer for word in correct_answer.split())
```

## Performance Optimizations

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
- **Context Limiting**: Truncates note content to 500 chars for prompts
- **Thread Safety**: Background initialization with daemon threads

## Testing & Development

### Manual Testing Checklist
- [ ] Character creation completes successfully
- [ ] Obsidian vault detection finds user vault
- [ ] Forest enemies show note-based names
- [ ] Quiz attacks generate contextual questions
- [ ] AI gracefully falls back to regex when unavailable
- [ ] Combat math matches LORD formulas
- [ ] Save/load preserves all character data

### Development Environment Setup
```bash
# Clone repository
git clone https://github.com/snedea/legend-of-obsidian-vault.git
cd legend-of-obsidian-vault

# Install dependencies
pip install -r requirements.txt

# Run in development mode
python3 lov.py

# Test individual components
python3 -c "from obsidian import vault; print(vault.get_vault_path())"
python3 -c "from brainbot import sync_generate_quiz_question; print(sync_generate_quiz_question('Test', 'Content'))"
```

### Debugging Tools

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

### Missing LORD Features (See TODO.md)
1. **Inn System**: Violet, Seth, bar room interactions
2. **Shop Mechanics**: Actual purchase transactions
3. **Banking**: Interest calculations and gold management
4. **PvP Combat**: Player vs player battle system
5. **Daily Events**: News, announcements, random encounters

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

## Future Architecture Plans

### v0.1.0 - Inn System
- **Violet Interaction**: Charm-based romance mechanics
- **Seth's Songs**: Daily musical performances with stat bonuses
- **Bar Room**: Social features and random events

### v0.2.0 - Commerce System
- **Shop Transactions**: Complete weapon/armor purchasing
- **Inventory Management**: Equipment upgrades and sales
- **Economic Balance**: LORD-accurate pricing and progression

### v0.3.0 - Banking & Daily Systems
- **Interest Calculations**: 10% daily compound interest
- **Time Management**: Daily resets and limit tracking
- **News System**: Player announcements and game events

### v0.4.0 - PvP Combat
- **Player Rankings**: Leaderboards and statistics
- **Combat Mechanics**: Player vs player battle system
- **Death Penalties**: Authentic LORD consequences

### v1.0.0 - Feature Complete
- **Random Events**: Olivia's head, old man encounters
- **Marriage System**: Conjugality list and weddings
- **Dragon Battle**: Level 12+ endgame content
- **Achievement System**: Progress tracking and rewards

## Contributing Guidelines

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

## Performance Benchmarks

### Target Performance
- **Startup Time**: < 3 seconds (excluding AI initialization)
- **AI Initialization**: < 10 seconds first run, < 5 seconds subsequent
- **Vault Scanning**: < 2 seconds for 1000 notes
- **Combat Response**: < 100ms for standard attacks
- **Quiz Generation**: < 3 seconds with AI, < 100ms fallback

### Resource Usage
- **Memory**: 512MB base + 1.5GB for AI model
- **Storage**: 50MB game + 670MB AI model
- **CPU**: Single-threaded, occasional bursts for AI inference
- **Network**: Only for initial model download

## Legacy Compatibility

### LORD v4.00a Parity
- **Combat Formulas**: Exact damage calculations
- **Economic System**: Identical pricing and progression
- **Character Classes**: Same abilities and skill systems
- **Daily Limits**: 15 forest fights, 3 PvP fights
- **Level Progression**: Experience and stat growth

### BBS Authenticity
- **Visual Design**: 16-color ANSI, 80x25 layout compatibility
- **Navigation**: Keyboard shortcuts match original
- **Text Content**: Original LORD dialog where applicable
- **Game Flow**: Screen transitions and menu structure

This project serves as both a nostalgic gaming experience and a demonstration of how AI can enhance classic gameplay without compromising authenticity. The architecture balances modern Python practices with faithful recreation of 1990s BBS gaming culture.
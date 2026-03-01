# CHANGELOG.md - Version History

All notable changes to Legend of the Obsidian Vault are documented in this file.

## [v0.0.5] - 2025-10-03 (Current)

### Added
- Authentic LORD v4.00a combat formula implementation
  - Source: [RT Soft LORD FAQ](https://www.rtsoft.com/pages/lordfaq.php)
  - `HIT_AMOUNT = (strength/2) + random(strength/2) - defence`
  - Monsters have NO defense in LORD combat
  - Negative hit amounts result in misses

### Changed
- Combat calculation accuracy improved to match original LORD exactly
- Documentation updated with combat formula sources and references

## [v0.0.4] - 2025-09-30

### Added - Complete LORD Secrets Implementation

The most significant update in the project's history - a comprehensive implementation of all LORD Secrets features.

#### **Jennie Codes System**
- Hidden command buffer tracking in Forest screen
- 13 authentic LORD secret codes implementation:
  - `JENNIE PRETTY` - High spirits mode (increased luck)
  - `JENNIE UGLY` - Low spirits mode (decreased luck)
  - `JENNIE DUNG` - Frog transformation state
  - Plus 10 additional authentic codes
- Complex state management for transformations
- Spirit level checking and validation

#### **Complete IGM (In-Game Module) System**
- **LORD Cavern** (`screens/igm/cavern.py`):
  - Daily exploration system (3 searches per day)
  - Riddler encounters with 5 unique riddles
  - Random treasure hunting with loot tables
  - Risk/reward mechanics with stat boosts and penalties

- **Barak's House** (`screens/igm/barak.py`):
  - Scholar sanctuary with book reading system
  - Combat study for random stat improvements
  - Basement gambling den with dice games
  - Aggression tracking based on player behavior

- **Fairy Garden** (`screens/igm/fairy_garden.py`):
  - Learnable Fairy Lore system (1000 gold investment)
  - Combat healing integration (25-40% max HP)
  - Practice and meditation systems
  - Advanced training options

- **Xenon's Storage Facility** (`screens/igm/xenon_storage.py`):
  - Resource management with daily storage fees
  - Horse purchasing and naming system
  - Dark trading mechanics (children for resources)
  - Storage limits and fee calculations

- **WereWolf Den** (`screens/igm/werewolf_den.py`):
  - Werewolf curse learning (5000 gold)
  - PvP combat enhancement framework
  - Stat stealing mechanics from opponents
  - Risk management (20% chance of control loss)

- **Gateway Portal** (`screens/igm/gateway_portal.py`):
  - Dimensional travel to adventure realms
  - Zycho Zircus: Carnival games, freakshow
  - Death's Mansion: High-risk trials
  - Random portals with unpredictable outcomes

#### **Advanced Criminal Mechanics**
- **Bank Robbery System**:
  - Hidden (R)ob command for thieves with fairy_lore
  - Skill-based success calculation
  - Base 30% + thieving points (5% each) + level (2% each)
  - Success capped at 80%
  - Steal 10-30% of total bank deposits
  - Heavy penalties for failure

#### **Enhanced Combat System**
- Fairy Lore healing integrated into combat
- Dynamic command display based on player abilities
- (H)eal command for fairy_lore users
- 25-40% max HP restoration with rich narrative

#### **Database Architecture Enhancements**
- Extended Character model with 12 new fields:
  - `fairy_lore: bool` - Combat healing ability
  - `spirit_level: str` - Jennie codes state
  - `cavern_searches_today: int` - Daily limit tracking
  - `children: int` - Strategic resource
  - `horse_name: str` - Storage system
  - `werewolf_uses_today: int` - Daily limits
  - `bank_robberies_today: int` - Criminal tracking
  - `successful_robberies: int` - Statistics
  - `stored_gold: int` - Xenon's facility
  - `stored_gems: int` - Xenon's facility
  - `is_werewolf: bool` - Curse status
  - `werewolf_transformations: int` - Usage tracking

- Automatic migration system for backward compatibility
- Zero data loss during schema updates

#### **Complete UI/UX System**
- 8 new CSS style sets for each IGM location
- Unified "Other Places" navigation menu
- Authentic BBS VGA/ANSI color styling
- Full keyboard shortcut support

### Technical Achievements
- Modular IGM framework with `screens/igm/` directory
- 8 new interactive screen modules
- Daily limit tracking across all systems
- Complex state persistence for transformations
- Event-driven hidden command parsing
- 36% code reduction in main file through modularization

## [v0.0.3] - 2025-09-28

### Added - Major UI/UX and Architecture Improvements

#### **Modular Architecture Refactoring**
- Created `screens/` directory structure:
  - `screens/combat/` - ForestScreen, CombatScreen, QuizScreen
  - `screens/town/` - TownSquare, Inn, Bank, Weapons, Armor, Healer, etc.
  - `screens/character/` - Creation, Selection, Stats screens
- **36% Code Reduction**: `lov.py` reduced from 2,197 → 1,400 lines
- Implemented delayed import pattern for circular dependency resolution
- Each screen in focused, maintainable module

#### **Combat UI Complete Redesign**
- Final Fantasy-style combat interface
- Clean enemy/player status sections
- Unicode HP bars: `█░░░░░░░░░ 30%` with percentages
- Real-time HP and stat updates during combat
- Color-coded stats: red for enemy, green for player
- Emoji-enhanced combat messages (⚔️🔥⭐❌)

#### **Functional Shop Implementation**

**Healer's Hut**:
- Full heal with level-based pricing (5-500 gold)
- Partial heal at 1 gold per HP
- Interactive input with validation

**Ye Old Bank**:
- Deposit/withdrawal system
- 10% daily compound interest
- "Deposit All" and "Withdraw All" shortcuts
- Real-time gold display updates

**Abdul's Armor**:
- 15-tier progressive armor upgrades
- Coat (200g) → Shimmering Armor (400M gold)
- Next-tier-only purchasing (authentic LORD)
- Defense improvement calculations
- Authentic LORD pricing

#### **Enhanced Visual Design**

**Forest Screen**:
- Mystical forest header with 5 detailed tree canopies
- Color-coded: green trees, brown trunks, white mist
- "✦ THE MYSTICAL FOREST OF KNOWLEDGE ✦" themed title

**Armor Shop**:
- Ornate shield and crossed swords ASCII art
- Metallic color scheme: silver shield, gold swords, cyan decorations
- "⚔️⚜️ ABDUL'S LEGENDARY ARMORY ⚜️⚔️" branding

### Fixed
- Forest healer navigation ("not yet available" → actual healer screen)
- TownSquare import crashes (missing screen imports)
- Combat header misalignment
- HP bar visibility and contrast

## [v0.1.0] - 2025-09-29

### Added - Turgon's Warrior Training & Hall of Honours

#### **Turgon's Warrior Training System**
- Complete LORD master progression:
  - 11 authentic masters: Halder → Turgon
  - Exact dialogue from original LORD
- Master challenge flow:
  - Greeting → Challenge → Combat → Level Up
- Authentic stat progression:
  - Exact LORD HP/STR/DEF gains per level
- Weapon rewards:
  - Earn master weapons (Short Sword → Able's Sword)
- Full screen system accessible via (T) in Town Square

#### **Hall of Honours for Dragon Slayers**
- Dragon kill tracking with defeat dates
- Class-specific victory messages
- Rankings display: Top 20 dragon slayers
- Kill count statistics
- Character reset system (authentic LORD post-dragon mechanics)
- Persistent statistics across sessions

#### **Database Migration System**
- Automatic schema updates
- Detects and adds missing columns
- Zero data loss preservation
- Default value handling
- 37-field CHARACTER class support

#### **Enhanced Combat Statistics**
- Total kill counter (all enemy defeats)
- Master fight integration (separate tracking)
- Hall entry dates (first dragon victory timestamp)
- Win streak tracking (multiple dragon kills)

## [v0.0.2] - 2025-09-27

### Added - AI-Powered Dungeon Master Narratives

#### **Enhanced AI Narrative Generation**
- Simplified AI prompts for focused narrative generation
- Increased context from 200 → 800+ characters
- Structured content parsing:
  - Markdown headers (# Title)
  - List items (-, *, +, 1.)
  - Numbers and bold items
- Content-aware generation incorporating note details
- Rich fallback narratives when AI parsing fails

#### **Template Enhancement System**
- Content-specific templates:
  - Code/technical notes
  - Meeting notes
  - Recipe/cooking notes
  - General knowledge
- Extension logic ensures 600+ character minimum
- Atmospheric details from note content

### Results
- **Before**: "You discover the Sanctum of Eternal Knowledge..." (generic)
- **After**: "You enter the Algorithm Archive where 27 mystical patterns swirl... The ancient text declares 'Machine learning automates model building' as glowing runes..." (1600+ characters)

### Performance
- AI generates 1600+ character immersive descriptions
- Incorporates specific numbers, concepts, text from notes
- 800ms generation time for rich fantasy encounters
- Graceful fallback with enhanced templates

### Added - Complete Setup Automation

#### **Auto-Setup Infrastructure**
- `setup.py`: Auto-installs dependencies, checks Python version, creates directories
- `run.sh`: Mac/Linux launcher with first-time setup detection
- `run.bat`: Windows launcher with same functionality

#### **Features**
- One-click launch (`./run.sh` or `run.bat`)
- Dependency detection (auto-installs only when needed)
- Clear error messages and fallback options
- Cross-platform compatibility

### Fixed - Input System Issues

#### **StartScreen Input Fix**
- Added `can_focus = True` for keyboard input
- Added `on_mount()` with `self.focus()` for auto-focus
- Clickable button fallbacks for all menu options
- Enhanced error handling with notifications

#### **PlayerSelectScreen Complete Rewrite**
- Full input support (keyboard + mouse)
- Auto-focus on mount
- User notifications for readiness
- Number key handling (1-5 for character selection)
- Q key for exit

#### **CombatScreen Interface Completion**
- Added missing combat button handlers
- Fixed NoMatches error for #combat_status
- Added _update_combat_display() synchronization
- Implemented quiz attack AI integration

#### **AI Initialization Fix**
- **Problem**: Incorrect async/await causing crashes
- **Solution**: Proper threading for background init
```python
# Before: asyncio.create_task() outside event loop
# After: threading.Thread(target=initialize_ai, daemon=True)
```

### Improved - User Experience

**Auto-Setup Benefits**:
- Zero configuration required
- Professional first-run experience
- Better error messages
- Self-contained installation

**Input Reliability**:
- Multiple input methods (keyboard + mouse)
- Visual feedback for all actions
- Auto-focus management
- Graceful degradation with fallbacks

**AI Integration**:
- Non-blocking startup
- Clear AI connection status
- Full functionality without AI dependencies

### Technical Debt Reduction

**Code Quality**:
- Standardized focus management
- Consistent event handling patterns
- Proper async/threading separation
- Enhanced error handling

**Architecture**:
- Separated setup from game logic
- Cross-platform improvements
- Better dependency management
- Streamlined development workflow

## [v0.0.1] - 2025-09-25

### Added - Initial Release

#### **Core Game Engine**
- Main Textual application framework
- Screen-based navigation system
- Authentic BBS 16-color ANSI/VGA styling

#### **Character System**
- Character creation with class selection
- Death Knight, Mystical, Thief classes
- Basic stat progression (HP, STR, DEF)
- Experience and leveling system

#### **Combat System**
- Traditional turn-based combat
- Enemy generation from Obsidian notes
- Basic damage calculations
- Victory/defeat mechanics

#### **Obsidian Integration**
- Vault detection (15+ common locations)
- Recursive .md file scanning
- Note content parsing
- Age-based difficulty scaling

#### **AI Integration**
- TinyLlama 1.1B local model
- Basic quiz question generation
- Answer validation (exact + keyword matching)
- Response caching (5-minute TTL)

#### **Data Persistence**
- SQLite database for player saves
- Character save/load system
- Game state preservation

#### **Basic Screens**
- Welcome/character selection
- Town Square hub
- Forest combat area
- Basic combat interface

---

## Version Numbering

Format: `MAJOR.MINOR.PATCH`

- **MAJOR**: Significant feature additions (v1.0.0 = full LORD parity)
- **MINOR**: New features, systems, or substantial improvements
- **PATCH**: Bug fixes, optimizations, minor enhancements

## Links

- **Current Development**: See [ROADMAP.md](ROADMAP.md)
- **Architecture Details**: See [CLAUDE.md](CLAUDE.md)
- **Troubleshooting**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Repository**: [github.com/snedea/legend-of-obsidian-vault](https://github.com/snedea/legend-of-obsidian-vault)

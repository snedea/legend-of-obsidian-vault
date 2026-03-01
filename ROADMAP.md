# ROADMAP.md - Future Development Plans

## Current Status: v0.0.5

**Completed Features**:
- ✅ Authentic LORD v4.00a combat formula
- ✅ Complete LORD Secrets implementation (IGMs, Jennie codes, etc.)
- ✅ AI-powered combat narratives (1600+ character rich descriptions)
- ✅ Obsidian vault integration with content-aware enemy generation
- ✅ Turgon's Warrior Training & Hall of Honours
- ✅ Complete shop/bank/healer systems

## v0.1.0 - Enhanced Enemy Intelligence (Q1 2026)

### Dynamic Enemy Names & Personalities
**Priority**: HIGH

Transform generic encounters into memorable fantasy experiences.

**Features**:
- **AI-Generated Names**: "Shadow Weaver, Keeper of Forgotten Themes" instead of "Mosquito of Themes Directory"
- **Personality Traits**: Enemies have consistent behavior patterns based on note content
- **Memory System**: Recurring enemies remember previous encounters
- **Emotional Tone**: Derive personality from note writing style (formal, casual, technical)

**Technical Approach**:
```python
# Enhanced enemy generation in brainbot.py
def generate_enemy_personality(note: ObsidianNote) -> EnemyPersonality:
    # Content analysis for personality traits
    # Technical notes → Logical, precise enemies
    # Personal journals → Emotional, unpredictable enemies
    # Project docs → Strategic, methodical enemies
```

**Example Output**:
- **Before**: "Mosquito of My Themes Directory"
- **After**: "Thematic Wraith - A cunning spirit that feeds on forgotten ideas, speaking in riddles about color theory and design principles"

### Knowledge-to-Fantasy Translation Layer
**Priority**: HIGH

Convert any note content into magical fantasy concepts.

**Translations**:
- Code snippets → Arcane formulas and mystical runes
- Bullet points → Ancient scrolls with sacred markings
- Timestamps → Prophetic dates and celestial alignments
- File paths → Mystical locations and dimensional gates
- Functions → Ritual spells
- Variables → Mystical essences
- Databases → Ancient tomes
- APIs → Dimensional gateways
- Bugs → Curses
- Features → Enchantments

**Implementation**:
```python
FANTASY_TRANSLATIONS = {
    "function": "ritual spell",
    "variable": "mystical essence",
    "database": "ancient tome",
    "API": "dimensional gateway",
    "bug": "curse",
    "feature": "enchantment",
    "commit": "chronicles entry"
}
```

## v0.2.0 - Contextual Combat Narration (Q2 2026)

### Pre-Battle & Mid-Combat Storytelling
**Priority**: MEDIUM

Transform combat from stat exchanges to immersive storytelling.

**Features**:
- **Pre-Battle Narrative**: Why this enemy guards this specific knowledge
- **Environmental Details**: Based on note folder structure
- **Enemy Dialogue**: Lore-appropriate taunts and threats
- **Mid-Combat Flavor**: Reference note concepts during attacks
- **Spell-Like Effects**: Technical concepts become magical attacks

**Example Combat Flow**:
```
Pre-Battle:
"You enter the Crimson Archives, where forgotten bug reports whisper
in the shadows. A Documentation Demon materializes, its form shifting
between incomplete specifications..."

Player Attack:
"You channel your understanding of clean code principles, striking
at the demon's poorly-structured defenses!"

Enemy Attack:
"The Documentation Demon hurls a bolt of confused requirements!
'Undefined behavior shall be your downfall!' it shrieks."

Critical Hit:
"Your deep understanding of the codebase pierces through its
defensive obfuscation! The demon recoils as clarity burns its essence."
```

### Riddle-Based Combat Enhancement
**Priority**: MEDIUM

Frame quiz questions as enemy riddles and magical challenges.

**Features**:
- Present questions as enemy riddles instead of plain quizzes
- Correct answers unlock enemy weaknesses (visual feedback)
- Lore-based explanations for all answers
- Wrong answers trigger enemy taunts related to the subject

## v0.3.0 - Note-Based World Building (Q3 2026)

### Dynamic Forest Regions
**Priority**: LOW

Use vault structure to create living world regions.

**Features**:
- **Folder Mapping**: Each note folder becomes a unique forest region
- **Region Themes**: "/Projects/WebDev/" → "The Silicon Swamplands"
- **Unique Enemies**: Region-specific enemy types and difficulty
- **Visual Distinctions**: ASCII art variations for each region
- **Region Progression**: Unlock regions as player levels up

**Example Regions**:
```
/Projects/WebDev/      → "The Silicon Swamplands"
/Personal/Journal/     → "Whispering Memory Meadows"
/Work/Meetings/        → "Council Chambers of Confusion"
/Learning/Tutorials/   → "Academy of Forgotten Lessons"
/Ideas/Concepts/       → "Ethereal Thoughtscape"
```

**Implementation**:
```python
# Map folder paths to fantasy regions
REGION_MAP = {
    "projects": {"name": "Silicon Swamplands", "theme": "tech", "difficulty": 1.2},
    "personal": {"name": "Memory Meadows", "theme": "emotional", "difficulty": 0.8},
    "work": {"name": "Corporate Catacombs", "theme": "bureaucratic", "difficulty": 1.0}
}
```

### Living Encyclopedia System
**Priority**: LOW

Create interconnected lore from vault relationships.

**Features**:
- **Enemy Relationships**: Related notes create enemy factions
- **Quest Chains**: Linked notes generate multi-stage quests
- **Tag-Based Abilities**: Note tags determine enemy special abilities
- **Cross-Reference Rewards**: Bonus XP for defeating related enemies

## v0.4.0 - Adaptive Learning System (Q4 2026)

### Knowledge Pattern Tracking
**Priority**: MEDIUM

Track player knowledge and adapt difficulty.

**Features**:
- **Weak Area Detection**: Identify topics player struggles with
- **Recurring Nemeses**: Stronger enemies appear for weak knowledge areas
- **Personalized Dialogue**: Enemies reference player's past failures
- **Adaptive Difficulty**: Quiz complexity scales with player performance
- **Study Recommendations**: Suggest notes to review based on combat performance

**Example**:
```
Player repeatedly fails Python quiz questions
→ "The Python Serpent" becomes a recurring mini-boss
→ Enemy taunts: "Still don't understand list comprehensions, do you?"
→ Defeating it requires mastering Python concepts
→ Game suggests reviewing Python notes after combat
```

### Spaced Repetition Integration
**Priority**: LOW

Incorporate proven learning techniques into combat.

**Features**:
- Quiz questions follow spaced repetition algorithm
- Recently answered questions appear less frequently
- Difficult concepts resurface at optimal intervals
- Progress tracking across game sessions
- Export quiz performance data for external review

## v0.5.0 - Multiplayer & Social Features (2027)

### Asynchronous PvP Combat
**Priority**: MEDIUM

Add player vs player battles (authentic LORD style).

**Features**:
- **Daily PvP Attempts**: 3 fights per day limit (authentic LORD)
- **Knowledge Duels**: Quiz battles between players
- **Vault Comparison**: Players fight enemies from opponent's vaults
- **Rankings & Leaderboards**: Top knowledge champions
- **Death Penalties**: Lose gold/experience when defeated (authentic LORD)

### Shared Vault Mode
**Priority**: LOW

Collaborative learning through shared knowledge bases.

**Features**:
- Multiple players explore same Obsidian vault
- Cooperative enemy battles
- Shared quest progression
- Team-based quiz challenges
- Vault contribution tracking

## v1.0.0 - Feature Complete LORD Recreation (2027)

### Missing Authentic LORD Features

**Random Events**:
- Old man in the forest encounters
- Olivia's head discovery
- Mysterious beggar interactions
- Hidden treasure locations

**Marriage System**:
- Conjugality list
- Player weddings
- Romance stat bonuses
- Spouse interactions

**Dragon Battle**:
- Level 12+ endgame content
- Epic multi-phase boss fight
- Special dragon-slaying weapons
- Victory celebrations and rewards

**Daily Events**:
- Player news announcements
- Daily server messages
- Random world events
- Festival days and special occasions

### Complete LORD Parity Checklist

- [ ] All random forest events
- [ ] Complete marriage/romance system
- [ ] Red Dragon endgame boss
- [ ] Inter-player messaging
- [ ] Daily news system
- [ ] Special event days
- [ ] Complete skill system (charm, thieving points)
- [ ] All authentic LORD dialogue
- [ ] Original sound effects (optional)
- [ ] Authentic BBS door game feel

## Research & Experimental Features

### Advanced AI Integration
**Status**: Research Phase

**Possibilities**:
- Larger language models for more sophisticated narratives
- Multi-modal AI (image generation for enemies)
- Voice synthesis for combat narration
- Real-time AI dungeon master mode

### Alternative Knowledge Sources
**Status**: Concept Phase

**Integration Ideas**:
- Notion database integration
- Roam Research support
- Markdown file systems (non-Obsidian)
- PDF library integration
- Browser bookmark integration

### Educational Platform Features
**Status**: Concept Phase

**Potential**:
- Teacher dashboard for student progress
- Curriculum-based enemy generation
- Exam preparation mode
- Subject-specific difficulty scaling
- Learning analytics and insights

## Performance & Quality Goals

### Performance Targets (All Versions)
- Startup time < 2 seconds
- Combat response < 50ms
- Vault scanning < 1 second (1000 notes)
- AI generation < 2 seconds
- Memory usage < 1GB (excluding AI model)

### Code Quality Goals
- 100% type hint coverage
- 90%+ test coverage
- Zero circular dependencies
- Comprehensive error handling
- Complete API documentation

### User Experience Goals
- < 5 minute learning curve
- Intuitive navigation (no manual needed)
- Graceful degradation (AI optional)
- Cross-platform consistency
- Accessibility features (screen readers, colorblind modes)

## Community Contributions Welcome

### High-Impact Contribution Areas
1. **Platform Support**: Windows Terminal optimization, Linux testing
2. **Vault Integrations**: Other note-taking apps
3. **AI Models**: Alternative local models (Llama 2, Mistral)
4. **LORD Authenticity**: Missing features from original game
5. **Accessibility**: Screen reader support, keyboard navigation

### Documentation Needs
1. Video tutorials for setup
2. Contributor's guide
3. Architecture deep-dives
4. Modding/extension system docs
5. Localization guide (i18n support)

## Timeline Summary

| Version | Target | Focus |
|---------|--------|-------|
| v0.1.0 | Q1 2026 | Enhanced enemy intelligence & personality |
| v0.2.0 | Q2 2026 | Contextual combat narration |
| v0.3.0 | Q3 2026 | Note-based world building |
| v0.4.0 | Q4 2026 | Adaptive learning system |
| v0.5.0 | 2027 | Multiplayer & social features |
| v1.0.0 | 2027 | Feature-complete LORD recreation |

---

For current implementation details, see [CLAUDE.md](CLAUDE.md).
For troubleshooting, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).
For version history, see [CHANGELOG.md](CHANGELOG.md).

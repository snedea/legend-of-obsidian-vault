# TODO - Development Roadmap

## 🚧 v0.0.1 Status: Pre-Alpha Release

This document tracks missing features and known issues in Legend of the Obsidian Vault.

### ✅ **Working Features (v0.0.1)**
- Character creation (all 3 classes)
- Forest combat with note-based enemies
- TinyLlama AI quiz generation
- Obsidian vault auto-detection
- Basic town square navigation
- SQLite save system
- Authentic BBS-style interface

---

## 🎯 **Priority Features for v0.1.0**

### Inn System (High Priority)
**Current State**: Basic navigation only, no interactions

**Required Implementation**:
- [ ] **Violet Flirtation System**
  - Charm-based romance mechanics
  - Daily interaction limits (1 per day)
  - Charm stat influences success rate
  - Romantic progression tracking
  - Authentic LORD dialog responses

- [ ] **Seth Abel's Songs**
  - Daily musical performances
  - Different songs with various effects
  - Stat bonuses (hitpoints, charm, etc.)
  - Experience point rewards
  - Song rotation system

- [ ] **Bar Room Interactions**
  - Player messaging system
  - Random NPC encounters
  - Drinking mechanics (optional stat effects)
  - Social gathering space
  - Gossip and rumors system

**Files to Modify**: `lov.py` (InnScreen class), `game_data.py` (add romance/music systems)

---

## 🛡️ **Priority Features for v0.2.0**

### Shop Functionality (Critical)
**Current State**: Display only, no purchasing mechanics

**King Arthur's Weapons**:
- [ ] Purchase transaction system
- [ ] Gold deduction and validation
- [ ] Equipment upgrade mechanics
- [ ] Inventory management
- [ ] Sell-back system (partial value)
- [ ] Level requirements enforcement

**Abdul's Armour**:
- [ ] Same purchasing mechanics as weapons
- [ ] Defense power calculations
- [ ] Equipment comparison display
- [ ] Upgrade recommendations

**Required Implementation**:
```python
def purchase_item(self, item_type: str, item_index: int) -> bool:
    # Validate gold, level requirements
    # Update player equipment
    # Deduct cost from player gold
    # Save changes to database
```

**Files to Modify**: `lov.py` (WeaponsScreen, ArmorScreen), `game_data.py` (purchase methods)

---

## 💰 **Priority Features for v0.3.0**

### Banking System
**Current State**: Navigation only

**Required Features**:
- [ ] **Gold Deposits**
  - Transfer gold from hand to bank
  - Security validation
  - Transaction logging

- [ ] **Gold Withdrawals**
  - Transfer gold from bank to hand
  - Daily withdrawal limits
  - Account balance tracking

- [ ] **Daily Interest**
  - 10% compound interest (LORD standard)
  - Automatic calculation on daily reset
  - Interest cap at reasonable limits
  - Historical tracking

- [ ] **Account Management**
  - Balance display
  - Transaction history
  - Interest earned reporting

**Implementation Notes**:
```python
def calculate_daily_interest(self, current_balance: int) -> int:
    # 10% daily interest, cap at reasonable amount
    interest = int(current_balance * 0.1)
    return min(interest, MAX_DAILY_INTEREST)
```

---

## ⚔️ **Priority Features for v0.4.0**

### Player vs Player Combat
**Current State**: Menu option exists, no implementation

**Core PvP System**:
- [ ] Player discovery and targeting
- [ ] Combat mechanics (same as monster combat)
- [ ] Victory/defeat consequences
- [ ] Gold and experience rewards
- [ ] Death penalties and resurrection

**Player Rankings**:
- [ ] Leaderboard system
- [ ] Player statistics tracking
- [ ] Combat history
- [ ] Win/loss ratios
- [ ] Reputation system

**Daily PvP Limits**:
- [ ] 3 attacks per day (LORD standard)
- [ ] Cooldown timers
- [ ] Reset mechanics

---

## 📰 **Priority Features for v0.5.0**

### Daily News & Events System
**Current State**: Menu exists but empty

**Features Needed**:
- [ ] **Daily News Display**
  - Player announcements
  - Game event notifications
  - Death reports
  - Marriage announcements

- [ ] **Player Announcements**
  - Public message system
  - Character limits
  - Moderation tools

- [ ] **Random Events** (LORD Authentic)
  - Olivia's Head encounters
  - Old man with stick
  - Fairy blessings
  - Dragon sightings
  - Treasure discoveries

---

## 🎲 **Priority Features for v0.6.0**

### Marriage & Social Systems
**Current State**: Conjugality list navigation only

**Marriage System**:
- [ ] Player courtship mechanics
- [ ] Wedding ceremonies
- [ ] Conjugality list management
- [ ] Relationship status tracking
- [ ] Social benefits/bonuses

**Other Places Expansion**:
- [ ] **Turgon's Training**
  - Level-up ceremonies
  - Stat training options
  - Special abilities unlock

- [ ] **Dragon's Lair** (Endgame)
  - Level 12+ access
  - Red Dragon boss battle
  - Ultimate victory condition
  - Hall of fame

---

## 🐛 **Known Issues & Bug Fixes**

### Critical Bugs
- [ ] **Character Creation**: Some edge cases in name validation
- [ ] **Combat Screen**: Widget refresh issues during rapid combat
- [ ] **Vault Scanning**: Very large vaults (10k+ notes) cause lag
- [ ] **AI Initialization**: Occasional timeout on slower systems

### Minor Issues
- [ ] **Color Compatibility**: Some terminals don't display VGA colors correctly
- [ ] **Window Resizing**: Interface doesn't adapt to terminal size changes
- [ ] **Keyboard Navigation**: Some screens missing escape key handling
- [ ] **Error Messages**: Need more user-friendly error reporting

### Performance Improvements
- [ ] **Note Caching**: Implement smarter cache invalidation
- [ ] **AI Response Time**: Optimize prompt engineering for faster generation
- [ ] **Database Queries**: Add indexes for player lookups
- [ ] **Memory Usage**: Reduce footprint for large vault scanning

---

## 🔮 **Future Enhancements (v1.0+)**

### Advanced AI Features
- [ ] **Dynamic Difficulty**: AI adjusts question complexity based on player performance
- [ ] **Learning System**: Tracks which notes player struggles with
- [ ] **Custom Prompts**: Allow users to customize AI behavior
- [ ] **Multi-Language**: Support for non-English notes

### Extended Obsidian Integration
- [ ] **Live Vault Updates**: Real-time note change detection
- [ ] **Tag-Based Filtering**: Use Obsidian tags for enemy categories
- [ ] **Graph Integration**: Visual representation of note connections
- [ ] **Plugin API**: Allow custom note processing

### Multiplayer Features
- [ ] **Local Network**: Multi-player on same network
- [ ] **BBS Simulation**: Full multi-user bulletin board system
- [ ] **Chat System**: Real-time communication
- [ ] **Guilds/Clans**: Group systems and competitions

### Accessibility
- [ ] **Screen Reader**: Full accessibility support
- [ ] **Keyboard Only**: Complete keyboard navigation
- [ ] **Color Blind**: Alternative color schemes
- [ ] **Font Scaling**: Adjustable text sizes

---

## 📝 **Development Notes**

### Technical Debt
- **Global State**: Refactor `current_player` into proper state management
- **Screen Coupling**: Reduce dependencies between screen classes
- **Error Handling**: Implement comprehensive exception management
- **Type Safety**: Complete type annotation coverage

### Testing Requirements
- **Unit Tests**: Core game mechanics testing
- **Integration Tests**: AI and vault integration testing
- **Performance Tests**: Large vault and extended gameplay testing
- **Cross-Platform**: macOS, Linux, Windows compatibility testing

### Documentation Updates
- **API Documentation**: Document all public interfaces
- **Tutorial System**: In-game help and tutorials
- **Video Guides**: Screen recording demonstrations
- **Community Wiki**: Player-contributed documentation

---

## 🎯 **Contribution Guidelines**

### Feature Priorities
1. **v0.1.0**: Inn system completion
2. **v0.2.0**: Shop functionality
3. **v0.3.0**: Banking system
4. **v0.4.0**: PvP combat

### Code Requirements
- Maintain LORD authenticity in all implementations
- Follow existing code style and architecture
- Add comprehensive testing for new features
- Update documentation for user-facing changes

### Testing Checklist for New Features
- [ ] Feature works with and without AI
- [ ] Maintains authentic LORD feel
- [ ] Handles edge cases gracefully
- [ ] Performance acceptable with large vaults
- [ ] Cross-platform compatibility verified

---

**Legend of the Obsidian Vault v0.0.1** - Your notes are waiting in the forest! 🌲⚔️📚
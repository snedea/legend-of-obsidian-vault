# TODO - Authentic LORD Implementation Roadmap

## 🧠 **IMMEDIATE PRIORITY: AI Enhancement (Tomorrow's Focus)**

**Mission**: Transform bland "Mosquito of My Themes Directory" encounters into epic fantasy adventures!

### **🔥 Quick Wins for Tomorrow (2-3 hours each)**

#### **Task 1: Enhanced Enemy Names**
**File**: `obsidian.py` → `_generate_enemy_name()` function
**Current**: "Mosquito of My Themes Directory" ❌
**Target**: "Vex'thara the Memory Weaver" ✅

```python
# Add to obsidian.py:
FANTASY_TITLES = ["Keeper", "Guardian", "Weaver", "Lord", "Wraith", "Sage"]
MYSTICAL_PREFIXES = ["Shadow", "Crimson", "Ancient", "Forgotten", "Whisper"]
KNOWLEDGE_THEMES = {
    "code": "Codex", "personal": "Memory", "meeting": "Council",
    "project": "Forge", "documentation": "Archive"
}
```

#### **Task 2: Enemy Backstories**
**File**: `game_data.py` → Extend Enemy class
**Add Fields**: `backstory`, `personality_type`, `knowledge_domain`

#### **Task 3: Combat Flavor Text**
**File**: `lov.py` → `CombatScreen._victory()` and attack methods
**Replace**: "You hit for 15 damage"
**With**: "Your Python knowledge pierces the guardian's confusion for 15 insight!"

### **📋 Detailed AI Roadmap Available**
See `TODO_AI_ENHANCEMENT.md` for complete 4-week implementation plan

---

## 🎯 **Mission: Complete LORD v4.00a Clone**

Based on the official LORD FAQ, this roadmap implements **every authentic feature** from the original game.

### ✅ **Working Features (v0.0.2)**
- Character creation (all 3 classes)
- Forest combat with note-based enemies
- **NEW**: Rich AI-generated dungeon master narratives
- **NEW**: Content-aware encounter descriptions
- **NEW**: Structured note parsing (headers, lists, numbers)
- TinyLlama AI quiz generation and narratives
- Obsidian vault auto-detection
- Basic town square navigation
- SQLite save system
- Authentic BBS-style interface

---

## 🏗️ **Phase 1: Core Game Systems (v0.1.0)**

### Skills System Implementation (Critical)
**Current State**: Basic class selection only

**Death Knight Skills**:
- [ ] Random skill learning at castle encounter
- [ ] Pure chance-based progression
- [ ] Ultra-mastery at 40 skill points
- [ ] Combat integration with daily usage limits

**Mystical Skills (6 Spells)**:
- [ ] **Pinch Real Hard (1)** - Basic enhanced damage
- [ ] **Disappear (4)** - Guaranteed escape
- [ ] **Heat Wave (8)** - High damage attack
- [ ] **Light Shield (12)** - Halves incoming damage
- [ ] **Shatter (16)** - Extremely powerful attack
- [ ] **Mind Heal (20)** - Complete health restoration
- [ ] Number guessing game (1-100, 6 attempts)

**Thievery Skills**:
- [ ] Gem-based learning system
- [ ] Forest combat advantages
- [ ] Special abilities against minor enemies

### Turgon's Warrior Training (Critical)
**Current State**: Basic level progression only

**11 Masters Implementation**:
- [ ] **Halder** (Level 1) - Short Sword, groin cup advice
- [ ] **Barak** (Level 2) - Battle Axe, bartender introduction
- [ ] **Aragorn** (Level 3) - Twin Swords, Violet mention
- [ ] **Olodrin** (Level 4) - Power Axe, humility lessons
- [ ] **Sandtiger** (Level 5) - Blessed Sword, eye patch story
- [ ] **Sparhawk** (Level 6) - Double Bladed Sword, respect teaching
- [ ] **Atsuko Sensei** (Level 7) - Huge Curved Blade, honor focus
- [ ] **Aladdin** (Level 8) - Shiny Lamp, genie jokes
- [ ] **Prince Caspian** (Level 9) - Flashing Rapier, perseverance
- [ ] **Gandalf** (Level 10) - Huge Fireballs, dragon destiny
- [ ] **Turgon** (Level 11) - Able's Sword, final challenge

**Authentic Stat Progression**:
```
Level  HP Gain  STR Gain  DEF Gain  Experience Needed
1      20       10        1         1
2      10       5         2         100
3      15       7         3         400
4      20       10        5         1,000
5      30       12        10        4,000
6      50       20        15        10,000
7      75       35        22        40,000
8      125      50        35        100,000
9      185      75        60        400,000
10     250      110       80        1,000,000
11     350      150       120       4,000,000
12     550      200       150       10,000,000
```

**Hall of Honours**:
- [ ] Dragon kill tracking
- [ ] Hero recognition system
- [ ] Game reset mechanics (after 10 wins)

---

## 🍺 **Phase 2: Inn System Completion (v0.2.0)**

### Bartender Features (High Priority)
**Current State**: Basic navigation only

**Core Services**:
- [ ] **Gem Exchange**: 2 gems = 1 stat point (prefer Defense)
- [ ] **Room Rental**: Level-based pricing (400-4800 gold)
- [ ] **Bribe System**: Kill sleeping players (3200-19200 gold)
- [ ] **Name Changes**: With restricted names (Seth, Barak, Turgon, etc.)
- [ ] **Free Stay**: At 101+ charm

**Level-Based Pricing Table**:
```
Level  Stay Cost  Bribe Cost
1      400        N/A
2      800        3200
3      1200       4800
...
12     4800       19200
```

### Violet Interaction System (High Priority)
**Current State**: Menu option exists, no implementation

**Charm-Based Flirtation**:
- [ ] **1 Charm**: Wink (5 Exp × Level)
- [ ] **2 Charm**: Kiss Her Hand (10 Exp × Level)
- [ ] **4 Charm**: Peck Her On The Lips (20 Exp × Level)
- [ ] **8 Charm**: Sit Her On Your Lap (30 Exp × Level)
- [ ] **16 Charm**: Grab Her Backside (40 Exp × Level)
- [ ] **32 Charm**: Carry Her Upstairs (40 Exp × Level)
- [ ] **100 Charm**: Marry Her (1000 Exp × Level)

**Grizelda System**:
- [ ] Replace Violet when married
- [ ] Humorous interaction text
- [ ] Painful buckteeth kiss

### Seth Able the Bard (High Priority)
**Current State**: Menu option exists, no implementation

**10 Song Types with Effects**:
- [ ] **Warrior Song**: 3 extra forest fights
- [ ] **Male/Female Strength**: 2-3 extra fights
- [ ] **Bard Story**: 2 extra fights
- [ ] **Red Dragon Legend**: 1 extra fight
- [ ] **Missing Children**: 1 extra user battle
- [ ] **Heritage Song**: Max out hitpoints
- [ ] **Legend Song**: +1 permanent hitpoint
- [ ] **Gods Prayer**: Double bank gold
- [ ] **Beauty Song**: +1 charm point

**Female Flirtation** (125 charm for marriage):
- [ ] Same progression as Violet
- [ ] Marriage responses when already wed
- [ ] Gender-specific song variations

---

## 🌟 **Phase 3: Advanced Systems (v0.3.0)**

### Dark Cloak Tavern (Medium Priority)
**Current State**: Not implemented

**Chance the Bartender**:
- [ ] Profession changing
- [ ] Player examination (2-3 gems)
- [ ] Color code system for names
- [ ] Gambling games (3 types)

**Color Name System**:
```
`1 Dark Blue    `9 Light Blue
`2 Dark Green   `0 Light Green
`3 Dark Cyan    `! Light Cyan
`4 Dark Red     `@ Light Red
`5 Dark Purple  `# Light Purple
`6 Orange       `$ Yellow
`7 White        `% White
`8 Dark Grey    `b Blinking Red
```

**Old Man's Rankings**:
- [ ] Evilness tracking
- [ ] Kill statistics
- [ ] Relationship status display

### Fairy System (Medium Priority)
**Current State**: Not implemented

**Fairy Encounters**:
- [ ] **Kiss Blessing**: Healing
- [ ] **Horse Gift**: Direct Dark Cloak travel
- [ ] **Sad Stories**: Tear → Gem conversion
- [ ] **Fairy Lore**: Experience bonus
- [ ] **Flower Arranging**: Player messaging

**Fairy Catching**:
- [ ] Revival on death (day only)
- [ ] Bank robbery (Thief + Fairy)
- [ ] Miss = thornberry bush (1 HP)

### Banking System Enhancement (Medium Priority)
**Current State**: Basic navigation only

**Core Features**:
- [ ] **10% Daily Interest**: Compound calculation
- [ ] **Deposit/Withdrawal**: Transfer validation
- [ ] **Transaction History**: Account tracking
- [ ] **Thief Bank Robbery**: Fairy requirement

---

## 💕 **Phase 4: Social Systems (v0.4.0)**

### Marriage & Romance (Medium Priority)
**Current State**: Conjugality list navigation only

**Romance Mail System**:
- [ ] **Male Options**: Flatter, Kiss, Dinner, Room, Propose
- [ ] **Female Options**: Same categories, different messages
- [ ] **Default Messages**: 5 random romantic phrases
- [ ] **Self-Mail Prevention**: Messenger refusal

**Marriage Mechanics**:
- [ ] **Proposal System**: 100/125 charm requirements
- [ ] **Wedding Ceremonies**: Public announcements
- [ ] **Divorce System**: 50% charm penalty
- [ ] **Status Tracking**: Relationship database

### Children System (Medium Priority)
**Current State**: Not implemented

**Kid Benefits**:
- [ ] **Extra Forest Fight**: +1 daily battle
- [ ] **Combat Intervention**: Kid helps when losing
- [ ] **Sacrifice Mechanic**: Kid dies protecting parent
- [ ] **Persistence**: Keep kids through divorce

### Player vs Player Combat (Medium Priority)
**Current State**: Menu exists, no implementation

**Combat Restrictions**:
- [ ] **Level Limits**: Can't kill 2+ levels down
- [ ] **Daily Limits**: 3 PvP fights per day
- [ ] **Experience Loss**: 10% for victim, 50% for killer
- [ ] **Gold/Gem Loss**: Transfer to winner

**Boasting System**:
- [ ] **5 Mood Options**: Happy, Sad, Moaning, Cursing, Effing Mad
- [ ] **Dirt Scratching**: Kill count messages
- [ ] **Public Messages**: Daily news integration

---

## 🐉 **Phase 5: Complete Monster System (v0.5.0)**

### All 131 Monsters Implementation (High Priority)
**Current State**: Basic random enemies

**Level-Organized Monster List**:
- [ ] **Level 1**: 11 monsters (Small Thief → Small Troll)
- [ ] **Level 2**: 11 monsters (Green Python → Rock Man)
- [ ] **Level 3**: 11 monsters (Lazy Bum → Magical Evil Gnome)
- [ ] **Level 4**: 11 monsters (Death Dog → Rock Man*)
- [ ] **Level 5**: 11 monsters (Pandion Knight → Black Sorcerer)
- [ ] **Level 6**: 11 monsters (Iron Warrior → Magical Evil Gnome)
- [ ] **Level 7**: 11 monsters (Emperor Len → Death Gnome)
- [ ] **Level 8**: 11 monsters (Screeching Witch → Death Gnome)
- [ ] **Level 9**: 11 monsters (Pink Elephant → Gollum's Wrath)
- [ ] **Level 10**: 11 monsters (Torak's Son → Black Sorcerer)
- [ ] **Level 11**: 11 monsters (Gorma the Leper → Cyclops Warrior)
- [ ] **Level 12**: 10 monsters (Corinthian Giant → Great Ogre)

**Authentic Monster Stats**:
- [ ] Exact HP, Strength, Gold, Experience values
- [ ] Power move death phrases
- [ ] Special powerful enemies marked with *

### Red Dragon Implementation (Critical)
**Current State**: Not implemented

**Dragon Combat System**:
- [ ] **15,000 Hit Points**: Increased from v3.25b
- [ ] **4 Attack Types**: Flaming Breath, Stomping, Claw, Tail
- [ ] **Flaming Breath**: 1000+ damage regardless of defense
- [ ] **Variable Damage**: Other attacks scale with defense

**Class-Specific Endings**:
- [ ] **Warrior Ending**: Heart trophy, crowd gathering
- [ ] **Wizard Ending**: Magical transport, nature calls trick
- [ ] **Thief Ending**: Bone looting, escape from angry mob

**Reset Mechanics**:
- [ ] Character reset after victory
- [ ] Skill/charm retention
- [ ] Hall of Honours entry

---

## 🎪 **Phase 6: Polish & Details (v0.6.0)**

### Daily Happenings System (Low Priority)
**Current State**: Not implemented

**10 Rotating Messages**:
- [ ] "More children are missing today."
- [ ] "A small girl was missing today."
- [ ] "The town is in grief. Several children didn't come home today."
- [ ] "Dragon sighting reported today by a drunken old man."
- [ ] "Despair covers the land - more bloody remains have been found today."
- [ ] "A group of children did not return from a nature walk today."
- [ ] "The land is in chaos today. Will the abductions ever stop?"
- [ ] "Dragon scales have been found in the forest today..Old or new?"
- [ ] "Several farmers report missing cattle today."
- [ ] "A Child was found today! But scared deaf and dumb."

### Exit Quotes System (Low Priority)
**Current State**: Not implemented

**5 Exit Messages**:
- [ ] "The black thing inside rejoices at your departure."
- [ ] "The very earth groans at your departure."
- [ ] "The very trees seem to moan as you leave."
- [ ] "Echoing screams fill the wastelands as you close your eyes."
- [ ] "Your very soul aches as you wake up from your favorite dream."

### Hidden Keys Implementation (Low Priority)
**Current State**: Not implemented

**Forest Hidden Keys**:
- [ ] **A**: "You brandish your weapon dramatically."
- [ ] **D**: "Your Death Knight skills cannot help you here."
- [ ] **M**: "Your Mystical skills cannot help you here."
- [ ] **T**: "Your Thieving skills cannot help you here."

**Combat Hidden Keys**:
- [ ] **Q**: "You are in combat! Try running."
- [ ] **S**: Show enemy stats
- [ ] **H**: "You are in combat, and they don't make house calls!"

### Charm Level Descriptions (Low Priority)
**Current State**: Basic charm tracking

**100 Charm Descriptions**:
- [ ] Male descriptions (0-100)
- [ ] Female descriptions (0-100)
- [ ] Opinion system integration

---

## 🛠️ **Technical Debt & Infrastructure**

### Code Quality Improvements
- [ ] **Refactor Global State**: Proper state management
- [ ] **Error Handling**: Comprehensive exception management
- [ ] **Type Safety**: Complete type annotation
- [ ] **Testing**: Unit tests for all LORD mechanics

### Performance Optimizations
- [ ] **Monster Loading**: Efficient large dataset handling
- [ ] **Save System**: Optimized database queries
- [ ] **Memory Usage**: Large-scale multiplayer support

### Documentation Updates
- [ ] **LORD Mechanics**: Document authentic formulas
- [ ] **Feature Parity**: Track original vs clone differences
- [ ] **Developer Guide**: LORD implementation details

---

## 🎯 **Version Milestones**

- **v0.1.0**: ✅ Skills System + Turgon's Training + Hall of Honours
- **v0.2.0**: 🧠 **AI Enhancement** - Fantasy Enemy Generation & Combat Narratives
- **v0.3.0**: Complete Inn System (Bartender, Violet, Seth)
- **v0.4.0**: Dark Cloak Tavern + Fairy System + Banking
- **v0.5.0**: Marriage, Kids, PvP Combat
- **v0.6.0**: All 131 Monsters + Red Dragon
- **v0.7.0**: Daily happenings, hidden keys, polish
- **v1.0.0**: **100% Feature-Complete LORD Clone with AI-Enhanced Immersion**

---

**Legend of the Obsidian Vault** - From Obsidian vault to authentic LORD experience! 🎮⚔️📚
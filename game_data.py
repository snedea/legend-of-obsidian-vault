"""
Legend of the Obsidian Vault - Core Game Data
Exact LORD mechanics and data structures
"""
import sqlite3
import random
from datetime import datetime, date
from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple
from pathlib import Path

# VGA/ANSI Color Palette (Exact BBS colors)
BBS_COLORS = {
    'BLACK': '#000000',
    'RED': '#AA0000',
    'GREEN': '#00AA00',
    'YELLOW': '#AA5500',
    'BLUE': '#0000AA',
    'MAGENTA': '#AA00AA',
    'CYAN': '#00AAAA',
    'WHITE': '#AAAAAA',
    'BRIGHT_BLACK': '#555555',
    'BRIGHT_RED': '#FF5555',
    'BRIGHT_GREEN': '#55FF55',
    'BRIGHT_YELLOW': '#FFFF55',
    'BRIGHT_BLUE': '#5555FF',
    'BRIGHT_MAGENTA': '#FF55FF',
    'BRIGHT_CYAN': '#55FFFF',
    'BRIGHT_WHITE': '#FFFFFF'
}

# LORD Weapons (EXACT prices and stats)
WEAPONS = [
    ("Stick", 200, 5),
    ("Dagger", 1000, 10),
    ("Short Sword", 3000, 20),
    ("Long Sword", 10000, 30),
    ("Huge Axe", 30000, 40),
    ("Bone Cruncher", 100000, 60),
    ("Twin Swords", 150000, 80),
    ("Power Axe", 200000, 120),
    ("Able's Sword", 400000, 180),
    ("Wan's Weapon", 1000000, 250),
    ("Spear of Gold", 4000000, 350),
    ("Crystal Shard", 10000000, 500),
    ("Nira's Teeth", 40000000, 800),
    ("Blood Sword", 100000000, 1200),
    ("Death Sword", 400000000, 1800)
]

# LORD Armor (EXACT prices and stats)
ARMOR = [
    ("Coat", 200, 5),
    ("Heavy Coat", 1000, 10),
    ("Leather Vest", 3000, 20),
    ("Bronze Armor", 10000, 30),
    ("Iron Armor", 30000, 40),
    ("Graphite Armor", 100000, 60),
    ("Erdrick's Armor", 150000, 80),
    ("Able's Armor", 200000, 120),
    ("Full Body Armor", 400000, 180),
    ("Blood Armor", 1000000, 250),
    ("Magic Protection", 4000000, 350),
    ("Belar's Mail", 10000000, 500),
    ("Golden Armor", 40000000, 800),
    ("Equipment of Lore", 100000000, 1200),
    ("Shimmering Armor", 400000000, 1800)
]

# Experience required for each level
LEVEL_EXP = [
    0, 100, 400, 1000, 2000, 4000, 8000, 16000, 32000, 64000, 128000, 256000, 512000
]

# Forest enemies by level (will be enhanced with Obsidian notes)
FOREST_ENEMIES = {
    1: [
        ("Small Thief", 15, 5, 50),
        ("Wild Boar", 20, 8, 75),
        ("Large Mosquito", 10, 3, 25),
        ("Old Man", 25, 10, 100)
    ],
    2: [
        ("Large Thief", 35, 15, 150),
        ("Raven", 25, 12, 100),
        ("Ugly Troll", 50, 20, 250)
    ],
    3: [
        ("Orc", 75, 30, 400),
        ("Skeleton", 60, 25, 350),
        ("Lizard Man", 80, 35, 450)
    ],
    4: [
        ("Hobgoblin", 120, 50, 600),
        ("Stone Golem", 150, 40, 750),
        ("Gargoyle", 100, 60, 550)
    ],
    5: [
        ("Minotaur", 200, 80, 1000),
        ("Cyclops", 250, 70, 1200),
        ("Giant Spider", 180, 90, 900)
    ],
    6: [
        ("Evil Mage", 300, 120, 1500),
        ("Demon", 350, 100, 1750),
        ("Dark Knight", 400, 150, 2000)
    ],
    7: [
        ("Vampire", 500, 180, 2500),
        ("Werewolf", 450, 200, 2250),
        ("Lich", 550, 160, 2750)
    ],
    8: [
        ("Dragon Whelp", 700, 250, 3500),
        ("Pit Fiend", 800, 220, 4000),
        ("Bone Dragon", 750, 280, 3750)
    ],
    9: [
        ("Young Dragon", 1000, 350, 5000),
        ("Balrog", 1200, 300, 6000),
        ("Death Knight", 1100, 400, 5500)
    ],
    10: [
        ("Ancient Dragon", 1500, 500, 7500),
        ("Archdemon", 1800, 450, 9000),
        ("Dracolich", 1700, 550, 8500)
    ],
    11: [
        ("Titan", 2500, 700, 12500),
        ("Avatar of Death", 3000, 650, 15000),
        ("Primordial", 2800, 750, 14000)
    ],
    12: [
        ("The Red Dragon", 10000, 2000, 50000)
    ]
}

# Mystical Skills (Exact LORD spells)
MYSTICAL_SPELLS = [
    (1, "Pinch Real Hard", "Basic damage, more than normal attack"),
    (4, "Disappear", "Guarantees a safe escape from your foe"),
    (8, "Heat Wave", "Quite powerful, at par with a Death Knight"),
    (12, "Light Shield", "Halves the damage you take, essential"),
    (16, "Shatter", "Incredibly powerful, can be worth 2 DK's"),
    (20, "Mind Heal", "Completely heal yourself!")
]

# Daily Happenings (Exact LORD text)
DAILY_HAPPENINGS = [
    "More children are missing today.",
    "A small girl was missing today.",
    "The town is in grief. Several children didn't come home today.",
    "Dragon sighting reported today by a drunken old man.",
    "Despair covers the land - more bloody remains have been found today.",
    "A group of children did not return from a nature walk today.",
    "The land is in chaos today. Will the abductions ever stop?",
    "Dragon scales have been found in the forest today..Old or new?",
    "Several farmers report missing cattle today.",
    "A Child was found today! But scared deaf and dumb."
]

# Exit Quotes (Exact LORD text)
EXIT_QUOTES = [
    "The black thing inside rejoices at your departure.",
    "The very earth groans at your departure.",
    "The very trees seem to moan as you leave.",
    "Echoing screams fill the wastelands as you close your eyes.",
    "Your very soul aches as you wake up from your favorite dream."
]

# Class types and their abilities
CLASS_TYPES = {
    'K': {
        'name': 'Death Knight',
        'description': 'Killing a lot of woodland creatures',
        'skill_name': 'Death Knight Attack',
        'daily_uses': 3
    },
    'P': {
        'name': 'Mystical',
        'description': 'Dabbling in the mystical forces',
        'skill_name': 'Mystical Spell',
        'daily_uses': 3
    },
    'D': {
        'name': 'Thieving',
        'description': 'Lying, cheating, and stealing from the blind',
        'skill_name': 'Thief Skill',
        'daily_uses': 3
    }
}

# Castles for events
CASTLES = [
    "Lamshire", "Pentis", "Kolbar", "Erinth", "Trenton", "Norshelm",
    "Darkmoor", "Kalesh", "Brinhill", "Westmont"
]

@dataclass
class Character:
    """Player character with EXACT LORD stats"""
    name: str = ""
    gender: str = "M"
    class_type: str = "K"
    level: int = 1
    experience: int = 0
    hitpoints: int = 20
    max_hitpoints: int = 20
    forest_fights: int = 15
    player_fights: int = 3
    gold: int = 500
    bank_gold: int = 0
    weapon: str = "Stick"
    weapon_num: int = 0
    armor: str = "Coat"
    armor_num: int = 0
    charm: int = 0
    gems: int = 0
    horse: bool = False
    fairy_blessing: bool = False
    flirted_violet: bool = False
    laid_today: bool = False
    inn_room: bool = False
    alive: bool = True
    days_played: int = 1
    last_played: str = ""
    skill_uses: int = 3
    married_to: str = ""
    married: bool = False

    # Skill Points (Exact LORD mechanics)
    death_knight_points: int = 0
    mystical_points: int = 0
    thieving_points: int = 0

    # Skill Knowledge Tracking
    learned_spells: str = ""  # Comma-separated list of spell levels known

    # Daily Skill Usage Tracking
    skills_used_today: int = 0

    def __post_init__(self):
        if not self.last_played:
            self.last_played = str(date.today())

    @property
    def attack_power(self) -> int:
        """Calculate total attack power"""
        weapon_power = WEAPONS[self.weapon_num][2] if self.weapon_num < len(WEAPONS) else 5
        level_bonus = self.level * 2
        return weapon_power + level_bonus

    @property
    def defense_power(self) -> int:
        """Calculate total defense power"""
        armor_power = ARMOR[self.armor_num][2] if self.armor_num < len(ARMOR) else 5
        level_bonus = self.level
        return armor_power + level_bonus

    def can_level_up(self) -> bool:
        """Check if player can level up"""
        if self.level >= 12:
            return False
        return self.experience >= LEVEL_EXP[self.level]

    def level_up(self):
        """Level up the character"""
        if self.can_level_up():
            self.level += 1
            hp_gain = random.randint(10, 20)
            self.max_hitpoints += hp_gain
            self.hitpoints = self.max_hitpoints
            return hp_gain
        return 0

    def daily_reset(self):
        """Reset daily counters"""
        today = str(date.today())
        if self.last_played != today:
            self.forest_fights = 15
            self.player_fights = 3
            self.flirted_violet = False
            self.laid_today = False
            self.alive = True
            self.skill_uses = CLASS_TYPES[self.class_type]['daily_uses']
            self.last_played = today

            # Bank interest (10% daily)
            self.bank_gold = int(self.bank_gold * 1.10)

            # Reset daily skill usage
            self.skills_used_today = 0

    def get_skill_points(self, skill_type: str) -> int:
        """Get skill points for specific type"""
        if skill_type == 'K':
            return self.death_knight_points
        elif skill_type == 'P':
            return self.mystical_points
        elif skill_type == 'D':
            return self.thieving_points
        return 0

    def add_skill_points(self, skill_type: str, points: int = 1):
        """Add skill points (max 40 for ultra-mastery)"""
        if skill_type == 'K':
            self.death_knight_points = min(40, self.death_knight_points + points)
        elif skill_type == 'P':
            self.mystical_points = min(40, self.mystical_points + points)
        elif skill_type == 'D':
            self.thieving_points = min(40, self.thieving_points + points)

    def has_ultra_mastery(self, skill_type: str) -> bool:
        """Check if player has ultra-mastery (40 points)"""
        return self.get_skill_points(skill_type) >= 40

    def knows_spell(self, spell_level: int) -> bool:
        """Check if player knows a mystical spell"""
        if not self.learned_spells:
            return False
        known_levels = [int(x) for x in self.learned_spells.split(',') if x.strip()]
        return spell_level in known_levels

    def learn_spell(self, spell_level: int):
        """Learn a new mystical spell"""
        if not self.knows_spell(spell_level):
            if self.learned_spells:
                self.learned_spells += f",{spell_level}"
            else:
                self.learned_spells = str(spell_level)

    def get_available_spells(self) -> List[Tuple[int, str, str]]:
        """Get spells available to cast based on mystical points"""
        available = []
        for points_needed, name, description in MYSTICAL_SPELLS:
            if self.mystical_points >= points_needed and self.knows_spell(points_needed):
                available.append((points_needed, name, description))
        return available

    def can_use_skill(self) -> bool:
        """Check if player can use skill today"""
        return self.skills_used_today < CLASS_TYPES[self.class_type]['daily_uses']

    def use_skill(self):
        """Use a skill (consume daily usage)"""
        if self.can_use_skill():
            self.skills_used_today += 1
            return True
        return False

@dataclass
class Enemy:
    """Forest enemy"""
    name: str
    hitpoints: int
    attack: int
    gold_reward: int
    exp_reward: int
    level: int = 1
    note_content: str = ""
    note_title: str = ""

    def __post_init__(self):
        self.max_hitpoints = self.hitpoints

@dataclass
class ObsidianNote:
    """Obsidian vault note"""
    path: Path
    title: str
    content: str
    created: datetime
    modified: datetime
    tags: List[str]

    @property
    def age_days(self) -> int:
        """Days since last modified"""
        return (datetime.now() - self.modified).days

    @property
    def difficulty_level(self) -> int:
        """Difficulty based on age - older notes are harder"""
        if self.age_days < 7:
            return 1
        elif self.age_days < 30:
            return min(2 + (self.age_days // 7), 6)
        elif self.age_days < 90:
            return min(7 + (self.age_days // 30), 9)
        else:
            return min(10 + (self.age_days // 90), 12)

class GameDatabase:
    """SQLite database for player saves"""

    def __init__(self, db_path: str = "saves/players.db"):
        self.db_path = db_path
        Path(db_path).parent.mkdir(exist_ok=True)
        self.init_db()

    def init_db(self):
        """Initialize database tables"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    name TEXT PRIMARY KEY,
                    gender TEXT,
                    class_type TEXT,
                    level INTEGER,
                    experience INTEGER,
                    hitpoints INTEGER,
                    max_hitpoints INTEGER,
                    forest_fights INTEGER,
                    player_fights INTEGER,
                    gold INTEGER,
                    bank_gold INTEGER,
                    weapon TEXT,
                    weapon_num INTEGER,
                    armor TEXT,
                    armor_num INTEGER,
                    charm INTEGER,
                    gems INTEGER,
                    horse BOOLEAN,
                    fairy_blessing BOOLEAN,
                    flirted_violet BOOLEAN,
                    laid_today BOOLEAN,
                    inn_room BOOLEAN,
                    alive BOOLEAN,
                    days_played INTEGER,
                    last_played TEXT,
                    skill_uses INTEGER,
                    married_to TEXT,
                    married BOOLEAN,
                    death_knight_points INTEGER DEFAULT 0,
                    mystical_points INTEGER DEFAULT 0,
                    thieving_points INTEGER DEFAULT 0,
                    learned_spells TEXT DEFAULT '',
                    skills_used_today INTEGER DEFAULT 0
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS bar_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player TEXT,
                    message TEXT,
                    timestamp TEXT
                )
            """)

    def save_player(self, player: Character):
        """Save player to database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO players VALUES
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                player.name, player.gender, player.class_type, player.level,
                player.experience, player.hitpoints, player.max_hitpoints,
                player.forest_fights, player.player_fights, player.gold,
                player.bank_gold, player.weapon, player.weapon_num,
                player.armor, player.armor_num, player.charm, player.gems,
                player.horse, player.fairy_blessing, player.flirted_violet,
                player.laid_today, player.inn_room, player.alive,
                player.days_played, player.last_played, player.skill_uses,
                player.married_to, player.married, player.death_knight_points,
                player.mystical_points, player.thieving_points, player.learned_spells,
                player.skills_used_today
            ))

    def load_player(self, name: str) -> Optional[Character]:
        """Load player from database"""
        with sqlite3.connect(self.db_path) as conn:
            result = conn.execute("SELECT * FROM players WHERE name = ?", (name,)).fetchone()
            if result:
                return Character(*result)
        return None

    def get_all_players(self) -> List[Character]:
        """Get all players for leaderboard"""
        with sqlite3.connect(self.db_path) as conn:
            results = conn.execute("SELECT * FROM players ORDER BY level DESC, experience DESC").fetchall()
            return [Character(*row) for row in results]

# Skill Learning Functions

def death_knight_encounter(player: Character) -> Tuple[bool, str]:
    """Death Knight castle encounter - pure random learning"""
    if random.randint(1, 3) == 1:  # 33% chance
        player.add_skill_points('K', 1)
        points = player.get_skill_points('K')
        if points >= 40:
            return True, f"**ULTRA MASTERY!** You have achieved ultimate Death Knight mastery! ({points}/40)"
        else:
            return True, f"You have learned more Death Knight skills! ({points}/40)"
    else:
        return False, "The Death Knights reject your training this time."

def mystical_learning_game(player: Character, guess: int, target: int, attempts_left: int) -> Tuple[bool, str, bool]:
    """Mystical skills number guessing game (1-100, 6 attempts)"""
    if guess == target:
        # Success! Learn a skill point
        player.add_skill_points('P', 1)
        points = player.get_skill_points('P')

        # Check if player can learn new spells
        new_spells = []
        for spell_points, spell_name, description in MYSTICAL_SPELLS:
            if points >= spell_points and not player.knows_spell(spell_points):
                player.learn_spell(spell_points)
                new_spells.append(spell_name)

        result = f"Correct! You have gained mystical knowledge! ({points}/40)"
        if new_spells:
            result += f"\n**NEW SPELL LEARNED:** {', '.join(new_spells)}"

        if points >= 40:
            result += "\n**ULTRA MASTERY!** Ultimate mystical mastery achieved!"

        return True, result, True

    elif attempts_left <= 1:
        return False, "You have failed to grasp the mystical knowledge this time.", True

    else:
        hint = "Higher!" if guess < target else "Lower!"
        return False, f"{hint} You have {attempts_left - 1} attempts remaining.", False

def thieving_encounter(player: Character, has_gem: bool, choice: str) -> Tuple[bool, str]:
    """Thieving skills encounter - gem-based learning"""
    if has_gem and choice.lower().startswith('g'):  # Give gem
        if player.gems > 0:
            player.gems -= 1
            player.add_skill_points('D', 1)
            points = player.get_skill_points('D')

            if points >= 40:
                return True, f"**ULTRA MASTERY!** You have achieved ultimate Thieving mastery! ({points}/40)"
            else:
                return True, f"The thieves accept your gem and teach you! ({points}/40)"
        else:
            return False, "You don't have any gems to give!"

    elif choice.lower().startswith('s'):  # Spit
        return False, "You spit at them. They leave in disgust, but at least they didn't rob you."

    else:  # Mumble or anything else
        return False, "You mumble incoherently. The thieves shake their heads and vanish."

def get_daily_happening() -> str:
    """Get random daily happening message"""
    return random.choice(DAILY_HAPPENINGS)

def get_exit_quote() -> str:
    """Get random exit quote"""
    return random.choice(EXIT_QUOTES)
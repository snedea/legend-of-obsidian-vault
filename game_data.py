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
                    married BOOLEAN
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
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                player.name, player.gender, player.class_type, player.level,
                player.experience, player.hitpoints, player.max_hitpoints,
                player.forest_fights, player.player_fights, player.gold,
                player.bank_gold, player.weapon, player.weapon_num,
                player.armor, player.armor_num, player.charm, player.gems,
                player.horse, player.fairy_blessing, player.flirted_violet,
                player.laid_today, player.inn_room, player.alive,
                player.days_played, player.last_played, player.skill_uses,
                player.married_to, player.married
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
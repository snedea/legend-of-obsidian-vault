"""
Legend of the Obsidian Vault - Core Game Data
Exact LORD mechanics and data structures
"""
import sqlite3
import random
from datetime import datetime, date
from dataclasses import dataclass, field
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

# Inn pricing (Exact LORD costs by level)
INN_ROOM_COSTS = [400, 800, 1200, 1600, 2000, 2400, 2800, 3200, 3600, 4000, 4400, 4800]
BRIBE_COSTS = [0, 3200, 4800, 6400, 8000, 9600, 11200, 12800, 14400, 16000, 17600, 19200]

# Reserved names that cannot be used
RESERVED_NAMES = {
    "BARAK": "Naw, the real Barak would decapitate you if he found out.",
    "SETH": "You are not Seth Able! Don't take his name in vain!",
    "SETH ABLE": "You are not God!",
    "TURGON": "Haw. Hardly - Turgon has muscles.",
    "VIOLET": "Haw. Hardly - Violet has breasts.",
    "RED DRAGON": "Oh go plague some other land!",
    "DRAGON": "You ain't Bruce Lee, so get out!",
    "BARTENDER": "Nah, the bartender is smarter than you!",
    "CHANCE": "Why not go take a chance with a rattlesnake?"
}

# Violet flirting options by charm level (Exact LORD)
VIOLET_FLIRT_OPTIONS = {
    1: {"action": "Wink", "exp_multiplier": 5, "message": "Violet smiles at you sweetly."},
    2: {"action": "Kiss Her Hand", "exp_multiplier": 10, "message": "Violet blushes as you kiss her hand."},
    4: {"action": "Peck Her On The Lips", "exp_multiplier": 20, "message": "Violet's lips are soft and warm."},
    8: {"action": "Sit Her On Your Lap", "exp_multiplier": 30, "message": "Violet giggles as she sits on your lap."},
    16: {"action": "Grab Her Backside", "exp_multiplier": 40, "message": "Violet squeals with delight!"},
    32: {"action": "Carry Her Upstairs", "exp_multiplier": 40, "message": "You carry Violet upstairs...", "special": "laid"},
    100: {"action": "Marry Her", "exp_multiplier": 1000, "message": "Violet says 'Yes!' You are now married!", "special": "marry"}
}

# Seth Able flirting options for female characters
SETH_FLIRT_OPTIONS = {
    1: {"action": "Wink", "exp_multiplier": 5, "message": "Seth winks back with a charming smile."},
    2: {"action": "Flutter Eyelashes", "exp_multiplier": 10, "message": "Seth is captivated by your beauty."},
    4: {"action": "Drop Hanky", "exp_multiplier": 20, "message": "Seth gallantly picks up your handkerchief."},
    8: {"action": "Ask The Bard to Buy You a Drink", "exp_multiplier": 30, "message": "Seth buys you the finest wine."},
    16: {"action": "Kiss the Bard Soundly", "exp_multiplier": 40, "message": "Seth is swept away by your passion!"},
    32: {"action": "Completely Seduce The Bard", "exp_multiplier": 40, "message": "You seduce the handsome bard...", "special": "laid"},
    125: {"action": "Marry Him", "exp_multiplier": 0, "message": "Seth says 'Yes!' You are now married!", "special": "marry"}
}

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

    # Hall of Honours tracking
    dragon_kills: int = 0
    times_won_game: int = 0
    total_kills: int = 0
    hall_of_honours_entry: str = ""  # Date of first dragon kill

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
        return self.experience >= LEVEL_EXP.get(self.level + 1, float('inf'))

    def get_next_level_exp(self) -> int:
        """Get experience needed for next level"""
        if self.level >= 12:
            return 0
        return LEVEL_EXP.get(self.level + 1, 0)

    def can_challenge_master(self) -> bool:
        """Check if player can challenge the next master"""
        if self.level >= 12:
            return False
        return self.can_level_up()

    def get_current_master(self) -> Optional[Dict]:
        """Get the master for current level"""
        if self.level <= 11:
            return MASTERS.get(self.level)
        return None

    def level_up_authentic(self):
        """Level up using authentic LORD stat progression"""
        if not self.can_level_up() or self.level >= 12:
            return False

        old_level = self.level
        self.level += 1

        # Apply authentic LORD stat gains
        gains = LEVEL_GAINS.get(self.level, {'hp': 0, 'str': 0, 'def': 0})
        hp_gain = gains['hp']

        self.max_hitpoints += hp_gain
        self.hitpoints = self.max_hitpoints  # Full heal on level up

        return {
            'old_level': old_level,
            'new_level': self.level,
            'hp_gain': hp_gain,
            'master': MASTERS.get(old_level),
            'level_up_text': MASTERS.get(old_level, {}).get('level_up_text', f"You are now level {self.level}!")
        }

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
    """Forest enemy with enhanced lore and personality"""
    name: str
    hitpoints: int
    attack: int
    gold_reward: int
    exp_reward: int
    level: int = 1
    note_content: str = ""
    note_title: str = ""

    # Enhanced lore fields
    backstory: str = ""
    personality_type: str = ""
    knowledge_domain: str = ""
    age_descriptor: str = ""
    folder_theme: str = ""
    combat_phrases: List[str] = field(default_factory=list)
    defeat_message: str = ""
    victory_message: str = ""

    # New LORD-style fields
    description: str = ""
    weapon: str = ""
    armor: str = ""

    # Rich narrative fields
    encounter_narrative: str = ""
    environment_description: str = ""
    manifestation_story: str = ""

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

    def _migrate_database(self, conn):
        """Migrate existing database to add missing columns"""
        try:
            # Get current table info
            cursor = conn.execute("PRAGMA table_info(players)")
            existing_columns = {row[1] for row in cursor.fetchall()}

            # Define all expected columns with their SQL types
            expected_columns = [
                ("death_knight_points", "INTEGER DEFAULT 0"),
                ("mystical_points", "INTEGER DEFAULT 0"),
                ("thieving_points", "INTEGER DEFAULT 0"),
                ("learned_spells", "TEXT DEFAULT ''"),
                ("skills_used_today", "INTEGER DEFAULT 0"),
                ("dragon_kills", "INTEGER DEFAULT 0"),
                ("times_won_game", "INTEGER DEFAULT 0"),
                ("total_kills", "INTEGER DEFAULT 0"),
                ("hall_of_honours_entry", "TEXT DEFAULT ''")
            ]

            # Add missing columns
            for column_name, column_def in expected_columns:
                if column_name not in existing_columns:
                    try:
                        conn.execute(f"ALTER TABLE players ADD COLUMN {column_name} {column_def}")
                        print(f"Added column: {column_name}")
                    except sqlite3.OperationalError as e:
                        # Column might already exist, ignore
                        pass

        except sqlite3.OperationalError:
            # Table doesn't exist yet, will be created by CREATE TABLE IF NOT EXISTS
            pass

    def init_db(self):
        """Initialize database tables"""
        with sqlite3.connect(self.db_path) as conn:
            # Check if we need to migrate existing tables
            self._migrate_database(conn)

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
                    skills_used_today INTEGER DEFAULT 0,
                    dragon_kills INTEGER DEFAULT 0,
                    times_won_game INTEGER DEFAULT 0,
                    total_kills INTEGER DEFAULT 0,
                    hall_of_honours_entry TEXT DEFAULT ''
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
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                player.skills_used_today, player.dragon_kills, player.times_won_game,
                player.total_kills, player.hall_of_honours_entry
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

    def is_violet_married(self) -> bool:
        """Check if Violet is married to anyone"""
        with sqlite3.connect(self.db_path) as conn:
            result = conn.execute("SELECT COUNT(*) FROM players WHERE married_to = 'Violet'").fetchone()
            return result[0] > 0

    def get_violet_husband(self) -> Optional[str]:
        """Get name of player married to Violet"""
        with sqlite3.connect(self.db_path) as conn:
            result = conn.execute("SELECT name FROM players WHERE married_to = 'Violet'").fetchone()
            return result[0] if result else None

    def is_seth_married(self) -> bool:
        """Check if Seth is married to anyone"""
        with sqlite3.connect(self.db_path) as conn:
            result = conn.execute("SELECT COUNT(*) FROM players WHERE married_to = 'Seth'").fetchone()
            return result[0] > 0

    def get_seth_wife(self) -> Optional[str]:
        """Get name of player married to Seth"""
        with sqlite3.connect(self.db_path) as conn:
            result = conn.execute("SELECT name FROM players WHERE married_to = 'Seth'").fetchone()
            return result[0] if result else None

    def get_players_at_inn(self) -> List[Character]:
        """Get all players currently at the inn"""
        with sqlite3.connect(self.db_path) as conn:
            results = conn.execute("SELECT * FROM players WHERE inn_room = 1").fetchall()
            return [Character(*row) for row in results]

    def marry_violet(self, player_name: str):
        """Handle marriage to Violet"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE players
                SET married = 1, married_to = 'Violet'
                WHERE name = ?
            """, (player_name,))

    def divorce_from_violet(self, player_name: str):
        """Handle divorce from Violet - sets charm to 50"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE players
                SET married = 0, married_to = '', charm = 50
                WHERE name = ?
            """, (player_name,))

    def divorce_from_seth(self, player_name: str):
        """Handle divorce from Seth - sets charm to 30 for females"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE players
                SET married = 0, married_to = '', charm = 30
                WHERE name = ?
            """, (player_name,))

# Turgon's Masters (Exact LORD data)
MASTERS = {
    1: {
        'name': 'Halder',
        'weapon': 'Short Sword',
        'greeting': "Hi there. Although I may not look muscular, I ain't all that weak. You cannot advance to another Master until you can best me in battle. I don't really have any advice except wear a groin cup at all times. I learned the hard way.",
        'ready': "Gee, your muscles are getting bigger than mine...",
        'victory': "Belar!!! You are truly a great warrior!",
        'level_up_text': "You are now level two, and ready to face greater challenges!"
    },
    2: {
        'name': 'Barak',
        'weapon': 'Battle Axe',
        'greeting': "You are now level two, and a respected warrior. Try talking to the Bartender, he will see you now. He is a worthy asset... Remember, your ultimate goal is to reach Ultimate Warrior status, which is level twelve.",
        'ready': "You know, you are actually getting pretty good with that thing...",
        'victory': "Children Of Mara!!! You have bested me??!",
        'level_up_text': "You are now level three! Your reputation grows in the realm."
    },
    3: {
        'name': 'Aragorn',
        'weapon': 'Twin Swords',
        'greeting': "You are now level three, and you are actually becoming well known in the realm. I heard your name being mentioned by Violet.... Ye Gods she's hot....",
        'ready': "You have learned everything I can teach you.",
        'victory': "Torak's Eye!!! You are a great warrior!",
        'level_up_text': "You are now level four! Even Violet has heard of you."
    },
    4: {
        'name': 'Olodrin',
        'weapon': 'Power Axe',
        'greeting': "You are now level four. But don't get cocky - There are many in the realm that could kick your... Nevermind, I'm just not good at being inspirational.",
        'ready': "You're becoming a very skilled warrior.",
        'victory': "Ye Gods!! You are a master warrior!",
        'level_up_text': "You are now level five! Don't let it go to your head."
    },
    5: {
        'name': 'Sandtiger',
        'weapon': 'Blessed Sword',
        'greeting': "You are now level five..Not bad...Not bad at all.. I am called Sandtiger - Because.. Actually I can't remember why people call me that. Oh - Don't pay attention to that stupid bartender - I could make a much better one.",
        'ready': "Gee - You really know how to handle your shaft!",
        'victory': "Very impressive...Very VERY impressive.",
        'level_up_text': "You are now level six! Sandtiger is proud of you."
    },
    6: {
        'name': 'Sparhawk',
        'weapon': 'Double Bladed Sword',
        'greeting': "You are level six! Vengeance is yours! You can now beat up on all those young punks that made fun of you when you were level 1. This patch? Oh - I lost my eye when I fell on my sword after tripping over a gopher. If you tell anyone this, I'll hunt you down.",
        'ready': "You're getting the hang of it now!",
        'victory': "This Battle is yours...You have fought with honor.",
        'level_up_text': "You are now level seven! Your skill with weapons is legendary."
    },
    7: {
        'name': 'Atsuko Sensei',
        'weapon': 'Huge Curved Blade',
        'greeting': "Even in my country, you would be considered a good warrior. But you have much to learn. Remember to always respect your teachers, for it is right.",
        'ready': "You are ready to be tested on the battle field!",
        'victory': "Even though you beat me, I am proud of you.",
        'level_up_text': "You are now level eight! Honor guides your blade."
    },
    8: {
        'name': 'Aladdin',
        'weapon': 'Shiny Lamp',
        'greeting': "You are now level eight. Remember, do not use your great strength in bullying the other warriors. Do not be a braggart. Be humble, and remember, honor is everything.",
        'ready': "You REALLY know how to use your weapon!!!",
        'victory': "I don't need a genie to see that you beat me, man!",
        'level_up_text': "You are now level nine! Your wisdom matches your strength."
    },
    9: {
        'name': 'Prince Caspian',
        'weapon': 'Flashing Rapier',
        'greeting': "You are now level nine. You have traveled far on the road of hardships, but what doesn't kill you, only makes you stronger. Never stop fighting.",
        'ready': "Something tells me you are as good as I am now..",
        'victory': "Good show, chap! Jolly good show!",
        'level_up_text': "You are now level ten! Your perseverance is unmatched."
    },
    10: {
        'name': 'Gandalf',
        'weapon': 'Huge Fireballs',
        'greeting': "You are now level ten.. A true honor! Do not stop now... You may be the one to rid the realm of the Red Dragon yet... Only two more levels to go until you are the greatest warrior in the land.",
        'ready': "You're becoming a very skilled warrior.",
        'victory': "Torak's Tooth! You are great!",
        'level_up_text': "You are now level eleven! The Red Dragon awaits..."
    },
    11: {
        'name': 'Turgon',
        'weapon': "Able's Sword",
        'greeting': "I am Turgon, son. The greatest warrior in the realm. You are a great warrior, and if you best me, you must find and kill the Red Dragon. I have every faith in you.",
        'ready': "You are truly the BEST warrior in the realm.",
        'victory': "You are a master warrior! You pay your respects to Turgon, and stroll around the grounds. Lesser warriors bow low as you pass. Turgon's last words advise you to find and kill the Red Dragon..",
        'level_up_text': "You are now level twelve! You are the Ultimate Warrior! Only the Red Dragon stands between you and true glory!"
    }
}

# Experience Requirements (Exact LORD progression)
LEVEL_EXP = {
    1: 1,
    2: 100,
    3: 400,
    4: 1000,
    5: 4000,
    6: 10000,
    7: 40000,
    8: 100000,
    9: 400000,
    10: 1000000,
    11: 4000000,
    12: 10000000
}

# Level Stat Gains (Exact LORD progression)
LEVEL_GAINS = {
    1: {'hp': 20, 'str': 10, 'def': 1},
    2: {'hp': 10, 'str': 5, 'def': 2},
    3: {'hp': 15, 'str': 7, 'def': 3},
    4: {'hp': 20, 'str': 10, 'def': 5},
    5: {'hp': 30, 'str': 12, 'def': 10},
    6: {'hp': 50, 'str': 20, 'def': 15},
    7: {'hp': 75, 'str': 35, 'def': 22},
    8: {'hp': 125, 'str': 50, 'def': 35},
    9: {'hp': 185, 'str': 75, 'def': 60},
    10: {'hp': 250, 'str': 110, 'def': 80},
    11: {'hp': 350, 'str': 150, 'def': 120},
    12: {'hp': 550, 'str': 200, 'def': 150}
}

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

def can_level_up(player: Character) -> bool:
    """Check if player can level up"""
    if player.level >= 12:
        return False
    return player.experience >= LEVEL_EXP.get(player.level + 1, float('inf'))

def get_next_level_exp(current_level: int) -> int:
    """Get experience needed for next level"""
    next_level = current_level + 1
    return LEVEL_EXP.get(next_level, float('inf'))

def create_master_enemy(level: int, master_data: dict) -> Enemy:
    """Create an enemy representing a training master"""
    # Masters are challenging but not impossible
    # Scale with level but keep beatable
    base_hp = 15 + (level * 8)
    base_attack = 8 + (level * 3)

    enemy = Enemy(
        name=f"Master {master_data['name']}",
        hitpoints=base_hp,
        attack=base_attack,
        gold_reward=50 + (level * 25),  # Good gold reward
        exp_reward=level * 15,   # Decent experience
        level=level
    )

    # Add custom attributes for master fights
    enemy.death_phrase = f"Master {master_data['name']} yields to your skill!"
    enemy.power_move = "Master's Technique"

    return enemy

def record_dragon_kill(player: Character) -> str:
    """Record a dragon kill in Hall of Honours"""
    from datetime import datetime

    player.dragon_kills += 1
    player.total_kills += 1
    player.times_won_game += 1

    # Set hall entry date if first dragon kill
    if not player.hall_of_honours_entry:
        player.hall_of_honours_entry = datetime.now().strftime("%B %d, %Y")

    # Return victory message based on class
    if player.class_type == 'K':  # Death Knight
        return f"{player.name} the Death Knight has slain the Red Dragon! The crowd cheers as you hold up the dragon's heart as a trophy!"
    elif player.class_type == 'M':  # Mystical
        return f"{player.name} the Mystical has defeated the Red Dragon through magic! You are transported away by mystical forces!"
    else:  # Thief
        return f"{player.name} the Thief has slain the Red Dragon! You quickly loot the dragon's bones before escaping the angry mob!"

def get_hall_of_honours_entries(db: 'GameDatabase') -> List[tuple]:
    """Get all Hall of Honours entries sorted by dragon kills"""
    with sqlite3.connect(db.db_path) as conn:
        results = conn.execute("""
            SELECT name, class_type, dragon_kills, times_won_game, hall_of_honours_entry, level
            FROM players
            WHERE dragon_kills > 0
            ORDER BY dragon_kills DESC, hall_of_honours_entry ASC
            LIMIT 20
        """).fetchall()
        return results

def reset_player_after_dragon(player: Character):
    """Reset player stats after dragon victory (authentic LORD mechanic)"""
    # Keep name, class, and Hall of Honours stats
    name = player.name
    class_type = player.class_type
    gender = player.gender
    dragon_kills = player.dragon_kills
    times_won_game = player.times_won_game
    total_kills = player.total_kills
    hall_entry = player.hall_of_honours_entry

    # Keep some skills/charm as per LORD mechanics
    skill_k = min(player.death_knight_points, 10)  # Keep some skill
    skill_m = min(player.mystical_points, 10)
    skill_d = min(player.thieving_points, 10)
    charm_keep = min(player.charm, 20)  # Keep some charm

    # Reset everything else to starting values
    player.__init__()  # Reset to defaults
    player.name = name
    player.class_type = class_type
    player.gender = gender
    player.dragon_kills = dragon_kills
    player.times_won_game = times_won_game
    player.total_kills = total_kills
    player.hall_of_honours_entry = hall_entry
    player.death_knight_points = skill_k
    player.mystical_points = skill_m
    player.thieving_points = skill_d
    player.charm = charm_keep

def get_exit_quote() -> str:
    """Get random exit quote"""
    return random.choice(EXIT_QUOTES)
"""
Barak's House IGM for Legend of the Obsidian Vault
Working version following IGM pattern with all features
"""
import datetime
import random
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static
from textual import events


class BarakHouseScreen(Screen):
    """Barak's House - Simplified version"""

    def __init__(self):
        super().__init__()

    def compose(self) -> ComposeResult:
        # Delayed import to avoid circular dependency
        import lov

        # Colored Barak's House ASCII Art Header
        yield Static("        ✦ BARAK'S HOUSE OF KNOWLEDGE ✦", classes="barak-title")
        yield Static("    ╔══════════════════════════════════════════════╗", classes="barak-border")
        yield Static("    ║  📚    🏠    📖    📜    ✨    📚    🏠  ║", classes="barak-decoration")
        yield Static("    ║                                              ║", classes="barak-border")
        yield Static("    ║     「 Scholar's Sanctuary & Game Den 」      ║", classes="barak-banner")
        yield Static("    ║                                              ║", classes="barak-border")
        yield Static("    ║   📚 Ancient Tomes    🎓 Knowledge Arts     ║", classes="barak-decoration")
        yield Static("    ║   📖 Study Halls      ⚔️ Warrior Training   ║", classes="barak-decoration")
        yield Static("    ║   📜 Sage Wisdom      💰 Scholar's Rewards  ║", classes="barak-decoration")
        yield Static("    ╚══════════════════════════════════════════════╝", classes="barak-border")

        # Two blank lines below header
        yield Static("")
        yield Static("")

        # Content
        yield Static("Welcome to Barak's House, where knowledge and fortune intertwine.", classes="barak-content")
        yield Static("The scholarly atmosphere is thick with the scent of ancient parchments.", classes="barak-content")
        yield Static("")

        # Check aggression level
        total_kills = getattr(lov.current_player, 'total_kills', 0)
        if total_kills < 10:
            aggression_text = "peaceful and scholarly"
        elif total_kills < 50:
            aggression_text = "moderately experienced"
        elif total_kills < 100:
            aggression_text = "battle-hardened"
        elif total_kills < 200:
            aggression_text = "fearsome and dangerous"
        else:
            aggression_text = "legendary and terrifying"

        yield Static(f"Barak notices your demeanor: {aggression_text}", classes="barak-content")
        yield Static("")

        # Available actions
        yield Static("═══ AVAILABLE ACTIONS ═══", classes="barak-content")
        yield Static("(R)ead ancient books - Gain INT, experience, or skill points", classes="barak-content")
        yield Static("(S)tudy combat techniques - Gain +1-2 STR/DEF/CHARM randomly", classes="barak-content")
        yield Static("(T)alk to Barak - Free lore + 20% chance bonus gold/gems/INT", classes="barak-content")
        yield Static("")
        yield Static("(L)eave house", classes="barak-content")

        # One blank line before status
        yield Static("")

        # Player status line
        hp_text = f"({lov.current_player.hitpoints} of {lov.current_player.max_hitpoints})"
        status_line = f"HitPoints: {hp_text}  Gold: {lov.current_player.gold}  INT: {lov.current_player.intelligence}"
        yield Static(status_line, classes="barak-status")

        # One blank line before command area
        yield Static("")

        # Command prompt area
        now = datetime.datetime.now()
        time_str = f"{now.hour:02d}:{now.minute:02d}"

        # Location and commands
        location_commands = "Barak's House (R,S,T,L)  (? for menu)"
        yield Static(location_commands, classes="barak-location-commands")

        # Command prompt with time and cursor
        yield Static(f"Your command, {lov.current_player.name}? [{time_str}]: █", classes="barak-prompt")

    def on_key(self, event: events.Key) -> None:
        # Delayed import to avoid circular dependency
        import lov

        key = event.key.upper()

        if key == "R":
            self._read_books()
        elif key == "S":
            self._study_combat()
        elif key == "T":
            self._talk_to_barak()
        elif key == "L":
            self.app.pop_screen()
        elif key == "?":
            self.notify("R = Read, S = Study, T = Talk, L = Leave")

    def _read_books(self):
        """Read ancient books for intelligence boost"""
        import lov

        books = [
            {"title": "Ancient Mysteries", "boost": 1, "effect": "intelligence"},
            {"title": "Combat Tactics", "boost": 2, "effect": "experience"},
            {"title": "Arcane Knowledge", "boost": 1, "effect": "intelligence"},
            {"title": "Mystical Arts", "boost": 1, "effect": "intelligence"},
            {"title": "Strategic Warfare", "boost": 3, "effect": "experience"},
        ]

        book = random.choice(books)

        if book['effect'] == 'intelligence':
            lov.current_player.intelligence += book['boost']
        elif book['effect'] == 'experience':
            lov.current_player.experience += book['boost'] * 10

        self.notify(f"You read '{book['title']}' and gain {book['boost']} {book['effect']}!")
        lov.game_db.save_player(lov.current_player)

    def _study_combat(self):
        """Study combat techniques for random stat boost"""
        import lov

        stats = ['strength', 'defense', 'charm']
        chosen_stat = random.choice(stats)
        boost = random.randint(1, 2)

        if chosen_stat == 'strength':
            lov.current_player.attack_power += boost
            self.notify(f"Your combat prowess improves! (+{boost} Strength)")
        elif chosen_stat == 'defense':
            lov.current_player.defense_power += boost
            self.notify(f"Your stance improves! (+{boost} Defense)")
        elif chosen_stat == 'charm':
            lov.current_player.charm += boost
            self.notify(f"Your confidence grows! (+{boost} Charm)")

        lov.game_db.save_player(lov.current_player)

    def _talk_to_barak(self):
        """Talk to Barak for local lore and hints"""
        import lov

        lore_messages = [
            "Barak shares ancient wisdom about the mystical arts.",
            "He tells you of hidden treasures in distant lands.",
            "Barak speaks of legendary warriors who came before.",
            "He hints at secret techniques for combat mastery.",
            "Barak reveals knowledge of magical creatures in the forest.",
            "He explains the properties of rare gems and metals.",
        ]

        message = random.choice(lore_messages)
        self.notify(message)

        # 20% chance for bonus reward
        if random.random() < 0.20:
            reward_type = random.choice(['gold', 'gems', 'intelligence'])
            if reward_type == 'gold':
                bonus = random.randint(10, 50)
                lov.current_player.gold += bonus
                self.notify(f"Barak gifts you {bonus} gold for your attention!")
            elif reward_type == 'gems':
                lov.current_player.gems += 1
                self.notify("Barak gives you a rare gem!")
            elif reward_type == 'intelligence':
                lov.current_player.intelligence += 1
                self.notify("Your understanding deepens! (+1 Intelligence)")

        lov.game_db.save_player(lov.current_player)
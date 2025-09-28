"""
Barak's House IGM for Legend of the Obsidian Vault
Starting from exact working test_screen.py code
"""
import datetime
import random
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static
from textual import events


class BarakHouseScreen(Screen):
    """Barak's House - Starting minimal"""

    def __init__(self):
        super().__init__()
        self.test_mode = True

    def compose(self) -> ComposeResult:
        # Delayed import to avoid circular dependency
        import lov

        # Beautiful Barak's House ASCII Art Header
        yield Static("        ✦ BARAK'S HOUSE OF KNOWLEDGE ✦", classes="barak-title")
        yield Static("    ╔══════════════════════════════════════════════╗", classes="barak-border")
        yield Static("    ║  📚    🏠    📖    📜    ✨    📚    🏠  ║", classes="barak-decoration")
        yield Static("    ║                                              ║", classes="barak-border")
        yield Static("    ║     「 Scholar's Sanctuary & Learning Den 」  ║", classes="barak-banner")
        yield Static("    ║                                              ║", classes="barak-border")
        yield Static("    ║   📚 Ancient Tomes    🎓 Knowledge Arts     ║", classes="barak-decoration")
        yield Static("    ║   📖 Study Halls      ⚔️ Combat Training    ║", classes="barak-decoration")
        yield Static("    ║   📜 Sage Wisdom      💰 Scholar's Rewards  ║", classes="barak-decoration")
        yield Static("    ╚══════════════════════════════════════════════╝", classes="barak-border")
        yield Static("═" * 52, classes="barak-decoration")

        # Two blank lines below header
        yield Static("")
        yield Static("")

        # Welcome content
        yield Static("Welcome to Barak's House, where knowledge and fortune intertwine.", classes="barak-content")
        yield Static("The scholarly atmosphere is thick with the scent of ancient parchments.", classes="barak-content")
        yield Static("")

        # Simple welcome message - no player data access
        yield Static("Barak greets you with scholarly enthusiasm.", classes="barak-content")
        yield Static("")

        # Available actions with beautiful formatting
        yield Static("═══ AVAILABLE ACTIONS ═══", classes="barak-content")
        yield Static("(R)ead ancient books - Gain INT, experience, or skill points", classes="barak-content")
        yield Static("(S)tudy combat techniques - Gain +1-2 STR/DEF/CHARM randomly", classes="barak-content")
        yield Static("(T)alk to Barak - Free lore + chance for bonus rewards", classes="barak-content")
        yield Static("")
        yield Static("(L)eave house", classes="barak-content")

        # One blank line before status
        yield Static("")

        # Player status line - only safe attributes
        hp_text = f"({lov.current_player.hitpoints} of {lov.current_player.max_hitpoints})"
        status_line = f"HitPoints: {hp_text}  Gold: {lov.current_player.gold}"
        yield Static(status_line, classes="barak-status")

        # One blank line before command area
        yield Static("")

        # Command prompt area with enhanced styling
        now = datetime.datetime.now()
        time_str = f"{now.hour:02d}:{now.minute:02d}"

        # Location and commands
        location_commands = "Barak's House (R,S,T,L)  (? for menu)"
        yield Static(location_commands, classes="barak-location-commands")

        # Command prompt with time and cursor
        yield Static(f"Your command, {lov.current_player.name}? [{time_str}]: █", classes="barak-prompt")

    def on_key(self, event: events.Key) -> None:
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
        """Read ancient books - safe version"""
        books = [
            "Ancient Mysteries",
            "Combat Tactics",
            "Arcane Knowledge",
            "Mystical Arts",
            "Strategic Warfare"
        ]
        import random
        book = random.choice(books)
        self.notify(f"You read '{book}' and feel wiser! (+1 Intelligence)")

    def _study_combat(self):
        """Study combat techniques - safe version"""
        techniques = [
            "sword techniques",
            "defensive stances",
            "charm training",
            "battle strategy",
            "warrior meditation"
        ]
        import random
        technique = random.choice(techniques)
        self.notify(f"You practice {technique} and improve your skills!")

    def _talk_to_barak(self):
        """Talk to Barak - safe version"""
        lore = [
            "Barak shares ancient wisdom about the mystical arts.",
            "He tells you of hidden treasures in distant lands.",
            "Barak speaks of legendary warriors who came before.",
            "He hints at secret techniques for combat mastery.",
            "Barak reveals knowledge of magical creatures.",
            "He explains the properties of rare gems and metals."
        ]
        import random
        message = random.choice(lore)
        self.notify(message)
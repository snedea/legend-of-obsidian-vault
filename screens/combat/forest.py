"""
Forest exploration screen for Legend of the Obsidian Vault
"""
import datetime
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static
from textual import events


class ForestScreen(Screen):
    """Forest exploration and combat - Authentic LORD BBS Style"""

    def compose(self) -> ComposeResult:
        # Delayed import to avoid circular dependency
        import lov

        # Colored Forest ASCII Art Header (8 lines)
        yield Static("        ░░░  ✦ THE MYSTICAL FOREST OF KNOWLEDGE ✦  ░░░", classes="forest-title")
        yield Static("    ▄▄██▄▄     ▄▄██▄▄     ▄▄██▄▄     ▄▄██▄▄     ▄▄██▄▄", classes="forest-trees")
        yield Static("   ███████    ███████    ███████    ███████    ███████", classes="forest-trees")
        yield Static("  ██▀▀▀▀▀██  ██▀▀▀▀▀██  ██▀▀▀▀▀██  ██▀▀▀▀▀██  ██▀▀▀▀▀██", classes="forest-trees")
        yield Static("     ║║║        ║║║        ║║║        ║║║        ║║║", classes="forest-trunks")
        yield Static("     ║║║        ║║║        ║║║        ║║║        ║║║", classes="forest-trunks")
        yield Static("  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░", classes="forest-mist")
        yield Static("═══════════════════════════════════════════════════════════════════════════", classes="forest-ground")

        # Two blank lines below header
        yield Static("")
        yield Static("")

        # Scene description (exact LORD text)
        yield Static("The murky forest stands before you - a giant maw of gloomy darkness ever beckoning.", classes="forest-content")

        # One blank line before actions menu
        yield Static("")

        # Player actions menu (exact LORD format)
        yield Static("(L)ook for something to kill", classes="forest-content")
        yield Static("(H)ealers hut", classes="forest-content")
        yield Static("(R)eturn to town", classes="forest-content")

        # One blank line before status line
        yield Static("")

        # Player status line (HitPoints and Fights in green, Gold in yellow, Gems in green)
        hp_text = f"({lov.current_player.hitpoints} of {lov.current_player.max_hitpoints})"
        status_line = f"HitPoints: {hp_text}  Fights: {lov.current_player.forest_fights}  Gold: {lov.current_player.gold}  Gems: {lov.current_player.gems}"
        yield Static(status_line, classes="forest-status")

        # One blank line before command area
        yield Static("")

        # Command prompt area (two lines)
        now = datetime.datetime.now()
        time_str = f"{now.hour:02d}:{now.minute:02d}"

        # Line 1: Location and commands on same line (magenta + green)
        location_commands = f"The Forest (L,H,R,Q)  (? for menu)"
        yield Static(location_commands, classes="forest-location-commands")

        # Line 2: Command prompt with time and cursor (cyan with white cursor)
        yield Static(f"Your command, {lov.current_player.name}? [{time_str}]: █", classes="forest-prompt")

    def on_key(self, event: events.Key) -> None:
        # Delayed import to avoid circular dependency
        import lov

        key = event.key.upper()

        if lov.current_player.forest_fights <= 0:
            self.app.pop_screen()
            return

        if key == "L" or key == "E":
            # Look for something to kill (enter combat)
            from .combat import CombatScreen
            self.app.push_screen(CombatScreen())
        elif key == "H":
            # Healers hut - navigate to healer screen
            from screens.town.healer import HealerScreen
            self.app.push_screen(HealerScreen())
        elif key == "R" or key == "Q":
            self.app.pop_screen()
        elif key == "?":
            # Show help menu
            self.notify("L = Look for enemies, H = Healer's hut, R = Return to town, Q = Quit")
"""
Legend of the Obsidian Vault (LOV)
EXACT Legend of the Red Dragon clone with Obsidian vault integration
"""
import asyncio
import random
from pathlib import Path
from typing import List
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, Grid, VerticalScroll
from textual.widgets import Header, Footer, Static, Button, Input, Label
from textual.screen import Screen
from textual import events
from textual.binding import Binding

from game_data import Character, GameDatabase, BBS_COLORS, WEAPONS, ARMOR, CLASS_TYPES, INN_ROOM_COSTS, BRIBE_COSTS, RESERVED_NAMES
from obsidian import vault

# Import combat screens
from screens.combat.forest import ForestScreen
from screens.combat.combat import CombatScreen
from screens.combat.quiz import QuizScreen

# Import town screens
from screens.town.townsquare import TownSquareScreen
from screens.town.stats import StatsScreen
from screens.town.weapons import WeaponsScreen
from screens.town.inn import InnScreen
from screens.town.barroom import BarRoomScreen
from screens.town.gem_trading import GemTradingScreen
from screens.town.armor import ArmorScreen
from screens.town.bank import BankScreen
from screens.town.healer import HealerScreen

# Import character screens
from screens.character.creation import CharacterCreationScreen
from screens.character.selection import PlayerSelectScreen


# Global game state
current_player = None
game_db = GameDatabase()

class LordApp(App):
    """Main LORD application with authentic BBS styling"""

    CSS = """
    Screen {
        background: black;
        color: ansi_bright_white;
    }

    .header {
        background: black;
        color: ansi_bright_yellow;
        text-style: bold;
        height: 1;
        text-align: center;
    }

    .separator {
        background: black;
        color: ansi_bright_white;
        height: 1;
    }

    .menu-btn {
        background: ansi_blue;
        border: solid ansi_bright_white;
        color: ansi_bright_white;
        text-align: center;
        padding: 1;
        margin: 1;
        height: 3;
        min-height: 3;
        width: 50;
    }

    .menu-btn:hover {
        background: ansi_bright_blue;
        color: ansi_bright_yellow;
        border: solid ansi_bright_yellow;
    }

    .menu-btn:focus {
        background: ansi_bright_blue;
        color: ansi_bright_yellow;
        border: solid ansi_bright_yellow;
    }

    .menu-key {
        color: ansi_bright_yellow;
        text-style: bold;
    }

    .main-border {
        border: thick ansi_bright_red;
        background: black;
        padding: 2;
        height: 1fr;
        border-title-color: ansi_bright_yellow;
        border-title-style: bold;
        border-subtitle-color: ansi_bright_cyan;
        border-subtitle-style: italic;
    }

    .prompt {
        background: black;
        color: ansi_bright_green;
        height: 1;
    }

    .stats {
        background: black;
        color: ansi_bright_cyan;
    }

    .enemy {
        color: ansi_bright_red;
        text-style: bold;
    }

    .narrative {
        color: ansi_bright_magenta;
        text-style: italic;
    }

    .player {
        color: ansi_bright_green;
        text-style: bold;
    }

    .gold {
        color: ansi_bright_yellow;
    }

    .content {
        background: black;
        color: ansi_bright_white;
        padding: 1;
    }

    Input {
        background: black;
        color: ansi_bright_green;
        border: none;
    }


    Input:focus {
        border: solid ansi_bright_yellow;
    }

    .town-scroll {
        max-height: 20;
        scrollbar-background: ansi_red;
        scrollbar-color: ansi_bright_red;
        scrollbar-size: 1 1;
    }

    .char-scroll {
        max-height: 15;
        scrollbar-background: ansi_red;
        scrollbar-color: ansi_bright_red;
        scrollbar-size: 1 1;
    }
    .forest-header {
        background: black;
        color: ansi_white;
        text-align: left;
        height: 1;
    }
    .forest-title {
        background: ansi_white;
        color: black;
        text-style: bold;
    }
    .forest-healthbar {
        background: ansi_bright_green;
        color: ansi_bright_green;
        height: 1;
    }
    .forest-trees {
        background: black;
        color: ansi_bright_green;
        height: 1;
    }
    .forest-content {
        background: black;
        color: ansi_bright_green;
        text-align: left;
    }
    .forest-status {
        background: black;
        color: ansi_bright_green;
        text-align: left;
        height: 1;
    }
    .forest-status-value {
        color: ansi_bright_yellow;
    }
    .forest-location {
        background: black;
        color: ansi_magenta;
        text-align: left;
        height: 1;
    }
    .forest-prompt {
        background: black;
        color: ansi_bright_cyan;
        text-align: left;
        height: 1;
    }
    .forest-commands {
        background: black;
        color: ansi_bright_green;
        text-align: left;
        height: 1;
    }
    .forest-location-commands {
        background: black;
        color: ansi_magenta;
        text-align: left;
        height: 1;
    }
    .bbs-header {
        background: black;
        color: ansi_bright_cyan;
        text-align: center;
        height: 1;
    }
    CombatScreen {
        background: black;
        color: ansi_bright_white;
    }

    /* Combat Screen Styling - Final Fantasy Style */
    .enemy-panel {
        background: ansi_red;
        color: ansi_bright_white;
        border: solid ansi_bright_red;
        padding: 1;
        margin: 1;
    }

    .player-panel {
        background: ansi_green;
        color: ansi_bright_white;
        border: solid ansi_bright_green;
        padding: 1;
        margin: 1;
    }

    .enemy-stats {
        color: ansi_bright_red;
        text-style: bold;
    }

    .player-stats {
        color: ansi_bright_green;
        text-style: bold;
    }

    .enemy-hp-bar {
        color: ansi_bright_red;
        background: ansi_black;
        text-style: bold;
    }

    .player-hp-bar {
        color: ansi_bright_green;
        background: ansi_black;
        text-style: bold;
    }

    .combat-commands {
        background: black;
        color: ansi_bright_yellow;
        text-align: center;
        text-style: bold;
        padding: 1;
    }

    .combat-log {
        color: ansi_bright_cyan;
        background: black;
        padding: 1;
    }

    .combat-panel-border {
        color: ansi_bright_white;
        background: black;
    }

    /* Forest ASCII Art Colors */
    .forest-trees {
        color: ansi_bright_green;
        background: black;
        text-style: bold;
    }

    .forest-trunks {
        color: ansi_yellow;
        background: black;
        text-style: bold;
    }

    .forest-sky {
        color: ansi_bright_cyan;
        background: black;
    }

    .forest-mist {
        color: ansi_bright_white;
        background: black;
    }

    .forest-title {
        color: ansi_bright_yellow;
        background: black;
        text-style: bold;
    }

    .forest-ground {
        color: ansi_green;
        background: black;
    }

    /* Armor Shop ASCII Art Colors */
    .armor-shield {
        color: ansi_bright_white;
        background: black;
        text-style: bold;
    }

    .armor-swords {
        color: ansi_yellow;
        background: black;
        text-style: bold;
    }

    .armor-banner {
        color: ansi_bright_yellow;
        background: black;
        text-style: bold;
    }

    .armor-decoration {
        color: ansi_cyan;
        background: black;
        text-style: bold;
    }

    .armor-border {
        color: ansi_white;
        background: black;
    }

    /* LORD Cavern Styles */
    .cavern-title {
        color: ansi_bright_yellow;
        background: black;
        text-style: bold;
    }

    .cavern-cave {
        color: ansi_yellow;
        background: black;
        text-style: bold;
    }

    .cavern-shadow {
        color: ansi_white;
        background: black;
    }

    .cavern-ground {
        color: ansi_green;
        background: black;
    }

    .cavern-content {
        color: ansi_bright_green;
        background: black;
    }

    .cavern-status {
        color: ansi_bright_green;
        background: black;
        text-style: bold;
    }

    .cavern-location-commands {
        color: ansi_magenta;
        background: black;
    }

    .cavern-prompt {
        color: ansi_bright_cyan;
        background: black;
    }

    /* Barak's House Styles */
    .barak-title {
        color: ansi_bright_yellow;
        background: black;
        text-style: bold;
    }

    .barak-border {
        color: ansi_white;
        background: black;
    }

    .barak-decoration {
        color: ansi_bright_cyan;
        background: black;
    }

    .barak-banner {
        color: ansi_bright_yellow;
        background: black;
        text-style: bold;
    }

    .barak-content {
        color: ansi_bright_green;
        background: black;
    }

    .barak-status {
        color: ansi_bright_green;
        background: black;
        text-style: bold;
    }

    .barak-location-commands {
        color: ansi_magenta;
        background: black;
    }

    .barak-prompt {
        color: ansi_bright_cyan;
        background: black;
    }

    /* Other Places Menu Styles */
    .other-title {
        color: ansi_bright_yellow;
        background: black;
        text-style: bold;
    }

    .other-border {
        color: ansi_white;
        background: black;
    }

    .other-subtitle {
        color: ansi_bright_cyan;
        background: black;
        text-style: italic;
    }

    .other-content {
        color: ansi_bright_green;
        background: black;
    }

    .other-coming-soon {
        color: ansi_bright_black;
        background: black;
        text-style: italic;
    }

    .other-status {
        color: ansi_bright_green;
        background: black;
        text-style: bold;
    }

    .other-location-commands {
        color: ansi_magenta;
        background: black;
    }

    .other-prompt {
        color: ansi_bright_cyan;
        background: black;
    }

    /* Fairy Garden Styles */
    .fairy-title {
        color: ansi_bright_magenta;
        background: black;
        text-style: bold;
    }

    .fairy-decoration {
        color: ansi_bright_yellow;
        background: black;
    }

    .fairy-border {
        color: ansi_bright_cyan;
        background: black;
    }

    .fairy-banner {
        color: ansi_bright_magenta;
        background: black;
        text-style: bold;
    }

    .fairy-ground {
        color: ansi_green;
        background: black;
    }

    .fairy-content {
        color: ansi_bright_green;
        background: black;
    }

    .fairy-status {
        color: ansi_bright_green;
        background: black;
        text-style: bold;
    }

    .fairy-location-commands {
        color: ansi_magenta;
        background: black;
    }

    .fairy-prompt {
        color: ansi_bright_cyan;
        background: black;
    }

    /* Xenon's Storage Styles */
    .xenon-title {
        color: ansi_bright_yellow;
        background: black;
        text-style: bold;
    }

    .xenon-border {
        color: ansi_bright_white;
        background: black;
    }

    .xenon-decoration {
        color: ansi_bright_cyan;
        background: black;
    }

    .xenon-ground {
        color: ansi_green;
        background: black;
    }

    .xenon-content {
        color: ansi_bright_green;
        background: black;
    }

    .xenon-status {
        color: ansi_bright_green;
        background: black;
        text-style: bold;
    }

    .xenon-location-commands {
        color: ansi_magenta;
        background: black;
    }

    .xenon-prompt {
        color: ansi_bright_cyan;
        background: black;
    }

    /* WereWolf Den Styles */
    .werewolf-title {
        color: ansi_bright_red;
        background: black;
        text-style: bold;
    }

    .werewolf-decoration {
        color: ansi_bright_yellow;
        background: black;
    }

    .werewolf-border {
        color: ansi_bright_white;
        background: black;
    }

    .werewolf-banner {
        color: ansi_bright_red;
        background: black;
        text-style: bold;
    }

    .werewolf-ground {
        color: ansi_red;
        background: black;
    }

    .werewolf-content {
        color: ansi_bright_green;
        background: black;
    }

    .werewolf-status {
        color: ansi_bright_green;
        background: black;
        text-style: bold;
    }

    .werewolf-location-commands {
        color: ansi_magenta;
        background: black;
    }

    .werewolf-prompt {
        color: ansi_bright_cyan;
        background: black;
    }

    /* Gateway Portal Styles */
    .gateway-title {
        color: ansi_bright_magenta;
        background: black;
        text-style: bold;
    }

    .gateway-decoration {
        color: ansi_bright_cyan;
        background: black;
    }

    .gateway-border {
        color: ansi_bright_white;
        background: black;
    }

    .gateway-banner {
        color: ansi_bright_magenta;
        background: black;
        text-style: bold;
    }

    .gateway-ground {
        color: ansi_blue;
        background: black;
    }

    .gateway-content {
        color: ansi_bright_green;
        background: black;
    }

    .gateway-status {
        color: ansi_bright_green;
        background: black;
        text-style: bold;
    }

    .gateway-location-commands {
        color: ansi_magenta;
        background: black;
    }

    .gateway-prompt {
        color: ansi_bright_cyan;
        background: black;
    }
    """

    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit", priority=True),
    ]

    def on_mount(self) -> None:
        """Initialize the app"""
        self.title = "Legend of the Obsidian Vault"

        # Initialize AI system in background using threading
        try:
            import threading
            from brainbot import initialize_ai
            ai_thread = threading.Thread(target=initialize_ai, daemon=True)
            ai_thread.start()
        except Exception as e:
            print(f"AI initialization failed: {e}")

        self.push_screen(StartScreen())

class StartScreen(Screen):
    """Opening screen - character creation or login"""

    # Make sure this screen can receive focus
    can_focus = True

    def compose(self) -> ComposeResult:
        with Container(classes="main-border") as container:
            container.border_title = "⚔️  LEGEND OF OBSIDIAN VAULT  ⚔️"
            container.border_subtitle = "✨ Enter the Realm of Adventure ✨"

            yield Static("The Legend of the Obsidian Vault", classes="header")
            yield Static("=-" * 30, classes="separator")
            yield Static("")
            yield Static("** Welcome to the realm, new warrior! **", classes="content")
            yield Static("")
            yield Static("Select an option (click buttons or press keys):")
            yield Static("")

            # Add clickable buttons as backup in 2-column layout
            with Horizontal():
                with Vertical():
                    yield Button("(N) Create New Character", id="new_char")
                    yield Button("(E) Load Existing Character", id="existing_char")
                    yield Button("(V) Configure Vault Settings", id="vault_settings")
                with Vertical():
                    yield Button("(B) BrainBot AI Settings", id="ai_settings")
                    yield Button("(Q) Quit Game", id="quit_game")

            yield Static("")
            yield Static("Press keys: N, E, V, B, Q or click buttons above", classes="prompt")

            # Padding to fill screen height
            for _ in range(15):
                yield Static("")

    def on_mount(self) -> None:
        """Ensure this screen gets focus for keyboard input"""
        self.focus()
        # Force layout refresh to fix initial height calculation
        self.refresh(layout=True)
        self.call_after_refresh(lambda: self.refresh(layout=True))

    def on_key(self, event: events.Key) -> None:
        """Handle key presses"""
        key = event.key.upper()

        try:
            if key == "N" or event.key == "enter":
                self.notify("Creating new character...")
                self.app.push_screen(CharacterCreationScreen())
            elif key == "E":
                self.app.push_screen(PlayerSelectScreen())
            elif key == "V":
                self.notify("Opening vault settings...")
                self.app.push_screen(VaultSettingsScreen())
            elif key == "B":
                self.notify("Opening AI settings...")
                self.app.push_screen(AISettingsScreen())
            elif key == "Q":
                self.app.exit()
        except Exception as e:
            self.notify(f"Error: {str(e)[:50]}")
            # Still try to continue
            pass

    def on_click(self, event) -> None:
        """Handle mouse clicks as fallback"""
        self.notify("Mouse click detected! Press N for new character")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button clicks as backup to keyboard input"""
        button_id = event.button.id

        try:
            if button_id == "new_char":
                self.notify("Creating new character...")
                self.app.push_screen(CharacterCreationScreen())
            elif button_id == "existing_char":
                self.app.push_screen(PlayerSelectScreen())
            elif button_id == "vault_settings":
                self.notify("Opening vault settings...")
                self.app.push_screen(VaultSettingsScreen())
            elif button_id == "ai_settings":
                self.notify("Opening AI settings...")
                self.app.push_screen(AISettingsScreen())
            elif button_id == "quit_game":
                self.app.exit()
        except Exception as e:
            self.notify(f"Button error: {str(e)[:50]}")
            pass

class VaultSettingsScreen(Screen):
    """Configure Obsidian vault path"""

    def compose(self) -> ComposeResult:
        yield Static("Obsidian Vault Configuration", classes="header")
        yield Static("=-" * 30, classes="separator")
        yield Static("")

        current_path = vault.get_vault_path()
        yield Static(f"Current vault: {current_path}")
        yield Static("")
        yield Static("Enter path to your Obsidian vault (or press Enter to auto-detect):")
        yield Input(placeholder="e.g., /Users/name/Documents/Obsidian Vault")
        yield Static("")
        yield Static("(Enter) to save, (Q) or (Escape) to go back")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle vault path input"""
        path = event.value.strip()

        if not path:
            # Try auto-detect
            new_vault = vault.find_vault()
            if new_vault:
                vault.vault_path = new_vault
                self.notify(f"Auto-detected vault: {new_vault}")
            else:
                self.notify("No vault found. Please specify path manually.")
        else:
            if vault.set_vault_path(path):
                self.notify(f"Vault set to: {path}")
            else:
                self.notify("Invalid path. Please try again.")
                return

        self.app.pop_screen()

    def on_key(self, event: events.Key) -> None:
        if event.key.upper() == "Q" or event.key == "escape":
            self.app.pop_screen()

class AISettingsScreen(Screen):
    """Configure BrainBot AI settings"""

    def compose(self) -> ComposeResult:
        yield Static("BrainBot AI Configuration", classes="header")
        yield Static("=-" * 30, classes="separator")
        yield Static("")

        # Check AI status
        try:
            from brainbot import is_ai_available
            ai_status = "🧠 Connected" if is_ai_available() else "❌ Disconnected"
        except ImportError:
            ai_status = "📦 Not installed"

        yield Static(f"AI Status: {ai_status}")
        yield Static("")
        yield Static("BrainBot provides:")
        yield Static("  • Intelligent quiz questions from your notes")
        yield Static("  • Better answer validation (semantic matching)")
        yield Static("  • Dynamic enemy backstories")
        yield Static("  • Enhanced combat dialog")
        yield Static("")
        yield Static("AI Setup:")
        yield Static("  • Dependencies are auto-installed on first run")
        yield Static("  • AI models download automatically when needed")
        yield Static("  • No manual configuration required")
        yield Static("")
        yield Static("The game works perfectly with or without AI")
        yield Static("")
        yield Static("(T)est AI Connection")
        yield Static("(Q) Back to main menu")

    def on_key(self, event: events.Key) -> None:
        key = event.key.upper()
        if key == "Q":
            self.app.pop_screen()
        elif key == "T":
            self._test_ai_connection()

    def _test_ai_connection(self):
        """Test AI connection"""
        try:
            from brainbot import is_ai_available, initialize_ai, ai_quiz_system

            # Initialize AI if not already done
            initialize_ai()
            self.notify("🔄 Testing AI connection...")

            # Check current status
            status = ai_quiz_system.initialization_status
            if status == "initializing":
                self.notify("⏳ AI initializing, waiting...")

            # Wait up to 5 seconds for initialization
            if is_ai_available(wait_timeout=5.0):
                self.notify("🧠 AI connected successfully!")
            else:
                if status == "failed":
                    self.notify("❌ AI initialization failed - using fallback mode")
                else:
                    self.notify("⏰ AI initialization timeout - using fallback mode")
        except Exception as e:
            self.notify(f"❌ AI test failed: {str(e)[:50]}")



class TurgonsTrainingScreen(Screen):
    """Turgon's Warrior Training - Master progression system"""

    def compose(self) -> ComposeResult:
        from textual.containers import Container

        with Container(classes="main-border") as container:
            container.border_title = "🏛️ TURGON'S TRAINING 🏛️"
            container.border_subtitle = "⚔️ Master Progression ⚔️"

            yield Static("🏛️  Turgon's Warrior Training", classes="header")
            yield Static("=-" * 50, classes="separator")
            yield Static("")

            # Player status
            yield Static(f"Warrior: {current_player.name}")
            yield Static(f"Level: {current_player.level}")
            yield Static(f"Experience: {current_player.experience:,}")
            yield Static("")

            # Check if player can level up
            from game_data import can_level_up, get_next_level_exp, MASTERS

            if can_level_up(current_player):
                next_level = current_player.level + 1
                if next_level <= 12 and next_level in MASTERS:
                    master = MASTERS[next_level]
                    yield Static(f"🎯 Ready to challenge {master['name']} for Level {next_level}!")
                    yield Static("")
                    yield Static(f"Master {master['name']} awaits your challenge...")
                    yield Static(f"Weapon to earn: {master['weapon']}")
                    yield Static("")
                    yield Button(f"(C)hallenge {master['name']}", id="challenge_master")
                else:
                    yield Static("🏆 You have mastered all training levels!")
                    yield Static("Seek the Red Dragon to prove your ultimate worth!")
            else:
                # Show experience needed
                next_level = current_player.level + 1
                if next_level <= 12:
                    exp_needed = get_next_level_exp(current_player.level) - current_player.experience
                    yield Static(f"Experience needed for Level {next_level}: {exp_needed:,}")
                else:
                    yield Static("🏆 Maximum level achieved!")

            yield Static("")
            yield Static("🗡️  Master Hall of Fame:")
            yield Static("=-" * 30)

            # Show defeated masters
            for level in range(1, min(current_player.level + 1, 13)):
                if level in MASTERS:
                    master = MASTERS[level]
                    status = "✅ DEFEATED" if level <= current_player.level else "❌ Awaiting"
                    yield Static(f"Level {level:2d}: {master['name']:<15} - {master['weapon']:<20} {status}")

            yield Static("")
            yield Button("(Q) Return to town", id="return_town")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle master challenge"""
        if event.button.id == "challenge_master":
            self._challenge_master()
        elif event.button.id == "return_town":
            self.app.pop_screen()

    def _challenge_master(self):
        """Challenge the next master for level up"""
        from game_data import can_level_up, MASTERS

        if not can_level_up(current_player):
            self.notify("You need more experience to challenge a master!")
            return

        next_level = current_player.level + 1
        if next_level > 12 or next_level not in MASTERS:
            self.notify("No more masters to challenge!")
            return

        master = MASTERS[next_level]

        # Show master dialogue and challenge
        self.app.push_screen(MasterChallengeScreen(next_level, master))

    def on_key(self, event: events.Key) -> None:
        key = event.key.upper()
        if key == "Q":
            self.app.pop_screen()
        elif key == "C":
            self._challenge_master()

class MasterChallengeScreen(Screen):
    """Individual master challenge screen with dialogue"""

    def __init__(self, level: int, master: dict):
        super().__init__()
        self.level = level
        self.master = master

    def compose(self) -> ComposeResult:
        from textual.containers import Container

        with Container(classes="main-border") as container:
            container.border_title = "⚔️ MASTER CHALLENGE ⚔️"
            container.border_subtitle = f"🏆 {self.master['name']} - Level {self.level} 🏆"

            yield Static(f"⚔️  Master {self.master['name']} - Level {self.level}", classes="header")
            yield Static("=-" * 50, classes="separator")
            yield Static("")

            # Master greeting
            yield Static(f'Master {self.master["name"]} says:')
            yield Static(f'"{self.master["greeting"]}"')
            yield Static("")

            yield Static("Do you wish to challenge this master?")
            yield Static("")
            yield Button("(Y)es, I'm ready to fight!", id="accept_challenge")
            yield Button("(N)o, I need more training", id="decline_challenge")
            yield Static("")
            yield Button("(Q) Return to training hall", id="return_training")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "accept_challenge":
            self._start_master_combat()
        elif event.button.id == "decline_challenge":
            self.app.pop_screen()
        elif event.button.id == "return_training":
            self.app.pop_screen()

    def _start_master_combat(self):
        """Start combat with the master"""
        from game_data import create_master_enemy

        # Create master as enemy
        master_enemy = create_master_enemy(self.level, self.master)

        # Start combat screen
        combat_screen = CombatScreen()
        combat_screen.enemy = master_enemy
        combat_screen.is_master_fight = True
        combat_screen.master_level = self.level
        combat_screen.master_data = self.master

        self.app.push_screen(combat_screen)

    def on_key(self, event: events.Key) -> None:
        key = event.key.upper()
        if key == "Q":
            self.app.pop_screen()
        elif key == "Y":
            self._start_master_combat()
        elif key == "N":
            self.app.pop_screen()

class NotesViewerScreen(Screen):
    """Display Obsidian notes and their status in the game"""

    def compose(self) -> ComposeResult:
        from textual.containers import Container
        from textual.widgets import Button

        with Container(classes="main-border") as container:
            container.border_title = "📚 OBSIDIAN VAULT 📚"
            container.border_subtitle = "🗡️ Knowledge Enemies 🗡️"

            yield Static("📚 Notes in the Obsidian Vault", classes="header")
            yield Static("=-" * 50, classes="separator")
            yield Static("")

            # Get vault status
            vault_path = vault.get_vault_path()
            if vault_path == "No vault found":
                yield Static("❌ No Obsidian vault configured")
                yield Static("")
                yield Static("Configure your vault in (V)ault Settings")
            else:
                yield Static(f"📁 Vault: {vault_path}")

                # Try to scan notes
                try:
                    notes = vault.scan_notes(force_rescan=True)

                    # Check AI status
                    ai_status = "❌ Disconnected"
                    try:
                        from brainbot import is_ai_available
                        ai_status = "🧠 Connected" if is_ai_available() else "❌ Disconnected"
                    except ImportError:
                        ai_status = "📦 Not installed"

                    yield Static(f"🤖 AI Status: {ai_status}")
                    yield Static("")

                    if notes:
                        yield Static(f"Found {len(notes)} notes haunting the forest:")
                        yield Static("")

                        # Group notes by difficulty level
                        levels = {}
                        for note in notes[:20]:  # Show first 20
                            level = note.difficulty_level
                            if level not in levels:
                                levels[level] = []
                            levels[level].append(note)

                        for level in sorted(levels.keys()):
                            level_notes = levels[level]
                            yield Static(f"⚔️  Level {level} Enemies ({len(level_notes)} notes):")
                            for note in level_notes[:5]:  # Show first 5 per level
                                age_desc = f"{note.age_days}d old" if note.age_days > 0 else "new"
                                yield Static(f"   • {note.title} ({age_desc})")
                            if len(level_notes) > 5:
                                yield Static(f"   ... and {len(level_notes) - 5} more")
                            yield Static("")

                        if len(notes) > 20:
                            yield Static(f"... and {len(notes) - 20} more notes")
                    else:
                        yield Static("❌ No notes found in vault")
                        yield Static("")
                        yield Static("Add some .md files to your Obsidian vault!")

                except Exception as e:
                    yield Static(f"❌ Error scanning vault: {str(e)[:50]}...")

            yield Static("")
            yield Static("💡 Notes become forest enemies based on age:")
            yield Static("   • Recent (< 7 days) = Level 1-2")
            yield Static("   • Medium (1-3 months) = Level 3-9")
            yield Static("   • Old (3+ months) = Level 10-12")
            yield Static("")
            yield Static("Fight them in the (F)orest to remember their content!")
            yield Static("")
            yield Button("(R)eturn to town", id="return_town")

    def on_button_pressed(self, event) -> None:
        """Handle button presses"""
        if event.button.id == "return_town":
            self.app.pop_screen()

    def on_key(self, event: events.Key) -> None:
        self.app.pop_screen()

class WarriorListScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Static("Warrior List", classes="header")
        yield Static("=-" * 30, classes="separator")
        yield Static("")

        players = game_db.get_all_players()
        for i, player in enumerate(players[:20]):
            status = "Online" if player.alive else "Dead"
            yield Static(f"{i+1:2d}. {player.name:<20} Level {player.level:2d} {status}")

        yield Static("")
        yield Static("Press any key to return...")

    def on_key(self, event: events.Key) -> None:
        self.app.pop_screen()

class HallOfHonoursScreen(Screen):
    """Hall of Honours - Dragon slayers and champions"""

    def compose(self) -> ComposeResult:
        yield Static("🏆 Hall of Honours - Dragon Slayers 🏆", classes="header")
        yield Static("=-" * 60, classes="separator")
        yield Static("")

        # Get all dragon slayers
        from game_data import get_hall_of_honours_entries
        hall_entries = get_hall_of_honours_entries(game_db)

        if not hall_entries:
            yield Static("🐉 No heroes have yet slain the Red Dragon...")
            yield Static("")
            yield Static("The Red Dragon still terrorizes the land, waiting for a")
            yield Static("worthy Level 12 champion to challenge its might!")
            yield Static("")
            yield Static("Only the bravest and strongest warriors dare face")
            yield Static("the ancient terror that has claimed so many lives...")
        else:
            yield Static("⚔️  Heroes who have slain the Red Dragon:")
            yield Static("")

            # Header
            yield Static(f"{'Rank':<5} {'Hero':<15} {'Class':<10} {'Kills':<6} {'Wins':<5} {'First Victory'}")
            yield Static("-" * 65)

            # Show all entries
            for i, (name, class_type, dragon_kills, times_won, hall_entry, level) in enumerate(hall_entries):
                class_name = {
                    'K': 'Death Knight',
                    'M': 'Mystical',
                    'T': 'Thief'
                }.get(class_type, 'Unknown')

                rank = f"#{i+1}"
                kills_text = f"{dragon_kills}🐉"
                wins_text = f"{times_won}👑"

                yield Static(f"{rank:<5} {name:<15} {class_name:<10} {kills_text:<6} {wins_text:<5} {hall_entry}")

            yield Static("")
            yield Static("🏆 Legend:")
            yield Static("   🐉 = Red Dragon kills")
            yield Static("   👑 = Total game victories")
            yield Static("")

            # Show current player's status if they have dragon kills
            if current_player and current_player.dragon_kills > 0:
                yield Static(f"Your record: {current_player.dragon_kills} dragon kills, {current_player.times_won_game} victories")
                yield Static(f"Hall entry: {current_player.hall_of_honours_entry}")

        yield Static("")
        yield Static("The Red Dragon awaits Level 12 champions in the deepest forest...")
        yield Static("")
        yield Static("Press any key to return to town...")

    def on_key(self, event: events.Key) -> None:
        self.app.pop_screen()

def main():
    """Run the game"""
    print("🚀 Starting Legend of the Obsidian Vault...")
    print("🤖 Initializing AI features...")

    # Initialize AI in background using threading
    try:
        import threading
        from brainbot import initialize_ai
        ai_thread = threading.Thread(target=initialize_ai, daemon=True)
        ai_thread.start()
        print("✅ AI initialization started")
    except Exception as e:
        print(f"⚠️  AI initialization failed: {e}")
        print("📝 Quiz questions will use regex fallback")

    # Periodic cache maintenance
    try:
        from simple_cache import periodic_maintenance
        periodic_maintenance()
    except ImportError:
        pass

    app = LordApp()
    app.run()

if __name__ == "__main__":
    main()
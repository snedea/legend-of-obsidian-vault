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

    def __init__(self):
        super().__init__()
        self.command_buffer = ""  # Track typed commands for Jennie codes
        self.in_frog_mode = False  # Track if player is transformed into a frog

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

        # Check if we're in frog mode first
        if self.in_frog_mode:
            self._handle_frog_action(key)
            return

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
        elif key == "C":
            # Hidden LORD Cavern access
            from screens.igm.cavern import CavernScreen
            self.app.push_screen(CavernScreen())
        elif key == "?":
            # Show help menu
            self.notify("L = Look for enemies, H = Healer's hut, R = Return to town, Q = Quit")
            self.notify("Hidden: C = LORD Cavern (mystical exploration)")
        else:
            # Check for Jennie codes or other special commands
            self._handle_command_input(key)

    def _handle_command_input(self, key: str):
        """Handle special command input like Jennie codes"""
        # Delayed import to avoid circular dependency
        import lov

        # Add character to command buffer
        if key.isalpha() and len(self.command_buffer) < 10:
            self.command_buffer += key.lower()
        elif key == "space":
            self.command_buffer += " "
        elif key == "enter":
            self._process_command()
            self.command_buffer = ""
        elif key == "escape":
            self.command_buffer = ""

        # Check if we have "jennie" followed by a space
        if self.command_buffer.startswith("jennie ") and len(self.command_buffer) > 7:
            descriptor = self.command_buffer[7:].strip()
            if descriptor:
                self._process_jennie_code(descriptor)
                self.command_buffer = ""

    def _process_command(self):
        """Process completed command from command buffer"""
        # Delayed import to avoid circular dependency
        import lov

        command = self.command_buffer.strip().lower()

        # Check for other special commands here if needed
        if not command:
            return

        # For now, just clear commands that don't match anything
        self.notify(f"Unknown command: {command}")

    def _process_jennie_code(self, descriptor: str):
        """Process Jennie Garth codes - requires high spirits"""
        # Delayed import to avoid circular dependency
        import lov

        # Check if player is in high spirits
        if lov.current_player.spirit_level != "high":
            self.notify("You must be in high spirits to call upon Jennie!")
            return

        descriptor = descriptor.upper()

        if descriptor == "LADY":
            # $1,000 times level
            gold_reward = 1000 * lov.current_player.level
            lov.current_player.gold += gold_reward
            self.notify(f"Jennie smiles warmly. You receive {gold_reward:,} gold!")

        elif descriptor == "BABE":
            # 1 extra forest fight
            lov.current_player.forest_fights += 1
            self.notify("Jennie winks at you. You feel energized! (+1 Forest Fight)")

        elif descriptor == "SEXY":
            # 1 extra user fight
            lov.current_player.player_fights += 1
            self.notify("Jennie blows you a kiss. You feel more confident! (+1 Player Fight)")

        elif descriptor == "FOXY":
            # 1 extra gem
            lov.current_player.gems += 1
            self.notify("Jennie's eyes sparkle. A mystical gem appears! (+1 Gem)")

        elif descriptor == "HOTT":
            # Receive more hitpoints (temporary)
            temp_hp = lov.current_player.level * 2
            lov.current_player.hitpoints = min(lov.current_player.hitpoints + temp_hp,
                                              lov.current_player.max_hitpoints + temp_hp)
            self.notify(f"Jennie radiates warmth. You feel stronger! (+{temp_hp} temp HP)")

        elif descriptor == "FAIR":
            # Kills your flirt for the day
            lov.current_player.flirted_violet = True
            self.notify("Jennie looks disappointed. Your charm fades for the day.")

        elif descriptor == "DUNG":
            # Turned into a frog
            self.notify("Jennie glares at you angrily!")
            self.notify("'Such rudeness!' she cries. You feel yourself changing...")
            self._frog_transformation()

        elif descriptor == "UGLY":
            # Bitch slapped and kicked out
            self.notify("Jennie gasps in shock!")
            self.notify("'You understand nothing!' (YOU ARE BITCH SLAPPED!)")
            lov.current_player.hitpoints = 1
            lov.game_db.save_player(lov.current_player)
            self.notify("You are thrown from the forest!")
            self.app.pop_screen()

        elif descriptor == "DUMB":
            # Insult
            self.notify("Jennie shakes her head sadly.")
            self.notify("'You idiot. You will NEVER be a useful member of society.'")

        elif descriptor == "STAR":
            # Nothing - obvious statement
            self.notify("'A huge star, infant.' (YOU GET NOTHING, YOU STATED THE OBVIOUS)")

        elif descriptor == "NICE" or descriptor == "DOLL":
            # Nothing
            self.notify("'You do not understand her, my son.'")

        elif descriptor == "COOL":
            # 1 charm point if hitpoints not full
            if lov.current_player.hitpoints < lov.current_player.max_hitpoints:
                lov.current_player.charm += 1
                self.notify("Jennie nods approvingly. You feel more charming! (+1 Charm)")
            else:
                self.notify("Jennie acknowledges you, but you gain nothing.")

        elif descriptor == "GIFT":
            # Use points equal skill points for current class
            from game_data import CLASS_TYPES
            current_skill = lov.current_player.class_type
            if current_skill == "K":  # Death Knight
                lov.current_player.skills_used_today = max(0,
                    CLASS_TYPES["K"]["daily_uses"] - lov.current_player.death_knight_points)
            elif current_skill == "P":  # Mystical
                lov.current_player.skills_used_today = max(0,
                    CLASS_TYPES["P"]["daily_uses"] - lov.current_player.mystical_points)
            elif current_skill == "D":  # Thieving
                lov.current_player.skills_used_today = max(0,
                    CLASS_TYPES["D"]["daily_uses"] - lov.current_player.thieving_points)

            self.notify("Jennie offers you a mystical gift!")
            self.notify("Your skill uses are restored based on your mastery!")

        else:
            self.notify("Jennie looks confused by your description.")

        # Save the player state
        lov.game_db.save_player(lov.current_player)

    def _frog_transformation(self):
        """Handle the frog transformation from DUNG jennie code"""
        self.notify("You have been turned into a frog!")
        self.notify("What do you do?")
        self.notify("(H)op like crazy")
        self.notify("(A)pologize")
        # Set a flag to handle the next keypress for frog actions
        self.in_frog_mode = True

    def _handle_frog_action(self, key: str):
        """Handle actions while transformed into a frog"""
        # Delayed import to avoid circular dependency
        import lov

        if key == "H":
            self.notify("You hop around frantically like a crazy frog!")
            # Stay as frog - could add some random effect here
        elif key == "A":
            self.notify("You croak out an apology.")
            self.notify("Jennie takes pity on you and transforms you back!")
            self.in_frog_mode = False

        lov.game_db.save_player(lov.current_player)
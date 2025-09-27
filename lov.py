"""
Legend of the Obsidian Vault (LOV)
EXACT Legend of the Red Dragon clone with Obsidian vault integration
"""
import asyncio
import random
from pathlib import Path
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, Grid
from textual.widgets import Header, Footer, Static, Button, Input, Label
from textual.screen import Screen
from textual import events
from textual.binding import Binding

from game_data import Character, GameDatabase, BBS_COLORS, WEAPONS, ARMOR, CLASS_TYPES
from obsidian import vault

# Global game state
current_player = None
game_db = GameDatabase()

class LordApp(App):
    """Main LORD application with authentic BBS styling"""

    CSS = """
    Screen {
        background: black;
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
        background: black;
        border: none;
        color: ansi_bright_white;
        text-align: left;
        padding: 0;
        margin: 0;
        height: 1;
        min-height: 1;
    }

    .menu-btn:hover {
        background: ansi_blue;
        color: ansi_bright_white;
    }

    .menu-btn:focus {
        background: ansi_blue;
        color: ansi_bright_white;
    }

    .menu-key {
        color: ansi_bright_yellow;
        text-style: bold;
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
    """

    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit", priority=True),
    ]

    def on_mount(self) -> None:
        """Initialize the app"""
        self.title = "Legend of the Obsidian Vault"

        # Initialize AI system
        try:
            import asyncio
            from brainbot import initialize_ai
            # Run AI initialization in background
            asyncio.create_task(initialize_ai())
        except Exception as e:
            print(f"AI initialization failed: {e}")

        self.push_screen(StartScreen())

class StartScreen(Screen):
    """Opening screen - character creation or login"""

    def compose(self) -> ComposeResult:
        yield Static("The Legend of the Obsidian Vault", classes="header")
        yield Static("=-" * 30, classes="separator")
        yield Static("")
        yield Static("** Welcome to the realm, new warrior! **", classes="content")
        yield Static("")
        yield Static("(N)ew Character")
        yield Static("(E)xisting Character")
        yield Static("(V)ault Settings")
        yield Static("(B)rainBot AI Settings")
        yield Static("(Q)uit")
        yield Static("")
        yield Static("Your command? [N] :", classes="prompt")

    def on_key(self, event: events.Key) -> None:
        """Handle key presses"""
        key = event.key.upper()

        if key == "N" or event.key == "enter":
            self.app.push_screen(CharacterCreationScreen())
        elif key == "E":
            self.app.push_screen(PlayerSelectScreen())
        elif key == "V":
            self.app.push_screen(VaultSettingsScreen())
        elif key == "B":
            self.app.push_screen(AISettingsScreen())
        elif key == "Q":
            self.app.exit()

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
        yield Static("(Enter) to save, (Q) to go back")

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
        if event.key.upper() == "Q":
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
        yield Static("To enable BrainBot:")
        yield Static("  1. Install: pip install aiohttp")
        yield Static("  2. Start BrainBot server on localhost:8080")
        yield Static("  3. Restart the game")
        yield Static("")
        yield Static("The game works perfectly without AI (fallback mode)")
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
        """Test BrainBot connection"""
        try:
            import asyncio
            from brainbot import ai_quiz_system

            async def test_connection():
                await ai_quiz_system.initialize()
                return ai_quiz_system.ai_available

            # Run the test
            result = asyncio.run(test_connection())
            if result:
                self.notify("🧠 BrainBot connected successfully!")
            else:
                self.notify("❌ BrainBot connection failed")
        except Exception as e:
            self.notify(f"❌ AI test failed: {str(e)[:50]}")

class CharacterCreationScreen(Screen):
    """Character creation with EXACT LORD flow"""

    def __init__(self):
        super().__init__()
        self.step = "name"
        self.new_character = Character()

    def compose(self) -> ComposeResult:
        yield Static("Character Creation", classes="header")
        yield Static("=-" * 30, classes="separator")
        yield Static("")
        yield Static("What would you like as an alias?", id="content")
        yield Static("")
        yield Static("Name: ", id="prompt")
        yield Input(id="input")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle character creation steps"""
        value = event.value.strip()

        if self.step == "name":
            if not value or len(value) > 20:
                self.notify("Name must be 1-20 characters")
                return

            # Check if name exists
            if game_db.load_player(value):
                self.notify("Name already exists. Choose another.")
                return

            self.new_character.name = value
            self.step = "gender"
            self._update_gender_prompt()

        elif self.step == "confirm_name":
            confirm = value.upper() if value else "Y"
            if confirm == "Y":
                self.step = "gender"
                self._update_gender_selection()
            elif confirm == "N":
                self.step = "name"
                self.query_one("#content").update("What would you like as an alias?")
                self.query_one("#prompt").update("Name: ")
                self.query_one("#input").value = ""
            else:
                self.notify("Enter Y or N")
                return

        elif self.step == "gender":
            gender = value.upper() if value else "M"
            if gender not in ["M", "F"]:
                self.notify("Enter M or F")
                return

            self.new_character.gender = gender
            if gender == "M":
                self.query_one("#prompt").update("Then don't be wearing any dresses, eh.")
            else:
                self.query_one("#prompt").update("Hmmm, well we'll try to watch our language then.")

            self.step = "class"
            self._update_class_prompt()

        elif self.step == "class":
            class_choice = value.upper() if value else "K"
            if class_choice not in ["K", "P", "D"]:
                self.notify("Enter K, P, or D")
                return

            self.new_character.class_type = class_choice
            self._finish_creation()

    def _update_gender_prompt(self):
        """Update to name confirmation"""
        self.query_one("#prompt").update(f"{self.new_character.name}? [Y] :")
        self.query_one("#input").value = "Y"

        # Add confirmation step
        self.step = "confirm_name"

    def _update_gender_selection(self):
        """Update to gender selection"""
        self.query_one("#content").update("And your gender?  (M/F) [M]:")
        self.query_one("#prompt").update("")
        self.query_one("#input").value = "M"

    def _update_class_prompt(self):
        """Update to class selection"""
        self.query_one("#content").update(
            "As you remember your childhood, you remember...\n\n"
            "(K)illing a lot of woodland creatures.\n"
            "(P)abbling in the mystical forces.\n"
            "(D)ying, cheating, and stealing from the blind.\n\n"
            "Pick one. (K,P,D) :"
        )
        self.query_one("#input").value = ""

    def _finish_creation(self):
        """Complete character creation"""
        global current_player
        current_player = self.new_character
        current_player.daily_reset()
        game_db.save_player(current_player)

        self.app.push_screen(TownSquareScreen())

    def on_key(self, event: events.Key) -> None:
        if event.key.upper() == "Q":
            self.app.pop_screen()

class PlayerSelectScreen(Screen):
    """Select existing character"""

    def compose(self) -> ComposeResult:
        yield Static("Select Character", classes="header")
        yield Static("=-" * 30, classes="separator")
        yield Static("")

        players = game_db.get_all_players()
        if not players:
            yield Static("No characters found. Create a new one.")
            yield Static("")
            yield Static("Press any key to return...")
        else:
            yield Static("Existing Characters:")
            yield Static("")
            for i, player in enumerate(players[:10]):  # Show top 10
                yield Button(
                    f"{i+1}. {player.name} - Level {player.level} {CLASS_TYPES[player.class_type]['name']}",
                    id=f"player_{player.name}"
                )

        yield Static("")
        yield Static("(Q) Back to main menu")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle player selection"""
        if event.button.id and event.button.id.startswith("player_"):
            player_name = event.button.id[7:]  # Remove "player_" prefix
            global current_player
            current_player = game_db.load_player(player_name)
            if current_player:
                current_player.daily_reset()
                game_db.save_player(current_player)
                self.app.push_screen(TownSquareScreen())

    def on_key(self, event: events.Key) -> None:
        if event.key.upper() == "Q" or not game_db.get_all_players():
            self.app.pop_screen()

class TownSquareScreen(Screen):
    """Main town square with all LORD menu options"""

    def compose(self) -> ComposeResult:
        yield Static("The Legend of the Red Dragon - Town Square", classes="header")
        yield Static("=-" * 60, classes="separator")
        yield Static("The streets are crowded, it is difficult to")
        yield Static("push your way through the mob....")
        yield Static("")

        # Two-column layout like original LORD
        with Horizontal():
            with Vertical():
                yield Button("(F)orest", id="forest")
                yield Button("(K)ing Arthurs Weapons", id="weapons")
                yield Button("(H)ealers Hut", id="healer")
                yield Button("(I)nn", id="inn")
                yield Button("(Y)e Old Bank", id="bank")
                yield Button("(W)rite Mail", id="mail")
                yield Button("(C)onjugality List", id="marriage")
                yield Button("(N)otes in the Vault", id="notes")
                yield Button("(X)pert Mode", id="expert")
                yield Button("(P)eople Online", id="online")

            with Vertical():
                yield Button("(S)laughter other players", id="pvp")
                yield Button("(A)bduls Armour", id="armor")
                yield Button("(V)iew your stats", id="stats")
                yield Button("(T)urgons Warrior Training", id="training")
                yield Button("(L)ist Warriors", id="list")
                yield Button("(D)aily News", id="news")
                yield Button("(O)ther Places", id="other")
                yield Button("(M)ake Announcement", id="announce")
                yield Button("(Q)uit to Fields", id="quit")

        yield Static("")
        yield Static("The Town Square  (? for menu)")
        yield Static(f"(F,S,K,A,H,V,R,T,Y,L,W,D,C,N,O,X,M,P,Q)")
        yield Static("")

        # Status line
        if current_player:
            time_left = f"{current_player.forest_fights:02d}:{current_player.player_fights:02d}"
            yield Static(f"Your command, {current_player.name}? [{time_left}] :", classes="prompt")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle menu selections"""
        action = event.button.id

        if action == "forest":
            self.app.push_screen(ForestScreen())
        elif action == "stats":
            self.app.push_screen(StatsScreen())
        elif action == "inn":
            self.app.push_screen(InnScreen())
        elif action == "weapons":
            self.app.push_screen(WeaponsScreen())
        elif action == "armor":
            self.app.push_screen(ArmorScreen())
        elif action == "bank":
            self.app.push_screen(BankScreen())
        elif action == "healer":
            self.app.push_screen(HealerScreen())
        elif action == "list":
            self.app.push_screen(WarriorListScreen())
        elif action == "notes":
            self.app.push_screen(NotesViewerScreen())
        elif action == "quit":
            game_db.save_player(current_player)
            self.app.pop_screen()
        else:
            self.notify(f"{action.title()} - Not yet implemented")

    def on_key(self, event: events.Key) -> None:
        """Handle keyboard shortcuts"""
        key = event.key.upper()

        menu_map = {
            "F": "forest", "S": "pvp", "K": "weapons", "A": "armor",
            "H": "healer", "V": "stats", "I": "inn", "T": "training",
            "Y": "bank", "L": "list", "W": "mail", "D": "news",
            "C": "marriage", "N": "notes", "O": "other", "X": "expert",
            "M": "announce", "P": "online", "Q": "quit"
        }

        if key in menu_map:
            # Simulate button press
            self.on_button_pressed(type('Event', (), {'button': type('Button', (), {'id': menu_map[key]})})())

class StatsScreen(Screen):
    """Player statistics display"""

    def compose(self) -> ComposeResult:
        if not current_player:
            yield Static("No player loaded")
            return

        p = current_player
        weapon_name = WEAPONS[p.weapon_num][0] if p.weapon_num < len(WEAPONS) else "Stick"
        armor_name = ARMOR[p.armor_num][0] if p.armor_num < len(ARMOR) else "Coat"

        yield Static(f"{p.name}'s Stats", classes="header")
        yield Static("=-" * 30, classes="separator")
        yield Static("")
        yield Static(f"Level           : {p.level}")
        yield Static(f"Experience      : {p.experience:,}")
        yield Static(f"Hit Points      : {p.hitpoints} of {p.max_hitpoints}")
        yield Static(f"Forest Fights   : {p.forest_fights}")
        yield Static(f"Player Fights   : {p.player_fights}")
        yield Static("")
        yield Static(f"Gold in hand    : {p.gold:,}", classes="gold")
        yield Static(f"Gold in bank    : {p.bank_gold:,}", classes="gold")
        yield Static("")
        yield Static(f"Weapon          : {weapon_name}")
        yield Static(f"Armor           : {armor_name}")
        yield Static(f"Charm           : {p.charm}")
        yield Static(f"Gems            : {p.gems}")
        yield Static("")
        yield Static(f"Class           : {CLASS_TYPES[p.class_type]['name']}")
        yield Static(f"Gender          : {'Male' if p.gender == 'M' else 'Female'}")
        yield Static("")
        yield Static("Press any key to continue...")

    def on_key(self, event: events.Key) -> None:
        self.app.pop_screen()

class ForestScreen(Screen):
    """Forest exploration and combat"""

    def compose(self) -> ComposeResult:
        yield Static("The Forest", classes="header")
        yield Static("=-" * 30, classes="separator")
        yield Static("")

        if current_player.forest_fights <= 0:
            yield Static("You are too tired to fight in the forest today.")
            yield Static("Come back tomorrow!")
            yield Static("")
            yield Static("Press any key to return to town...")
        else:
            yield Static("You enter the dark forest...")
            yield Static(f"You have {current_player.forest_fights} forest fights remaining today.")
            yield Static("")

            # Show vault and notes info
            vault_path = vault.get_vault_path()
            if vault_path != "No vault found":
                try:
                    notes = vault.scan_notes()
                    ai_status = "❌"
                    try:
                        from brainbot import is_ai_available
                        ai_status = "🧠" if is_ai_available() else "❌"
                    except ImportError:
                        ai_status = "📦"

                    yield Static(f"📚 {len(notes)} notes lurking in the forest {ai_status}")
                    yield Static(f"📁 Vault: {vault_path.split('/')[-1]}")
                except Exception as e:
                    yield Static(f"⚠️  Vault error: {str(e)[:30]}...")
            else:
                yield Static("⚠️  No Obsidian vault found - using standard enemies")
                yield Static("   Use (V)ault Settings to configure manually")

            yield Static("")
            yield Static("(E)nter the forest")
            yield Static("(R)eturn to town")
            yield Static("")
            yield Static("Your choice? [E] :", classes="prompt")

    def on_key(self, event: events.Key) -> None:
        key = event.key.upper()

        if current_player.forest_fights <= 0:
            self.app.pop_screen()
            return

        if key == "E" or event.key == "enter":
            self.app.push_screen(CombatScreen())
        elif key == "R":
            self.app.pop_screen()

class CombatScreen(Screen):
    """Forest combat with Obsidian integration"""

    def __init__(self):
        super().__init__()
        self.enemy = None
        self.combat_log = []
        self.player_turn = True
        self.quiz_available = True

    def compose(self) -> ComposeResult:
        # Generate enemy based on player level and Obsidian notes
        self.enemy = vault.get_enemy_for_level(current_player.level)

        yield Static("**FIGHT**", classes="header")
        yield Static("=-" * 40, classes="separator")
        yield Static(f"You have encountered {self.enemy.name}!!", classes="enemy")

        # Check AI status and show indicator
        ai_active = False
        ai_description = None
        try:
            from brainbot import sync_generate_enemy_description, is_ai_available
            ai_active = is_ai_available()
            if ai_active and self.enemy.note_content:
                ai_description = sync_generate_enemy_description(
                    self.enemy.note_title,
                    self.enemy.note_content,
                    "warrior"  # base enemy type
                )
        except Exception as e:
            pass

        # Show note and AI status information
        if hasattr(self.enemy, 'note_title') and self.enemy.note_title:
            yield Static(f"📝 Note-Based Enemy: '{self.enemy.note_title}'", classes="stats")
            if ai_active:
                yield Static("🧠 AI-Enhanced Combat (intelligent questions available)", classes="stats")
            else:
                yield Static("🤖 Basic Mode (regex-based questions)", classes="stats")
        else:
            yield Static("⚔️ Standard Forest Enemy", classes="stats")

        # Show description
        if ai_description and hasattr(ai_description, 'backstory'):
            yield Static(f"🎭 {ai_description.backstory[:150]}{'...' if len(ai_description.backstory) > 150 else ''}")
        elif hasattr(self.enemy, 'note_content') and self.enemy.note_content:
            yield Static(f"This creature guards knowledge of '{self.enemy.note_title}'.")
            yield Static("Test your knowledge for bonus damage!")
        else:
            yield Static("A wild forest creature blocks your path!")

        yield Static("Your skill allows you to get the first strike!")

        yield Static("")

        # Initial combat status
        status = (
            f"Your Hitpoints : {current_player.hitpoints}\n"
            f"{self.enemy.name}'s Hitpoints : {self.enemy.hitpoints}"
        )
        yield Static(status, id="combat_status")

        # Initial combat options
        options = [
            "(A)ttack",
            "(S)tats",
            "(R)un"
        ]
        if current_player.can_use_skill():
            skill_type = current_player.class_type
            skill_points = current_player.get_skill_points(skill_type)
            uses_left = CLASS_TYPES[skill_type]['daily_uses'] - current_player.skills_used_today
            mastery_indicator = "★" if current_player.has_ultra_mastery(skill_type) else ""
            options.append(f"({skill_type}){CLASS_TYPES[skill_type]['skill_name']} {mastery_indicator}({uses_left})")
        if self.quiz_available and self.enemy.note_content:
            options.append("(Q)uiz Attack (2x damage if correct)")

        yield Static("\n".join(options), id="combat_options")

    def _update_combat_display(self):
        """Update combat status and options"""
        status = (
            f"Your Hitpoints : {current_player.hitpoints}\n"
            f"{self.enemy.name}'s Hitpoints : {self.enemy.hitpoints}"
        )
        self.query_one("#combat_status").update(status)

        options = [
            "(A)ttack",
            "(S)tats",
            "(R)un"
        ]

        if current_player.can_use_skill():
            skill_type = current_player.class_type
            skill_points = current_player.get_skill_points(skill_type)
            uses_left = CLASS_TYPES[skill_type]['daily_uses'] - current_player.skills_used_today
            mastery_indicator = "★" if current_player.has_ultra_mastery(skill_type) else ""
            options.append(f"({skill_type}){CLASS_TYPES[skill_type]['skill_name']} {mastery_indicator}({uses_left})")

        if self.quiz_available and self.enemy.note_content:
            options.append("(Q)uiz Attack (2x damage if correct)")

        self.query_one("#combat_options").update("\n".join(options))

    def on_key(self, event: events.Key) -> None:
        if not self.player_turn:
            return

        key = event.key.upper()

        if key == "A":
            self._player_attack()
        elif key == "S":
            self.app.push_screen(StatsScreen())
        elif key == "R":
            self._run_away()
        elif key == current_player.class_type and current_player.can_use_skill():
            self._skill_attack()
        elif key == "Q" and self.quiz_available and self.enemy.note_content:
            self.app.push_screen(QuizScreen(self.enemy, self))

    def _player_attack(self):
        """Player normal attack"""
        damage = random.randint(1, current_player.attack_power)
        self.enemy.hitpoints -= damage

        self.notify(f"You hit for {damage} damage!")

        if self.enemy.hitpoints <= 0:
            self._victory()
        else:
            self._enemy_attack()

    def _skill_attack(self):
        """Player special skill attack"""
        if not current_player.can_use_skill():
            self.notify("You have no skill uses remaining today!")
            return

        current_player.use_skill()
        skill_type = current_player.class_type
        skill_points = current_player.get_skill_points(skill_type)

        # Calculate damage based on skill points
        base_damage = current_player.attack_power
        skill_multiplier = 1.0 + (skill_points * 0.05)  # 5% per skill point

        if skill_type == 'K':  # Death Knight
            damage = int(base_damage * skill_multiplier * random.uniform(1.5, 2.5))
            skill_name = "Death Knight Strike"
        elif skill_type == 'P':  # Mystical
            damage = int(base_damage * skill_multiplier * random.uniform(1.3, 2.0))
            skill_name = "Mystical Blast"
        elif skill_type == 'D':  # Thieving
            damage = int(base_damage * skill_multiplier * random.uniform(1.2, 2.2))
            skill_name = "Sneak Attack"
        else:
            damage = base_damage
            skill_name = "Skill Attack"

        self.enemy.hitpoints -= damage

        # Ultra-mastery bonus message
        mastery_msg = ""
        if current_player.has_ultra_mastery(skill_type):
            mastery_msg = " **ULTRA MASTERY!**"

        uses_left = CLASS_TYPES[skill_type]['daily_uses'] - current_player.skills_used_today
        self.notify(f"{skill_name}! You hit for {damage} damage!{mastery_msg} ({uses_left} uses left)")

        if self.enemy.hitpoints <= 0:
            self._victory()
        else:
            self._enemy_attack()

    def quiz_attack(self, correct: bool):
        """Quiz-based attack from QuizScreen"""
        self.quiz_available = False

        if correct:
            damage = current_player.attack_power * 2
            self.enemy.hitpoints -= damage
            self.notify(f"**CRITICAL HIT** You remember and strike for {damage} damage!")
        else:
            self.notify("Your knowledge fails you! No damage dealt.")

        if self.enemy.hitpoints <= 0:
            self._victory()
        else:
            self._enemy_attack()

        self._update_combat_display()

    def _enemy_attack(self):
        """Enemy attacks player"""
        damage = random.randint(1, self.enemy.attack)
        damage = max(1, damage - (current_player.defense_power // 2))
        current_player.hitpoints -= damage

        self.notify(f"{self.enemy.name} hits you for {damage} damage!")

        if current_player.hitpoints <= 0:
            self._defeat()
        else:
            self._update_combat_display()

    def _victory(self):
        """Player wins combat"""
        current_player.forest_fights -= 1
        current_player.experience += self.enemy.exp_reward
        current_player.gold += self.enemy.gold_reward

        self.notify(f"You have killed {self.enemy.name}!")
        self.notify(f"You receive {self.enemy.exp_reward} experience and {self.enemy.gold_reward} gold!")

        # Check for level up
        if current_player.can_level_up():
            hp_gain = current_player.level_up()
            self.notify(f"You have gained a level! (+{hp_gain} HP)")

        game_db.save_player(current_player)
        self.app.pop_screen()

    def _defeat(self):
        """Player loses combat"""
        current_player.hitpoints = 0
        current_player.alive = False
        current_player.gold = 0  # Lose all carried gold

        self.notify("You have been defeated!")
        self.notify("You lose all your gold and awaken in the healer's hut tomorrow.")

        game_db.save_player(current_player)
        self.app.pop_screen()

    def _run_away(self):
        """Player runs from combat"""
        self.notify(f"You run away from {self.enemy.name}!")
        self.app.pop_screen()

class QuizScreen(Screen):
    """Quiz question for bonus combat damage"""

    def __init__(self, enemy, combat_screen):
        super().__init__()
        self.enemy = enemy
        self.combat_screen = combat_screen
        self.question, self.answer = vault.generate_quiz_question(
            type('Note', (), {
                'title': enemy.note_title,
                'content': enemy.note_content
            })()
        )

    def compose(self) -> ComposeResult:
        yield Static("Knowledge Strike!", classes="header")
        yield Static("=-" * 40, classes="separator")
        yield Static(f"Facing: {self.enemy.name}")

        # Show AI status for quiz
        try:
            from brainbot import is_ai_available
            if is_ai_available():
                yield Static("🧠 AI-Enhanced Question", classes="stats")
            else:
                yield Static("📝 Pattern-Based Question", classes="stats")
        except ImportError:
            yield Static("📝 Pattern-Based Question", classes="stats")

        yield Static("")
        yield Static("Answer correctly for a CRITICAL HIT!")
        yield Static("")
        yield Static(f"Question: {self.question}")
        yield Static("")
        yield Input(placeholder="Your answer...", id="answer")
        yield Static("")
        yield Static("(Enter) to answer, (Escape) to cancel")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Check quiz answer with AI-enhanced validation"""
        user_answer = event.value.strip()

        # Try AI-enhanced answer validation
        correct = False
        try:
            from brainbot import ai_quiz_system, is_ai_available
            if is_ai_available():
                correct = ai_quiz_system.validate_answer(user_answer, self.answer, ai_question=True)
            else:
                # Fallback to simple matching
                user_lower = user_answer.lower()
                correct_lower = self.answer.lower()
                correct = any(word in user_lower for word in correct_lower.split() if len(word) > 2)
        except Exception as e:
            # Fallback to simple matching
            user_lower = user_answer.lower()
            correct_lower = self.answer.lower()
            correct = any(word in user_lower for word in correct_lower.split() if len(word) > 2)

        self.app.pop_screen()
        self.combat_screen.quiz_attack(correct)

    def on_key(self, event: events.Key) -> None:
        if event.key == "escape":
            self.app.pop_screen()

# Additional screens would go here (WeaponsScreen, ArmorScreen, etc.)
# For brevity, I'll implement the core ones

class WeaponsScreen(Screen):
    """King Arthur's Weapons shop"""

    def compose(self) -> ComposeResult:
        yield Static("King Arthur's Weapons", classes="header")
        yield Static("=-" * 30, classes="separator")
        yield Static("")
        yield Static(f"Gold: {current_player.gold:,}", classes="gold")
        yield Static(f"Current weapon: {WEAPONS[current_player.weapon_num][0]}")
        yield Static("")

        # Show available weapons
        for i, (name, price, power) in enumerate(WEAPONS):
            if i <= current_player.weapon_num + 1:  # Can only buy next weapon
                if i == current_player.weapon_num:
                    yield Static(f"  {name} - OWNED", classes="gold")
                else:
                    can_afford = current_player.gold >= price
                    color = "bright_green" if can_afford else "bright_red"
                    yield Button(f"{i+1}. {name} - {price:,} gold (Power: {power})",
                               id=f"weapon_{i}", disabled=not can_afford)

        yield Static("")
        yield Static("(Q) Return to town")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle weapon purchase"""
        if event.button.id and event.button.id.startswith("weapon_"):
            weapon_idx = int(event.button.id.split("_")[1])
            weapon_name, price, power = WEAPONS[weapon_idx]

            if current_player.gold >= price:
                current_player.gold -= price
                current_player.weapon_num = weapon_idx
                current_player.weapon = weapon_name
                game_db.save_player(current_player)

                self.notify(f"You bought {weapon_name}!")
                self.app.pop_screen()
            else:
                self.notify("You don't have enough gold!")

    def on_key(self, event: events.Key) -> None:
        if event.key.upper() == "Q":
            self.app.pop_screen()

class InnScreen(Screen):
    """The Inn - placeholder for now"""

    def compose(self) -> ComposeResult:
        yield Static("Ye Olde Inn", classes="header")
        yield Static("=-" * 30, classes="separator")
        yield Static("")
        yield Static("The inn is cozy and warm...")
        yield Static("")
        yield Static("(B)ar Room")
        yield Static("(V)iolet's Room")
        yield Static("(Q) Return to town")

    def on_key(self, event: events.Key) -> None:
        key = event.key.upper()
        if key == "Q":
            self.app.pop_screen()
        else:
            self.notify(f"{key} - Not yet implemented")

# Placeholder screens
class ArmorScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Static("Abdul's Armor - Coming Soon!")
        yield Static("Press any key to return...")

    def on_key(self, event: events.Key) -> None:
        self.app.pop_screen()

class BankScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Static("Ye Old Bank - Coming Soon!")
        yield Static("Press any key to return...")

    def on_key(self, event: events.Key) -> None:
        self.app.pop_screen()

class HealerScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Static("Healer's Hut - Coming Soon!")
        yield Static("Press any key to return...")

    def on_key(self, event: events.Key) -> None:
        self.app.pop_screen()

class NotesViewerScreen(Screen):
    """Display Obsidian notes and their status in the game"""

    def compose(self) -> ComposeResult:
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
        yield Static("Press any key to return to town...")

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

def main():
    """Run the game"""
    # Initialize AI system
    try:
        from brainbot import initialize_ai
        print("🔄 Starting AI initialization...")
        initialize_ai()
    except Exception as e:
        print(f"⚠️  AI initialization error: {e}")
        print("🔄 Continuing with regex-based fallback")

    app = LordApp()
    app.run()

if __name__ == "__main__":
    main()
"""
LORD Cavern IGM for Legend of the Obsidian Vault
Daily exploration with Riddler system and random encounters
"""
import datetime
import random
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static
from textual import events


class CavernScreen(Screen):
    """LORD Cavern - Daily exploration with Riddler encounters"""

    def __init__(self):
        super().__init__()
        self.riddler_active = False
        self.current_riddle = None
        self.riddle_answer = ""

    def compose(self) -> ComposeResult:
        # Delayed import to avoid circular dependency
        import lov

        # Colored Cavern ASCII Art Header
        yield Static("        ✦ THE MYSTICAL LORD CAVERN ✦", classes="cavern-title")
        yield Static("    ▄████████████████████████████████████████████▄", classes="cavern-cave")
        yield Static("   ███▀▀▀                                    ▀▀▀███", classes="cavern-cave")
        yield Static("  ██▀     ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░     ▀██", classes="cavern-shadow")
        yield Static("  █▌      ░░   🔮 Ancient Mysteries 🔮   ░░      ▐█", classes="cavern-shadow")
        yield Static("  █▌      ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░      ▐█", classes="cavern-shadow")
        yield Static("  ██▄     ╠══════════════════════════════╣     ▄██", classes="cavern-cave")
        yield Static("   ███▄▄▄ ║    The Riddler Awaits...    ║ ▄▄▄███", classes="cavern-cave")
        yield Static("    ▀████ ╚══════════════════════════════╝ ████▀", classes="cavern-cave")
        yield Static("════════════════════════════════════════════════════", classes="cavern-ground")

        # Two blank lines below header
        yield Static("")
        yield Static("")

        # Check daily search limit
        searches_today = lov.current_player.cavern_searches_today
        max_daily_searches = 3

        if searches_today >= max_daily_searches:
            yield Static("The cavern is too dangerous to explore further today.", classes="cavern-content")
            yield Static("The ancient magic has been disturbed enough.", classes="cavern-content")
            yield Static("")
            yield Static("(R)eturn to forest", classes="cavern-content")
        else:
            # Scene description
            yield Static("Deep within the earth, ancient mysteries whisper in the darkness.", classes="cavern-content")
            yield Static(f"You have explored {searches_today} of {max_daily_searches} times today.", classes="cavern-content")
            yield Static("")

            # Actions menu
            yield Static("(E)xplore deeper into the cavern", classes="cavern-content")
            yield Static("(S)earch for hidden treasures", classes="cavern-content")
            yield Static("(L)isten for the Riddler's voice", classes="cavern-content")
            yield Static("(R)eturn to forest", classes="cavern-content")

        # One blank line before status
        yield Static("")

        # Player status line
        hp_text = f"({lov.current_player.hitpoints} of {lov.current_player.max_hitpoints})"
        status_line = f"HitPoints: {hp_text}  Gold: {lov.current_player.gold}  Gems: {lov.current_player.gems}"
        yield Static(status_line, classes="cavern-status")

        # One blank line before command area
        yield Static("")

        # Command prompt area
        now = datetime.datetime.now()
        time_str = f"{now.hour:02d}:{now.minute:02d}"

        # Location and commands
        location_commands = f"LORD Cavern (E,S,L,R,Q)  (? for menu)"
        yield Static(location_commands, classes="cavern-location-commands")

        # Command prompt with time and cursor
        yield Static(f"Your command, {lov.current_player.name}? [{time_str}]: █", classes="cavern-prompt")

    def on_key(self, event: events.Key) -> None:
        # Delayed import to avoid circular dependency
        import lov

        key = event.key.upper()

        # Check if player has reached daily limit
        if lov.current_player.cavern_searches_today >= 3:
            if key == "R" or key == "Q":
                self.app.pop_screen()
            return

        if key == "E":
            # Explore deeper - random encounter
            self._explore_cavern()
        elif key == "S":
            # Search for treasures
            self._search_treasures()
        elif key == "L":
            # Listen for Riddler
            self._encounter_riddler()
        elif key == "R" or key == "Q":
            self.app.pop_screen()
        elif key == "?":
            # Show help menu
            self.notify("E = Explore, S = Search treasures, L = Listen for Riddler, R = Return to forest")

    def _explore_cavern(self):
        """Random exploration encounter"""
        # Delayed import to avoid circular dependency
        import lov

        # Increment daily searches
        lov.current_player.cavern_searches_today += 1

        encounter_roll = random.randint(1, 100)

        if encounter_roll <= 30:
            # Find gold
            gold_found = random.randint(50, 200) * lov.current_player.level
            lov.current_player.gold += gold_found
            self.notify(f"You discover an ancient treasure cache! (+{gold_found:,} gold)")

        elif encounter_roll <= 50:
            # Find gems
            gems_found = random.randint(1, 3)
            lov.current_player.gems += gems_found
            self.notify(f"Mystical gems glimmer in the darkness! (+{gems_found} gems)")

        elif encounter_roll <= 70:
            # Dangerous encounter - lose HP
            damage = random.randint(5, 15)
            lov.current_player.hitpoints = max(1, lov.current_player.hitpoints - damage)
            self.notify(f"You trigger an ancient trap! (-{damage} hitpoints)")

        elif encounter_roll <= 85:
            # Find nothing
            self.notify("The cavern passages echo with emptiness...")

        else:
            # Special encounter - boost stats temporarily
            if random.choice([True, False]):
                lov.current_player.strength += 1
                self.notify("Ancient power flows through you! (+1 Strength)")
            else:
                lov.current_player.defense += 1
                self.notify("The cavern's magic protects you! (+1 Defense)")

        lov.game_db.save_player(lov.current_player)
        self._refresh_screen()

    def _search_treasures(self):
        """Targeted treasure search"""
        # Delayed import to avoid circular dependency
        import lov

        # Increment daily searches
        lov.current_player.cavern_searches_today += 1

        search_roll = random.randint(1, 100)

        if search_roll <= 40:
            # Find moderate gold
            gold_found = random.randint(25, 100) * lov.current_player.level
            lov.current_player.gold += gold_found
            self.notify(f"Your careful search reveals hidden riches! (+{gold_found:,} gold)")

        elif search_roll <= 60:
            # Find experience points
            exp_gain = random.randint(50, 150)
            lov.current_player.experience += exp_gain
            self.notify(f"You gain wisdom from ancient inscriptions! (+{exp_gain} experience)")

        elif search_roll <= 80:
            # Nothing found
            self.notify("Despite your careful search, you find nothing of value.")

        else:
            # Special item or blessing
            blessing_roll = random.randint(1, 3)
            if blessing_roll == 1:
                # Temporary HP boost
                hp_boost = random.randint(10, 25)
                lov.current_player.hitpoints = min(lov.current_player.max_hitpoints + hp_boost,
                                                 lov.current_player.hitpoints + hp_boost)
                self.notify(f"A mystical fountain restores your vitality! (+{hp_boost} HP)")
            elif blessing_roll == 2:
                # Charm boost
                lov.current_player.charm += 1
                self.notify("Ancient charisma flows through you! (+1 Charm)")
            else:
                # Forest fights boost
                lov.current_player.forest_fights += 1
                self.notify("The cavern's energy invigorates you! (+1 Forest Fight)")

        lov.game_db.save_player(lov.current_player)
        self._refresh_screen()

    def _encounter_riddler(self):
        """Encounter the mysterious Riddler"""
        # Delayed import to avoid circular dependency
        import lov

        # Increment daily searches
        lov.current_player.cavern_searches_today += 1

        riddles = [
            {
                "question": "I have cities, but no houses. I have mountains, but no trees. I have water, but no fish. What am I?",
                "answer": "MAP",
                "reward_type": "gems",
                "reward_amount": 3
            },
            {
                "question": "The more you take, the more you leave behind. What am I?",
                "answer": "FOOTSTEPS",
                "reward_type": "gold",
                "reward_amount": 500
            },
            {
                "question": "I speak without a mouth and hear without ears. I have no body, but come alive with wind. What am I?",
                "answer": "ECHO",
                "reward_type": "strength",
                "reward_amount": 2
            },
            {
                "question": "What gets wet while drying?",
                "answer": "TOWEL",
                "reward_type": "defense",
                "reward_amount": 2
            },
            {
                "question": "I'm not clothes but I cover your body; I'm not a book but you can read me. What am I?",
                "answer": "TATTOO",
                "reward_type": "charm",
                "reward_amount": 2
            }
        ]

        riddle = random.choice(riddles)
        self.current_riddle = riddle
        self.riddler_active = True

        self.notify("A mysterious hooded figure emerges from the shadows...")
        self.notify(f"The Riddler speaks: '{riddle['question']}'")
        self.notify("Type your answer and press Enter, or type 'skip' to avoid the riddle.")

    def _process_riddle_answer(self, answer: str):
        """Process the player's riddle answer"""
        # Delayed import to avoid circular dependency
        import lov

        if not self.current_riddle:
            return

        if answer.upper() == "SKIP":
            self.notify("The Riddler nods knowingly and fades back into the shadows...")
            self.riddler_active = False
            self.current_riddle = None
            return

        correct_answer = self.current_riddle["answer"].upper()
        user_answer = answer.upper().strip()

        if user_answer == correct_answer or correct_answer in user_answer:
            # Correct answer - give reward
            reward_type = self.current_riddle["reward_type"]
            reward_amount = self.current_riddle["reward_amount"]

            if reward_type == "gold":
                gold_reward = reward_amount * lov.current_player.level
                lov.current_player.gold += gold_reward
                self.notify(f"Correct! The Riddler grants you {gold_reward:,} gold!")
            elif reward_type == "gems":
                lov.current_player.gems += reward_amount
                self.notify(f"Correct! The Riddler grants you {reward_amount} mystical gems!")
            elif reward_type == "strength":
                lov.current_player.strength += reward_amount
                self.notify(f"Correct! The Riddler's magic increases your strength by {reward_amount}!")
            elif reward_type == "defense":
                lov.current_player.defense += reward_amount
                self.notify(f"Correct! The Riddler's magic increases your defense by {reward_amount}!")
            elif reward_type == "charm":
                lov.current_player.charm += reward_amount
                self.notify(f"Correct! The Riddler's magic increases your charm by {reward_amount}!")

            self.notify("'Wisdom is its own reward,' the Riddler whispers before vanishing.")
        else:
            # Wrong answer - minor penalty or nothing
            penalty_roll = random.randint(1, 100)
            if penalty_roll <= 30:
                damage = random.randint(5, 10)
                lov.current_player.hitpoints = max(1, lov.current_player.hitpoints - damage)
                self.notify(f"Wrong! The Riddler's disappointment stings! (-{damage} HP)")
            else:
                self.notify("Wrong! The Riddler shakes his head sadly and disappears.")

        lov.game_db.save_player(lov.current_player)
        self.riddler_active = False
        self.current_riddle = None
        self._refresh_screen()

    def _refresh_screen(self):
        """Refresh the screen to show updated stats"""
        self.app.pop_screen()
        self.app.push_screen(CavernScreen())
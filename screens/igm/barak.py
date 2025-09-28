"""
Barak's House IGM for Legend of the Obsidian Vault
Book reading system, aggression management, and basement dice game
"""
import datetime
import random
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static
from textual import events


class BarakScreen(Screen):
    """Barak's House - Scholar and gambling den"""

    def __init__(self):
        super().__init__()
        self.reading_book = False
        self.current_book = None
        self.in_basement = False
        self.gambling_session = False
        self.dice_bet = 0

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
        yield Static("    ║   📚 Ancient Tomes    🎲 Basement Games     ║", classes="barak-decoration")
        yield Static("    ║   📖 Study Halls      ⚔️ Warrior Training   ║", classes="barak-decoration")
        yield Static("    ║   📜 Sage Wisdom      💰 High Stakes        ║", classes="barak-decoration")
        yield Static("    ╚══════════════════════════════════════════════╝", classes="barak-border")

        # Two blank lines below header
        yield Static("")
        yield Static("")

        if self.in_basement:
            self._compose_basement()
        else:
            self._compose_main_house()

    def _compose_main_house(self):
        """Compose the main house interface"""
        # Delayed import to avoid circular dependency
        import lov

        # Scene description
        yield Static("Welcome to Barak's House, where knowledge and fortune intertwine.", classes="barak-content")
        yield Static("The scholarly atmosphere is thick with the scent of ancient parchments.", classes="barak-content")
        yield Static("")

        # Check aggression level
        aggression_text = self._get_aggression_description()
        yield Static(f"Barak notices your demeanor: {aggression_text}", classes="barak-content")
        yield Static("")

        # Main house options
        yield Static("(R)ead ancient books (+1 Intelligence temporarily)", classes="barak-content")
        yield Static("(S)tudy combat techniques (+1 to random stat)", classes="barak-content")
        yield Static("(T)alk to Barak about local lore", classes="barak-content")
        yield Static("(B)asement gambling den (gold required)", classes="barak-content")
        yield Static("(L)eave house", classes="barak-content")

        # Status and command area
        self._compose_status_area()

    def _compose_basement(self):
        """Compose the basement gambling interface"""
        # Delayed import to avoid circular dependency
        import lov

        yield Static("You descend into Barak's basement gambling den...", classes="barak-content")
        yield Static("Smoke fills the air as dice clatter on wooden tables.", classes="barak-content")
        yield Static("")

        if self.gambling_session:
            yield Static(f"Current bet: {self.dice_bet} gold", classes="barak-content")
            yield Static("Barak prepares to roll the dice...", classes="barak-content")
            yield Static("")
            yield Static("(R)oll dice and see your fate", classes="barak-content")
            yield Static("(Q)uit gambling session", classes="barak-content")
        else:
            yield Static("Games available:", classes="barak-content")
            yield Static("(D)ice game - Bet gold, win double or lose all", classes="barak-content")
            yield Static("(H)igh stakes dice - High risk, high reward", classes="barak-content")
            yield Static("(U)pstairs to main house", classes="barak-content")

        self._compose_status_area()

    def _compose_status_area(self):
        """Compose the status and command prompt area"""
        # Delayed import to avoid circular dependency
        import lov

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
        location = "Basement" if self.in_basement else "Barak's House"
        location_commands = f"{location} (R,S,T,B,L)  (? for menu)"
        yield Static(location_commands, classes="barak-location-commands")

        # Command prompt with time and cursor
        yield Static(f"Your command, {lov.current_player.name}? [{time_str}]: █", classes="barak-prompt")

    def on_key(self, event: events.Key) -> None:
        # Delayed import to avoid circular dependency
        import lov

        key = event.key.upper()

        if self.in_basement:
            self._handle_basement_input(key)
        else:
            self._handle_main_house_input(key)

    def _handle_main_house_input(self, key: str):
        """Handle input in the main house"""
        # Delayed import to avoid circular dependency
        import lov

        if key == "R":
            # Read books - increase intelligence temporarily
            self._read_books()
        elif key == "S":
            # Study combat techniques
            self._study_combat()
        elif key == "T":
            # Talk to Barak
            self._talk_to_barak()
        elif key == "B":
            # Enter basement
            if lov.current_player.gold >= 50:
                self.in_basement = True
                self._refresh_screen()
            else:
                self.notify("Barak shakes his head. 'You need at least 50 gold to enter the basement.'")
        elif key == "L":
            self.app.pop_screen()
        elif key == "?":
            self.notify("R = Read books, S = Study combat, T = Talk to Barak, B = Basement, L = Leave")

    def _handle_basement_input(self, key: str):
        """Handle input in the basement"""
        # Delayed import to avoid circular dependency
        import lov

        if self.gambling_session:
            if key == "R":
                # Roll dice in active session
                self._roll_dice()
            elif key == "Q":
                # Quit gambling session
                self.gambling_session = False
                self.dice_bet = 0
                self._refresh_screen()
        else:
            if key == "D":
                # Regular dice game
                self._start_dice_game("normal")
            elif key == "H":
                # High stakes dice
                self._start_dice_game("high_stakes")
            elif key == "U":
                # Go upstairs
                self.in_basement = False
                self._refresh_screen()
            elif key == "?":
                self.notify("D = Dice game, H = High stakes, U = Upstairs")

    def _read_books(self):
        """Read ancient books for intelligence boost"""
        # Delayed import to avoid circular dependency
        import lov

        books = [
            {
                "title": "The Art of War",
                "effect": "intelligence",
                "boost": 2,
                "description": "Strategic thinking flows through your mind."
            },
            {
                "title": "Mystical Energies",
                "effect": "mystical_points",
                "boost": 1,
                "description": "You understand deeper mystical forces."
            },
            {
                "title": "Thievery Techniques",
                "effect": "thieving_points",
                "boost": 1,
                "description": "Subtle arts of stealth become clearer."
            },
            {
                "title": "Ancient Histories",
                "effect": "experience",
                "boost": 100,
                "description": "Knowledge of ages past enriches your wisdom."
            },
            {
                "title": "Combat Mastery",
                "effect": "strength",
                "boost": 1,
                "description": "Physical training techniques sharpen your body."
            }
        ]

        book = random.choice(books)

        self.notify(f"You open '{book['title']}' and begin reading...")
        self.notify(book['description'])

        # Apply book effect
        if book['effect'] == 'intelligence':
            lov.current_player.intelligence += book['boost']
        elif book['effect'] == 'mystical_points':
            lov.current_player.mystical_points += book['boost']
        elif book['effect'] == 'thieving_points':
            lov.current_player.thieving_points += book['boost']
        elif book['effect'] == 'experience':
            lov.current_player.experience += book['boost']
        elif book['effect'] == 'strength':
            lov.current_player.strength += book['boost']

        self.notify(f"You gain {book['boost']} {book['effect'].replace('_', ' ')}!")
        lov.game_db.save_player(lov.current_player)

    def _study_combat(self):
        """Study combat techniques for random stat boost"""
        # Delayed import to avoid circular dependency
        import lov

        stats = ['strength', 'defense', 'charm']
        chosen_stat = random.choice(stats)
        boost = random.randint(1, 2)

        self.notify("You practice combat forms with Barak's training equipment...")

        if chosen_stat == 'strength':
            lov.current_player.strength += boost
            self.notify(f"Your muscles feel stronger! (+{boost} Strength)")
        elif chosen_stat == 'defense':
            lov.current_player.defense += boost
            self.notify(f"Your stance improves! (+{boost} Defense)")
        elif chosen_stat == 'charm':
            lov.current_player.charm += boost
            self.notify(f"Your confidence grows! (+{boost} Charm)")

        lov.game_db.save_player(lov.current_player)

    def _talk_to_barak(self):
        """Talk to Barak for local lore and hints"""
        # Delayed import to avoid circular dependency
        import lov

        lore_messages = [
            "The forest holds many secrets, but beware the ancient creatures within.",
            "I've heard whispers of a mystical cavern where riddlers test the worthy.",
            "The inn's violet has caught many a warrior's eye, but few their heart.",
            "Gold flows like water in the basement, but fortune favors the bold.",
            "There are codes spoken in the forest that unlock ancient powers...",
            "Some say there's a fairy in these lands who teaches healing arts.",
            "The dragon sleeps, but its awakening draws near for the strongest warriors.",
            "Jennie Garth appears to those with high spirits - treat her with respect."
        ]

        message = random.choice(lore_messages)
        self.notify(f"Barak strokes his beard thoughtfully: '{message}'")

        # Small chance for bonus
        if random.randint(1, 100) <= 20:
            bonus_roll = random.randint(1, 3)
            if bonus_roll == 1:
                lov.current_player.intelligence += 1
                self.notify("Barak's wisdom enlightens you! (+1 Intelligence)")
            elif bonus_roll == 2:
                gem_found = random.randint(1, 2)
                lov.current_player.gems += gem_found
                self.notify(f"Barak gives you a small gem as a token of friendship! (+{gem_found} gems)")
            else:
                gold_found = random.randint(25, 75)
                lov.current_player.gold += gold_found
                self.notify(f"Barak tips you for listening! (+{gold_found} gold)")

            lov.game_db.save_player(lov.current_player)

    def _start_dice_game(self, game_type: str):
        """Start a dice gambling session"""
        # Delayed import to avoid circular dependency
        import lov

        if game_type == "normal":
            min_bet = 50
            max_bet = min(lov.current_player.gold, 500)
        else:  # high_stakes
            min_bet = 200
            max_bet = min(lov.current_player.gold, 2000)

        if lov.current_player.gold < min_bet:
            self.notify(f"You need at least {min_bet} gold for this game.")
            return

        # For now, bet a random amount in range
        self.dice_bet = min(random.randint(min_bet, max_bet), lov.current_player.gold)
        self.gambling_session = True

        game_name = "High Stakes" if game_type == "high_stakes" else "Regular"
        self.notify(f"You join a {game_name} dice game with {self.dice_bet} gold at stake!")
        self._refresh_screen()

    def _roll_dice(self):
        """Execute dice roll and determine outcome"""
        # Delayed import to avoid circular dependency
        import lov

        player_roll = random.randint(1, 6) + random.randint(1, 6)  # 2d6
        house_roll = random.randint(1, 6) + random.randint(1, 6)   # 2d6

        self.notify(f"You roll: {player_roll}")
        self.notify(f"House rolls: {house_roll}")

        if player_roll > house_roll:
            # Player wins - double the bet
            winnings = self.dice_bet * 2
            lov.current_player.gold += winnings
            self.notify(f"You win! Gained {winnings} gold!")
        elif player_roll == house_roll:
            # Tie - return bet
            lov.current_player.gold += self.dice_bet
            self.notify("It's a tie! Your bet is returned.")
        else:
            # Player loses - already deducted bet at start
            self.notify(f"House wins! You lose {self.dice_bet} gold.")

        # End gambling session
        self.gambling_session = False
        self.dice_bet = 0
        lov.game_db.save_player(lov.current_player)
        self._refresh_screen()

    def _get_aggression_description(self):
        """Get description based on player's aggression/behavior"""
        # Delayed import to avoid circular dependency
        import lov

        # Use kills as a rough aggression metric
        total_kills = getattr(lov.current_player, 'total_kills', 0)

        if total_kills < 10:
            return "peaceful and scholarly"
        elif total_kills < 50:
            return "moderately experienced"
        elif total_kills < 100:
            return "battle-hardened"
        elif total_kills < 200:
            return "fearsome and dangerous"
        else:
            return "legendary and terrifying"

    def _refresh_screen(self):
        """Refresh the screen to show updated interface"""
        self.app.pop_screen()
        new_screen = BarakScreen()
        new_screen.in_basement = self.in_basement
        new_screen.gambling_session = self.gambling_session
        new_screen.dice_bet = self.dice_bet
        self.app.push_screen(new_screen)
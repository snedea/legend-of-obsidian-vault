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
            # Basement content
            yield Static("You descend into Barak's basement gambling den...", classes="barak-content")
            yield Static("Smoke fills the air as dice clatter on wooden tables.", classes="barak-content")
            yield Static("")

            if self.gambling_session:
                yield Static(f"💰 Current bet: {self.dice_bet} gold", classes="barak-content")
                yield Static("🎲 Barak prepares to roll the dice...", classes="barak-content")
                yield Static("🎯 Win: +100% of bet | Tie: Keep bet | Lose: -100% of bet", classes="barak-content")
                yield Static("")
                yield Static("═══ GAMBLING SESSION ═══", classes="barak-content")
                yield Static("(R)oll dice and see your fate", classes="barak-content")
                yield Static("(Q)uit gambling session - Keep remaining gold", classes="barak-content")
                yield Static("(?)Help - Show commands", classes="barak-content")
            else:
                yield Static("═══ GAMBLING GAMES ═══", classes="barak-content")
                yield Static("(D)ice game - Bet 50-500g, win double or lose all (2d6 vs 2d6)", classes="barak-content")
                yield Static("(H)igh stakes dice - Bet 200-2000g, higher risk/reward", classes="barak-content")
                yield Static("")
                yield Static(f"💰 Your gold: {lov.current_player.gold}", classes="barak-content")
                yield Static("")
                yield Static("(U)pstairs to main house", classes="barak-content")
                yield Static("(?)Help - Show commands", classes="barak-content")
        else:
            # Main house content
            yield Static("Welcome to Barak's House, where knowledge and fortune intertwine.", classes="barak-content")
            yield Static("The scholarly atmosphere is thick with the scent of ancient parchments.", classes="barak-content")
            yield Static("")

            # Check aggression level - inline to avoid import issues
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

            # Main house options
            yield Static("═══ AVAILABLE ACTIONS ═══", classes="barak-content")
            yield Static("(R)ead ancient books - Gain INT, experience, or skill points", classes="barak-content")
            yield Static("(S)tudy combat techniques - Gain +1-2 STR/DEF/CHARM randomly", classes="barak-content")
            yield Static("(T)alk to Barak - Free lore + 20% chance bonus gold/gems/INT", classes="barak-content")

            # Show basement requirements dynamically
            gold_req = 50
            if lov.current_player.gold >= gold_req:
                yield Static(f"(B)asement gambling den - {gold_req}+ gold (You have {lov.current_player.gold})", classes="barak-content")
            else:
                yield Static(f"(B)asement gambling den - NEED {gold_req} gold (You have {lov.current_player.gold})", classes="barak-content")

            yield Static("")
            yield Static("(L)eave house", classes="barak-content")
            yield Static("(?)Help - Show all commands", classes="barak-content")

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

        # Location and commands - Dynamic based on state
        if self.in_basement:
            if self.gambling_session:
                location_commands = "Basement Gambling (R,Q,?)  Click buttons or use keys"
            else:
                location_commands = "Basement Games (D,H,U,?)  Click buttons or use keys"
        else:
            location_commands = "Barak's House (R,S,T,B,L,?)  Click buttons or use keys"
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
            # Enter basement gambling den
            if lov.current_player.gold >= 50:
                self.in_basement = True
                self._refresh_screen()
            else:
                self.notify("You need at least 50 gold to enter the gambling den!")
        elif key == "L":
            # Leave house
            self.app.pop_screen()
        elif key == "?":
            self.notify("R = Read, S = Study, T = Talk, B = Basement, L = Leave")

    def _handle_basement_input(self, key: str):
        """Handle input in the basement"""
        # Delayed import to avoid circular dependency
        import lov

        if self.gambling_session:
            if key == "R":
                self._roll_dice()
            elif key == "Q":
                self.gambling_session = False
                self._refresh_screen()
            elif key == "?":
                self.notify("R = Roll dice, Q = Quit gambling")
        else:
            if key == "D":
                self._start_dice_game(50, 500)
            elif key == "H":
                self._start_high_stakes_dice(200, 2000)
            elif key == "U":
                self.in_basement = False
                self._refresh_screen()
            elif key == "?":
                self.notify("D = Dice game, H = High stakes, U = Upstairs")

    def _refresh_screen(self):
        """Refresh the screen display"""
        self.app.refresh()

    def _read_books(self):
        """Read ancient books for intelligence boost"""
        # Simple implementation
        import lov

        books = [
            {"title": "Ancient Mysteries", "boost": 1, "effect": "intelligence"},
            {"title": "Combat Tactics", "boost": 2, "effect": "experience"},
            {"title": "Arcane Knowledge", "boost": 1, "effect": "intelligence"},
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

    def _start_dice_game(self, min_bet: int, max_bet: int):
        """Start a dice gambling session"""
        import lov

        if lov.current_player.gold < min_bet:
            self.notify(f"You need at least {min_bet} gold to play!")
            return

        # For now, just notify - full implementation would handle betting
        self.notify("Dice game started! (Simplified version)")

    def _start_high_stakes_dice(self, min_bet: int, max_bet: int):
        """Start high stakes dice gambling"""
        import lov

        if lov.current_player.gold < min_bet:
            self.notify(f"You need at least {min_bet} gold for high stakes!")
            return

        self.notify("High stakes dice! (Simplified version)")

    def _roll_dice(self):
        """Roll dice in gambling session"""
        self.notify("Rolling dice... (Simplified)")
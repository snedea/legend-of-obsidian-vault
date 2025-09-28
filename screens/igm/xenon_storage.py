"""
Xenon's Storage Facility IGM for Legend of the Obsidian Vault
Strategic resource management, horse trading, and dark resource exchange
"""
import datetime
import random
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button, Input
from textual import events


class XenonStorageScreen(Screen):
    """Xenon's Storage - Strategic resource management facility"""

    def __init__(self):
        super().__init__()
        self.transaction_mode = None  # 'store_gold', 'store_gems', 'retrieve_gold', 'retrieve_gems', 'name_horse', 'trade_children'

    def compose(self) -> ComposeResult:
        # Delayed import to avoid circular dependency
        import lov

        # Colored Xenon's Storage ASCII Art Header
        yield Static("        ✦ XENON'S STORAGE FACILITY ✦", classes="xenon-title")
        yield Static("    ╔════════════════════════════════════════════╗", classes="xenon-border")
        yield Static("    ║  📦 🏰 📦 Strategic Resource Management 📦 🏰 📦 ║", classes="xenon-decoration")
        yield Static("    ║                                            ║", classes="xenon-border")
        yield Static("    ║    🔒 Secure Vaults    🐎 Horse Stables    ║", classes="xenon-decoration")
        yield Static("    ║    💰 Gold Storage     ⚡ Resource Trading  ║", classes="xenon-decoration")
        yield Static("    ║    💎 Gem Safes       👥 Strategic Assets  ║", classes="xenon-decoration")
        yield Static("    ╚════════════════════════════════════════════╝", classes="xenon-border")
        yield Static("═══════════════════════════════════════════════════", classes="xenon-ground")

        # Two blank lines below header
        yield Static("")
        yield Static("")

        if self.transaction_mode:
            self._compose_transaction_interface(lov.current_player)
        else:
            self._compose_main_interface(lov.current_player)

    def _compose_main_interface(self, player):
        """Compose the main storage interface"""
        # Storage status
        stored_gold = getattr(player, 'stored_gold', 0)
        stored_gems = getattr(player, 'stored_gems', 0)
        horse_name = getattr(player, 'horse_name', "")

        yield Static("Welcome to Xenon's Storage Facility, where resources are power.", classes="xenon-content")
        yield Static(f"Storage fees: 5% daily on all stored items", classes="xenon-content")
        yield Static("")

        # Current storage status
        yield Static("═ CURRENT STORAGE ═", classes="xenon-content")
        yield Static(f"Gold in storage: {stored_gold:,}", classes="xenon-content")
        yield Static(f"Gems in storage: {stored_gems:,}", classes="xenon-content")

        # Horse information
        if horse_name:
            yield Static(f"Horse: {horse_name} (Stable fees: 10 gold/day)", classes="xenon-content")
        else:
            yield Static("Horse: None (Purchase available)", classes="xenon-content")

        # Strategic resources
        yield Static(f"Children: {player.children} (Strategic value: High)", classes="xenon-content")
        yield Static("")

        # Main options
        yield Static("═ SERVICES AVAILABLE ═", classes="xenon-content")
        yield Button("(S)tore Gold", id="store_gold", disabled=player.gold <= 0)
        yield Button("(G)old Retrieval", id="retrieve_gold", disabled=stored_gold <= 0)
        yield Button("(M)anage Gems", id="store_gems", disabled=player.gems <= 0)
        yield Button("(R)etrieve Gems", id="retrieve_gems", disabled=stored_gems <= 0)

        if not horse_name:
            yield Button("(H)orse Purchase & Naming", id="name_horse", disabled=player.gold < 500)
        else:
            yield Button("(H)orse Management", id="manage_horse")

        # Dark trading option (authentic LORD feature)
        if player.children > 0:
            yield Button("(T)rade Strategic Assets", id="trade_children")

        yield Button("(L)eave facility", id="leave")

        # Status and command area
        self._compose_status_area()

    def _compose_transaction_interface(self, player):
        """Compose transaction-specific interface"""
        if self.transaction_mode == 'store_gold':
            yield Static("How much gold to store? (5% daily storage fee)", classes="xenon-content")
            yield Input(id="amount_input", placeholder="Amount to store")
            yield Static("(A)ll Gold | (Q) Cancel", classes="xenon-content")

        elif self.transaction_mode == 'retrieve_gold':
            stored_gold = getattr(player, 'stored_gold', 0)
            yield Static(f"Stored gold: {stored_gold:,}. How much to retrieve?", classes="xenon-content")
            yield Input(id="amount_input", placeholder="Amount to retrieve")
            yield Static("(A)ll Gold | (Q) Cancel", classes="xenon-content")

        elif self.transaction_mode == 'store_gems':
            yield Static("How many gems to store? (1 gem = 5 gold storage fee daily)", classes="xenon-content")
            yield Input(id="amount_input", placeholder="Gems to store")
            yield Static("(A)ll Gems | (Q) Cancel", classes="xenon-content")

        elif self.transaction_mode == 'retrieve_gems':
            stored_gems = getattr(player, 'stored_gems', 0)
            yield Static(f"Stored gems: {stored_gems}. How many to retrieve?", classes="xenon-content")
            yield Input(id="amount_input", placeholder="Gems to retrieve")
            yield Static("(A)ll Gems | (Q) Cancel", classes="xenon-content")

        elif self.transaction_mode == 'name_horse':
            yield Static("Name your horse (500 gold purchase price):", classes="xenon-content")
            yield Input(id="name_input", placeholder="Enter horse name")
            yield Static("(Q) Cancel purchase", classes="xenon-content")

        elif self.transaction_mode == 'trade_children':
            yield Static("DARK TRADING - Strategic Asset Exchange", classes="xenon-content")
            yield Static("Children can be traded for valuable resources...", classes="xenon-content")
            yield Static("Trade rates:", classes="xenon-content")
            yield Static("  1 Child = 2000 gold", classes="xenon-content")
            yield Static("  1 Child = 5 gems", classes="xenon-content")
            yield Static("  1 Child = +2 to random stat", classes="xenon-content")
            yield Static("")
            yield Static("(G)old trade | (E)m trade | (S)tat trade | (Q) Cancel", classes="xenon-content")

        self._compose_status_area()

    def _compose_status_area(self):
        """Compose the status and command prompt area"""
        # Delayed import to avoid circular dependency
        import lov

        # One blank line before status
        yield Static("")

        # Player status line
        hp_text = f"({lov.current_player.hitpoints} of {lov.current_player.max_hitpoints})"
        status_line = f"HitPoints: {hp_text}  Gold: {lov.current_player.gold}  Gems: {lov.current_player.gems}"
        yield Static(status_line, classes="xenon-status")

        # One blank line before command area
        yield Static("")

        # Command prompt area
        now = datetime.datetime.now()
        time_str = f"{now.hour:02d}:{now.minute:02d}"

        location_commands = f"Xenon's Storage (S,G,M,R,H,T,L)  (? for menu)"
        yield Static(location_commands, classes="xenon-location-commands")

        # Command prompt with time and cursor
        yield Static(f"Your command, {lov.current_player.name}? [{time_str}]: █", classes="xenon-prompt")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle storage facility selections"""
        action = event.button.id

        if action == "store_gold":
            self.transaction_mode = 'store_gold'
            self._refresh_screen()
        elif action == "retrieve_gold":
            self.transaction_mode = 'retrieve_gold'
            self._refresh_screen()
        elif action == "store_gems":
            self.transaction_mode = 'store_gems'
            self._refresh_screen()
        elif action == "retrieve_gems":
            self.transaction_mode = 'retrieve_gems'
            self._refresh_screen()
        elif action == "name_horse":
            self.transaction_mode = 'name_horse'
            self._refresh_screen()
        elif action == "manage_horse":
            self._manage_horse()
        elif action == "trade_children":
            self.transaction_mode = 'trade_children'
            self._refresh_screen()
        elif action == "leave":
            self.app.pop_screen()

    def on_key(self, event: events.Key) -> None:
        """Handle keyboard shortcuts"""
        # Delayed import to avoid circular dependency
        import lov

        key = event.key.upper()

        if self.transaction_mode:
            if key == "Q":
                self.transaction_mode = None
                self._refresh_screen()
            elif key == "A" and self.transaction_mode in ['store_gold', 'retrieve_gold', 'store_gems', 'retrieve_gems']:
                self._handle_all_transaction()
            elif self.transaction_mode == 'trade_children':
                if key == "G":
                    self._trade_child_for_gold()
                elif key == "E":
                    self._trade_child_for_gems()
                elif key == "S":
                    self._trade_child_for_stats()
        else:
            if key == "S":
                self.transaction_mode = 'store_gold'
                self._refresh_screen()
            elif key == "G":
                self.transaction_mode = 'retrieve_gold'
                self._refresh_screen()
            elif key == "M":
                self.transaction_mode = 'store_gems'
                self._refresh_screen()
            elif key == "R":
                self.transaction_mode = 'retrieve_gems'
                self._refresh_screen()
            elif key == "H":
                if not getattr(lov.current_player, 'horse_name', ""):
                    self.transaction_mode = 'name_horse'
                    self._refresh_screen()
                else:
                    self._manage_horse()
            elif key == "T":
                if lov.current_player.children > 0:
                    self.transaction_mode = 'trade_children'
                    self._refresh_screen()
            elif key == "L":
                self.app.pop_screen()
            elif key == "?":
                self.notify("S = Store gold, G = Retrieve gold, M = Manage gems, R = Retrieve gems, H = Horse, T = Trade, L = Leave")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submission for transactions"""
        # Delayed import to avoid circular dependency
        import lov

        if self.transaction_mode == 'name_horse':
            horse_name = event.value.strip()
            if len(horse_name) > 0 and len(horse_name) <= 20:
                if lov.current_player.gold >= 500:
                    lov.current_player.gold -= 500
                    lov.current_player.horse_name = horse_name
                    lov.game_db.save_player(lov.current_player)
                    self.notify(f"Congratulations! You now own {horse_name}!")
                    self.transaction_mode = None
                    self._refresh_screen()
                else:
                    self.notify("Insufficient gold for horse purchase!")
            else:
                self.notify("Invalid horse name! (1-20 characters)")
            return

        try:
            amount = int(event.value.strip())

            if amount <= 0:
                self.notify("Invalid amount!")
                return

            if self.transaction_mode == 'store_gold':
                self._store_gold(min(amount, lov.current_player.gold))
            elif self.transaction_mode == 'retrieve_gold':
                stored_gold = getattr(lov.current_player, 'stored_gold', 0)
                self._retrieve_gold(min(amount, stored_gold))
            elif self.transaction_mode == 'store_gems':
                self._store_gems(min(amount, lov.current_player.gems))
            elif self.transaction_mode == 'retrieve_gems':
                stored_gems = getattr(lov.current_player, 'stored_gems', 0)
                self._retrieve_gems(min(amount, stored_gems))

        except ValueError:
            self.notify("Please enter a valid number!")

    def _handle_all_transaction(self):
        """Handle 'all' transactions"""
        # Delayed import to avoid circular dependency
        import lov

        if self.transaction_mode == 'store_gold':
            if lov.current_player.gold > 0:
                self._store_gold(lov.current_player.gold)
        elif self.transaction_mode == 'retrieve_gold':
            stored_gold = getattr(lov.current_player, 'stored_gold', 0)
            if stored_gold > 0:
                self._retrieve_gold(stored_gold)
        elif self.transaction_mode == 'store_gems':
            if lov.current_player.gems > 0:
                self._store_gems(lov.current_player.gems)
        elif self.transaction_mode == 'retrieve_gems':
            stored_gems = getattr(lov.current_player, 'stored_gems', 0)
            if stored_gems > 0:
                self._retrieve_gems(stored_gems)

    def _store_gold(self, amount: int):
        """Store gold in the facility"""
        # Delayed import to avoid circular dependency
        import lov

        lov.current_player.gold -= amount
        if not hasattr(lov.current_player, 'stored_gold'):
            lov.current_player.stored_gold = 0
        lov.current_player.stored_gold += amount

        lov.game_db.save_player(lov.current_player)
        self.notify(f"Stored {amount:,} gold! Daily fees: {amount * 0.05:.0f} gold/day")
        self.transaction_mode = None
        self._refresh_screen()

    def _retrieve_gold(self, amount: int):
        """Retrieve gold from storage"""
        # Delayed import to avoid circular dependency
        import lov

        if not hasattr(lov.current_player, 'stored_gold'):
            lov.current_player.stored_gold = 0

        lov.current_player.stored_gold -= amount
        lov.current_player.gold += amount

        lov.game_db.save_player(lov.current_player)
        self.notify(f"Retrieved {amount:,} gold from storage!")
        self.transaction_mode = None
        self._refresh_screen()

    def _store_gems(self, amount: int):
        """Store gems in the facility"""
        # Delayed import to avoid circular dependency
        import lov

        lov.current_player.gems -= amount
        if not hasattr(lov.current_player, 'stored_gems'):
            lov.current_player.stored_gems = 0
        lov.current_player.stored_gems += amount

        lov.game_db.save_player(lov.current_player)
        self.notify(f"Stored {amount} gems! Daily fees: {amount * 5} gold/day")
        self.transaction_mode = None
        self._refresh_screen()

    def _retrieve_gems(self, amount: int):
        """Retrieve gems from storage"""
        # Delayed import to avoid circular dependency
        import lov

        if not hasattr(lov.current_player, 'stored_gems'):
            lov.current_player.stored_gems = 0

        lov.current_player.stored_gems -= amount
        lov.current_player.gems += amount

        lov.game_db.save_player(lov.current_player)
        self.notify(f"Retrieved {amount} gems from storage!")
        self.transaction_mode = None
        self._refresh_screen()

    def _manage_horse(self):
        """Manage existing horse"""
        # Delayed import to avoid circular dependency
        import lov

        horse_name = getattr(lov.current_player, 'horse_name', "")
        options = [
            f"Your horse {horse_name} is stabled here.",
            "Stable fees: 10 gold per day automatically deducted.",
            "Horses provide +1 Charm and faster travel between locations.",
            "(R)ename horse | (S)ell horse (250 gold) | (Q) Cancel"
        ]

        for option in options:
            self.notify(option)

    def _trade_child_for_gold(self):
        """Trade a child for 2000 gold"""
        # Delayed import to avoid circular dependency
        import lov

        if lov.current_player.children > 0:
            lov.current_player.children -= 1
            lov.current_player.gold += 2000
            lov.game_db.save_player(lov.current_player)
            self.notify("Strategic asset exchanged for 2000 gold.")
            self.transaction_mode = None
            self._refresh_screen()

    def _trade_child_for_gems(self):
        """Trade a child for 5 gems"""
        # Delayed import to avoid circular dependency
        import lov

        if lov.current_player.children > 0:
            lov.current_player.children -= 1
            lov.current_player.gems += 5
            lov.game_db.save_player(lov.current_player)
            self.notify("Strategic asset exchanged for 5 mystical gems.")
            self.transaction_mode = None
            self._refresh_screen()

    def _trade_child_for_stats(self):
        """Trade a child for +2 to random stat"""
        # Delayed import to avoid circular dependency
        import lov

        if lov.current_player.children > 0:
            lov.current_player.children -= 1

            # Random stat boost
            stats = ['strength', 'defense', 'charm', 'intelligence']
            chosen_stat = random.choice(stats)

            if chosen_stat == 'strength':
                lov.current_player.strength += 2
            elif chosen_stat == 'defense':
                lov.current_player.defense += 2
            elif chosen_stat == 'charm':
                lov.current_player.charm += 2
            elif chosen_stat == 'intelligence':
                lov.current_player.intelligence += 2

            lov.game_db.save_player(lov.current_player)
            self.notify(f"Strategic asset exchanged for +2 {chosen_stat}!")
            self.transaction_mode = None
            self._refresh_screen()

    def on_mount(self) -> None:
        """Focus input if in transaction mode"""
        if self.transaction_mode:
            try:
                if self.transaction_mode == 'name_horse':
                    input_widget = self.query_one("#name_input", Input)
                else:
                    input_widget = self.query_one("#amount_input", Input)
                input_widget.focus()
            except:
                pass

    def _refresh_screen(self):
        """Refresh the screen to show updated interface"""
        self.app.pop_screen()
        new_screen = XenonStorageScreen()
        new_screen.transaction_mode = self.transaction_mode
        self.app.push_screen(new_screen)
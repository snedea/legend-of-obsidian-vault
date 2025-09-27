"""
Bank screen for Legend of the Obsidian Vault - Ye Old Bank
"""
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button, Input
from textual import events


class BankScreen(Screen):
    """Ye Old Bank - Banking services with 10% daily interest"""

    def __init__(self):
        super().__init__()
        self.transaction_mode = None  # 'deposit' or 'withdraw'

    def compose(self) -> ComposeResult:
        # Delayed import to avoid circular dependency
        import lov

        yield Static("🏦 Ye Old Bank", classes="header")
        yield Static("=-" * 30, classes="separator")
        yield Static("")

        # Account status
        yield Static(f"Gold in hand: {lov.current_player.gold:,}", classes="gold")
        yield Static(f"Gold in bank: {lov.current_player.bank_gold:,}", classes="gold")
        yield Static("")
        yield Static("📈 Earn 10% interest daily on banked gold!", classes="content")
        yield Static("")

        if self.transaction_mode == 'deposit':
            yield Static("How much gold to deposit?")
            yield Input(id="amount_input", placeholder="Amount to deposit")
            yield Static("")
            yield Static("(A) Deposit All | (Q) Cancel")

        elif self.transaction_mode == 'withdraw':
            yield Static("How much gold to withdraw?")
            yield Input(id="amount_input", placeholder="Amount to withdraw")
            yield Static("")
            yield Static("(A) Withdraw All | (Q) Cancel")

        else:
            # Main menu
            yield Button("(D) Deposit Gold", id="deposit", disabled=lov.current_player.gold <= 0)
            yield Button("(W) Withdraw Gold", id="withdraw", disabled=lov.current_player.bank_gold <= 0)
            yield Static("")
            yield Static("The banker eyes your gold with interest.")
            yield Static("'Your money is safe with us, earning 10% daily!'")
            yield Static("")
            yield Static("(Q) Return to town")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle banking options"""
        if event.button.id == "deposit":
            self.transaction_mode = 'deposit'
            self._refresh_screen()
        elif event.button.id == "withdraw":
            self.transaction_mode = 'withdraw'
            self._refresh_screen()

    def _refresh_screen(self):
        """Refresh the screen to show new state"""
        self.app.pop_screen()
        from .bank import BankScreen
        new_screen = BankScreen()
        new_screen.transaction_mode = self.transaction_mode
        self.app.push_screen(new_screen)

    def on_mount(self) -> None:
        """Focus input if in transaction mode"""
        if self.transaction_mode:
            try:
                input_widget = self.query_one("#amount_input", Input)
                input_widget.focus()
            except:
                pass

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle transaction amount"""
        # Delayed import to avoid circular dependency
        import lov

        try:
            amount = int(event.value.strip())

            if amount <= 0:
                self.notify("Invalid amount!")
                return

            if self.transaction_mode == 'deposit':
                if amount > lov.current_player.gold:
                    amount = lov.current_player.gold

                if amount > 0:
                    lov.current_player.gold -= amount
                    lov.current_player.bank_gold += amount
                    lov.game_db.save_player(lov.current_player)
                    self.notify(f"Deposited {amount:,} gold!")
                    self.app.pop_screen()

            elif self.transaction_mode == 'withdraw':
                if amount > lov.current_player.bank_gold:
                    amount = lov.current_player.bank_gold

                if amount > 0:
                    lov.current_player.bank_gold -= amount
                    lov.current_player.gold += amount
                    lov.game_db.save_player(lov.current_player)
                    self.notify(f"Withdrew {amount:,} gold!")
                    self.app.pop_screen()

        except ValueError:
            self.notify("Please enter a valid number!")

    def on_key(self, event: events.Key) -> None:
        key = event.key.upper()

        if key == "Q":
            if self.transaction_mode:
                # Cancel transaction mode
                self.transaction_mode = None
                self._refresh_screen()
            else:
                # Return to town
                self.app.pop_screen()

        elif key == "D" and not self.transaction_mode:
            # Start deposit
            self.transaction_mode = 'deposit'
            self._refresh_screen()

        elif key == "W" and not self.transaction_mode:
            # Start withdraw
            self.transaction_mode = 'withdraw'
            self._refresh_screen()

        elif key == "A" and self.transaction_mode:
            # All deposits/withdrawals
            import lov

            if self.transaction_mode == 'deposit' and lov.current_player.gold > 0:
                amount = lov.current_player.gold
                lov.current_player.bank_gold += amount
                lov.current_player.gold = 0
                lov.game_db.save_player(lov.current_player)
                self.notify(f"Deposited all {amount:,} gold!")
                self.app.pop_screen()

            elif self.transaction_mode == 'withdraw' and lov.current_player.bank_gold > 0:
                amount = lov.current_player.bank_gold
                lov.current_player.gold += amount
                lov.current_player.bank_gold = 0
                lov.game_db.save_player(lov.current_player)
                self.notify(f"Withdrew all {amount:,} gold!")
                self.app.pop_screen()
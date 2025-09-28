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

            # Show different messages for thieves with special abilities
            if (lov.current_player.class_type == "D" and
                lov.current_player.fairy_lore and
                lov.current_player.bank_robberies_today == 0):
                yield Static("The banker seems distracted by paperwork...")
                yield Static("You notice the vault door is slightly ajar.")
                yield Static("Your fairy magic tingles - you sense opportunity.")
            else:
                yield Static("The banker eyes your gold with interest.")
                yield Static("'Your money is safe with us, earning 10% daily!'")

            yield Static("")
            yield Static("(Q) Return to town")

            # Hidden robbery option for qualified thieves
            if (lov.current_player.class_type == "D" and
                lov.current_player.fairy_lore and
                lov.current_player.bank_robberies_today == 0):
                yield Static("", classes="content")  # Blank line for spacing

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

        elif key == "R" and not self.transaction_mode:
            # Hidden robbery option for thieves with fairy lore
            import lov
            if (lov.current_player.class_type == "D" and
                lov.current_player.fairy_lore and
                lov.current_player.bank_robberies_today == 0):
                self._attempt_bank_robbery()
            else:
                self.notify("The guards look at you suspiciously...")

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

    def _attempt_bank_robbery(self):
        """Attempt to rob the bank using thief skills and fairy magic"""
        # Delayed import to avoid circular dependency
        import lov
        import random

        # Mark that a robbery attempt was made today
        lov.current_player.bank_robberies_today += 1

        self.notify("You silently approach the vault...")
        self.notify("Your fairy magic helps you sense the magical locks...")

        # Calculate success chance based on thieving points and level
        base_chance = 30  # 30% base chance
        thief_bonus = lov.current_player.thieving_points * 5  # 5% per thieving point
        level_bonus = lov.current_player.level * 2  # 2% per level

        success_chance = min(80, base_chance + thief_bonus + level_bonus)  # Cap at 80%

        roll = random.randint(1, 100)

        if roll <= success_chance:
            # Successful robbery!
            self._successful_robbery()
        else:
            # Failed robbery!
            self._failed_robbery()

        lov.game_db.save_player(lov.current_player)

    def _successful_robbery(self):
        """Handle successful bank robbery"""
        # Delayed import to avoid circular dependency
        import lov
        import random

        # Calculate total gold in bank (simplified - use current player's bank as base)
        total_bank_gold = max(1000, lov.current_player.bank_gold * 5)  # Simulate other players' deposits

        # Steal 10-30% of total bank gold
        steal_percentage = random.randint(10, 30)
        stolen_gold = int(total_bank_gold * steal_percentage / 100)

        lov.current_player.gold += stolen_gold
        lov.current_player.successful_robberies += 1

        self.notify("✨ SUCCESS! ✨")
        self.notify("Your fairy magic guides you past the enchanted locks!")
        self.notify(f"You grab {stolen_gold:,} gold and slip away into the shadows!")
        self.notify("The banker won't notice until morning...")

        # Small boost to thieving for successful heist
        lov.current_player.thieving_points += 1
        self.notify("Your thieving skills improve from this daring heist! (+1 Thieving)")

        # Return to town square to avoid suspicion
        import time
        self.app.call_later(3, self.app.pop_screen)

    def _failed_robbery(self):
        """Handle failed bank robbery"""
        # Delayed import to avoid circular dependency
        import lov
        import random

        failure_messages = [
            "A magical alarm sounds! The fairy locks were more complex than expected!",
            "You trigger a ward that alerts the guards!",
            "Your fairy magic backfires, causing a bright flash!",
            "The vault door slams shut with a thunderous boom!"
        ]

        penalty_message = random.choice(failure_messages)
        self.notify("💀 CAUGHT! 💀")
        self.notify(penalty_message)

        # Penalty: Lose half current gold as fine
        penalty = lov.current_player.gold // 2
        lov.current_player.gold -= penalty

        if penalty > 0:
            self.notify(f"The guards confiscate {penalty:,} gold as punishment!")
        else:
            self.notify("Fortunately, you have no gold for them to confiscate.")

        self.notify("You are roughly escorted from the bank!")
        self.notify("'Don't let us catch you in here again today!' the guard warns.")

        # Return to town square in shame
        import time
        self.app.call_later(3, self.app.pop_screen)
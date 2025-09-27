"""
Bribe screen for Legend of the Obsidian Vault
"""
from typing import List
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static
from textual import events


class BribeScreen(Screen):
    """Screen for bribing bartender to kill players"""

    def __init__(self, targets: List, cost: int):
        super().__init__()
        self.targets = targets
        self.cost = cost

    def compose(self) -> ComposeResult:
        yield Static("Sleeping Targets", classes="header")
        yield Static("=-" * 30, classes="separator")
        yield Static("")
        yield Static(f"Bribe cost: {self.cost} gold")
        yield Static("")

        if not self.targets:
            yield Static("No one is sleeping at the inn tonight.")
        else:
            yield Static("Choose your target:")
            for i, target in enumerate(self.targets):
                yield Static(f"({i + 1}) {target.name} - Level {target.level}")

        yield Static("")
        yield Static("(Q) Cancel")

    def on_key(self, event: events.Key) -> None:
        # Delayed import to avoid circular dependency
        import lov

        key = event.key.upper()

        if key == "Q":
            self.app.pop_screen()
        elif key.isdigit():
            index = int(key) - 1
            if 0 <= index < len(self.targets):
                target = self.targets[index]
                lov.current_player.gold -= self.cost

                # Simplified kill mechanics for now
                self.notify(f"The bartender slips a knife between {target.name}'s ribs...")
                self.notify(f"{target.name} has been eliminated!")

                # Award experience and gold
                exp_gain = target.level * 50
                gold_gain = target.gold // 2
                lov.current_player.experience += exp_gain
                lov.current_player.gold += gold_gain
                lov.current_player.total_kills += 1

                # Reset target's inn status and reduce their stats
                target.inn_room = False
                target.alive = False
                lov.game_db.save_player(target)
                lov.game_db.save_player(lov.current_player)

                self.notify(f"You gain {exp_gain} experience and {gold_gain} gold!")
                self.app.pop_screen()
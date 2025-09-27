"""
Bar Room screen for Legend of the Obsidian Vault
"""
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static
from textual import events


class BarRoomScreen(Screen):
    """Bar Room - Bartender interactions"""

    def compose(self) -> ComposeResult:
        # Delayed import to avoid circular dependency
        import lov

        # Check if player is level 1 (bartender won't talk to them)
        if lov.current_player.level == 1:
            yield Static("The Bar Room", classes="header")
            yield Static("=-" * 30, classes="separator")
            yield Static("")
            yield Static("The bartender glances at you dismissively.")
            yield Static("'Get out of here, kid. Come back when you've")
            yield Static("proven yourself in the forest.'")
            yield Static("")
            yield Static("Press any key to return...")
        else:
            yield Static("The Bar Room", classes="header")
            yield Static("=-" * 30, classes="separator")
            yield Static("")
            yield Static("The gruff bartender eyes you carefully.")
            yield Static("'What'll it be, warrior?'")
            yield Static("")
            yield Static("(G)ems for stats (2 gems)")
            yield Static("(R)oom for the night")
            yield Static("(B)ribe me to kill sleeping players")
            yield Static("(N)ame change")
            yield Static("(Q) Return to inn")

    def on_key(self, event: events.Key) -> None:
        # Delayed import to avoid circular dependency
        import lov

        key = event.key.upper()

        if key == "Q":
            self.app.pop_screen()
        elif lov.current_player.level == 1:
            self.app.pop_screen()
        elif key == "G":
            self._gem_trading()
        elif key == "R":
            self._rent_room()
        elif key == "B":
            self._bribe_bartender()
        elif key == "N":
            self._change_name()

    def _gem_trading(self):
        """Trade gems for stat points"""
        import lov

        if lov.current_player.gems < 2:
            self.notify("You need at least 2 gems!")
            return

        # Show gem trading options
        from .gem_trading import GemTradingScreen
        self.app.push_screen(GemTradingScreen())

    def _rent_room(self):
        """Rent a room at the inn"""
        import lov
        from game_data import INN_ROOM_COSTS

        if lov.current_player.inn_room:
            self.notify("You already have a room for tonight!")
            return

        cost = INN_ROOM_COSTS[min(lov.current_player.level - 1, 11)]

        # Free if charm > 100
        if lov.current_player.charm > 100:
            lov.current_player.inn_room = True
            lov.game_db.save_player(lov.current_player)
            self.notify("'No charge for such a charming warrior!'")
            self.notify("You have a room for tonight.")
        elif lov.current_player.gold >= cost:
            lov.current_player.gold -= cost
            lov.current_player.inn_room = True
            lov.game_db.save_player(lov.current_player)
            self.notify(f"'That'll be {cost} gold pieces.'")
            self.notify("You have a room for tonight.")
        else:
            self.notify(f"You need {cost} gold pieces for a room.")

    def _bribe_bartender(self):
        """Bribe bartender to kill sleeping players"""
        import lov
        from game_data import BRIBE_COSTS

        cost = BRIBE_COSTS[min(lov.current_player.level - 1, 11)]

        if lov.current_player.gold < cost:
            self.notify(f"You need {cost} gold to bribe me!")
            return

        # Get players at inn
        sleeping_players = lov.game_db.get_players_at_inn()
        # Filter out players more than 1 level below (can't kill them)
        valid_targets = [p for p in sleeping_players
                        if p.name != lov.current_player.name and
                        p.level >= lov.current_player.level - 1]

        if not valid_targets:
            self.notify("No suitable targets at the inn tonight.")
            return

        from .bribe import BribeScreen
        self.app.push_screen(BribeScreen(valid_targets, cost))

    def _change_name(self):
        """Change player name"""
        from .name_change import NameChangeScreen
        self.app.push_screen(NameChangeScreen())
"""
Town Square screen for Legend of the Obsidian Vault - Main hub
"""
import datetime
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button
from textual.containers import Horizontal, Vertical, Container, VerticalScroll
from textual import events


class TownSquareScreen(Screen):
    """Main town square with all LORD menu options"""

    def compose(self) -> ComposeResult:
        # Delayed import to avoid circular dependency
        import lov

        with Container(classes="main-border") as container:
            container.border_title = "🏰  TOWN SQUARE  🏰"
            container.border_subtitle = "⚔️ Hub of Adventure ⚔️"
            yield Static("The Legend of the Red Dragon - Town Square", classes="header")
            yield Static("=-" * 60, classes="separator")
            yield Static("The streets are crowded, it is difficult to")
            yield Static("push your way through the mob....")
            yield Static("")

            # Main menu options - 3-column layout with scrolling
            with VerticalScroll(classes="town-scroll"):
                with Horizontal():
                    with Vertical():
                        # First column - 7 buttons
                        yield Button("(F)orest", id="forest")
                        yield Button("(S)laughter other players", id="pvp")
                        yield Button("(K)ing Arthurs Weapons", id="weapons")
                        yield Button("(A)bduls Armour", id="armor")
                        yield Button("(H)ealers Hut", id="healer")
                        yield Button("(V)iew your stats", id="stats")
                        yield Button("(I)nn", id="inn")

                    with Vertical():
                        # Second column - 6 buttons
                        yield Button("(T)urgons Warrior Training", id="training")
                        yield Button("(Y)e Old Bank", id="bank")
                        yield Button("(L)ist Warriors", id="list")
                        yield Button("(W)rite Mail", id="mail")
                        yield Button("(D)aily News", id="news")
                        yield Button("(C)onjugality List", id="marriage")

                    with Vertical():
                        # Third column - 6 buttons
                        yield Button("(O)ther Places", id="other")
                        yield Button("(N)otes in the Vault", id="notes")
                        yield Button("(M)ake Announcement", id="announce")
                        yield Button("(X)pert Mode", id="expert")
                        yield Button("(P)eople Online", id="online")
                        yield Button("(Q)uit to Fields", id="quit")

            yield Static("")
            yield Static("The Town Square  (? for menu)")
            yield Static(f"(F,S,K,A,H,V,R,T,Y,L,W,D,C,N,O,X,M,P,Q)")
            yield Static("")

            # Status line
            if lov.current_player:
                time_left = f"{lov.current_player.forest_fights:02d}:{lov.current_player.player_fights:02d}"
                yield Static(f"Your command, {lov.current_player.name}? [{time_left}] :", classes="prompt")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses for touchscreen/mouse support"""
        self._handle_menu_action(event.button.id)

    def _handle_menu_action(self, action: str) -> None:
        """Handle menu action for both keyboard and button presses"""
        # Delayed import to avoid circular dependency
        import lov
        from screens.combat.forest import ForestScreen

        if action == "forest":
            self.app.push_screen(ForestScreen())
        elif action == "stats":
            from .stats import StatsScreen
            self.app.push_screen(StatsScreen())
        elif action == "inn":
            from .inn import InnScreen
            self.app.push_screen(InnScreen())
        elif action == "weapons":
            from .weapons import WeaponsScreen
            self.app.push_screen(WeaponsScreen())
        elif action == "armor":
            from .armor import ArmorScreen
            self.app.push_screen(ArmorScreen())
        elif action == "bank":
            from .bank import BankScreen
            self.app.push_screen(BankScreen())
        elif action == "healer":
            from .healer import HealerScreen
            self.app.push_screen(HealerScreen())
        elif action == "training":
            # TurgonsTrainingScreen is still in main lov module
            self.app.push_screen(lov.TurgonsTrainingScreen())
        elif action == "list":
            # WarriorListScreen is still in main lov module
            self.app.push_screen(lov.WarriorListScreen())
        elif action == "notes":
            # NotesViewerScreen is still in main lov module
            self.app.push_screen(lov.NotesViewerScreen())
        elif action == "other":
            # Other Places IGM menu
            from screens.igm.other_places import OtherPlacesScreen
            self.app.push_screen(OtherPlacesScreen())
        elif action == "quit":
            lov.game_db.save_player(lov.current_player)
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
            self._handle_menu_action(menu_map[key])
"""
Other Places IGM Menu for Legend of the Obsidian Vault
Gateway to all In-Game Modules and special locations
"""
import datetime
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button
from textual.containers import Vertical, Container
from textual import events


class OtherPlacesScreen(Screen):
    """Other Places - Gateway to IGMs and special locations"""

    def compose(self) -> ComposeResult:
        # Delayed import to avoid circular dependency
        import lov

        with Container(classes="main-border") as container:
            container.border_title = "🌍 OTHER PLACES 🌍"
            container.border_subtitle = "🗺️ Realm Gateways 🗺️"

            # Header
            yield Static("✦ OTHER PLACES - REALM GATEWAYS ✦", classes="header")
            yield Static("═" * 40, classes="separator")
            yield Static("🌟 Special locations beyond the town square 🌟", classes="other-subtitle")
            yield Static("")

            # Main menu options
            yield Static("Available Destinations:", classes="other-content")
            yield Static("")

            # IGM options
            yield Button("(B)arak's House - Scholar & Gambling Den", id="barak")
            yield Button("(C)avern Entrance - Hidden from Forest", id="cavern")
            yield Button("(H)all of Honours - Dragon Slayers", id="hall")
            yield Button("(F)airy Garden - Learn Healing Arts", id="fairy")
            yield Button("(X)enon's Storage - Resource Management", id="xenon")
            yield Button("(W)ereWolf Den - Primal Transformation", id="werewolf")
            yield Button("(G)ateway Portal - Dimensional Travel", id="gateway")
            yield Static("")

            # Return option
            yield Button("(R)eturn to Town Square", id="return")

            # Status and command area
            yield Static("")
            hp_text = f"({lov.current_player.hitpoints} of {lov.current_player.max_hitpoints})"
            status_line = f"HitPoints: {hp_text}  Gold: {lov.current_player.gold}  Gems: {lov.current_player.gems}"
            yield Static(status_line, classes="stats")

            yield Static("")
            now = datetime.datetime.now()
            time_str = f"{now.hour:02d}:{now.minute:02d}"
            yield Static("Other Places (B,C,H,F,X,W,G,R)  (? for menu)", classes="other-location-commands")
            yield Static(f"Your command, {lov.current_player.name}? [{time_str}]: █", classes="prompt")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle IGM selections"""
        # Delayed import to avoid circular dependency
        import lov

        action = event.button.id

        if action == "barak":
            from .barak_house import BarakHouseScreen
            self.app.push_screen(BarakHouseScreen())
        elif action == "cavern":
            from .cavern import CavernScreen
            self.app.push_screen(CavernScreen())
        elif action == "hall":
            # Hall of Honours is still in main lov module
            self.app.push_screen(lov.HallOfHonoursScreen())
        elif action == "fairy":
            from .fairy_garden import FairyGardenScreen
            self.app.push_screen(FairyGardenScreen())
        elif action == "xenon":
            from .xenon_storage import XenonStorageScreen
            self.app.push_screen(XenonStorageScreen())
        elif action == "werewolf":
            from .werewolf_den import WereWolfDenScreen
            self.app.push_screen(WereWolfDenScreen())
        elif action == "gateway":
            from .gateway_portal import GatewayPortalScreen
            self.app.push_screen(GatewayPortalScreen())
        elif action == "return":
            self.app.pop_screen()

    def on_key(self, event: events.Key) -> None:
        """Handle keyboard shortcuts"""
        # Delayed import to avoid circular dependency
        import lov

        key = event.key.upper()

        if key == "B":
            from .barak_house import BarakHouseScreen
            self.app.push_screen(BarakHouseScreen())
        elif key == "C":
            from .cavern import CavernScreen
            self.app.push_screen(CavernScreen())
        elif key == "H":
            self.app.push_screen(lov.HallOfHonoursScreen())
        elif key == "F":
            from .fairy_garden import FairyGardenScreen
            self.app.push_screen(FairyGardenScreen())
        elif key == "X":
            from .xenon_storage import XenonStorageScreen
            self.app.push_screen(XenonStorageScreen())
        elif key == "W":
            from .werewolf_den import WereWolfDenScreen
            self.app.push_screen(WereWolfDenScreen())
        elif key == "G":
            from .gateway_portal import GatewayPortalScreen
            self.app.push_screen(GatewayPortalScreen())
        elif key == "R":
            self.app.pop_screen()
        elif key == "?":
            self.notify("B = Barak, C = Cavern, H = Hall, F = Fairy, X = Xenon, W = Wolf, G = Gateway, R = Return")
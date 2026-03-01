from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

# Add project root to path so we can import game_data, obsidian, brainbot
_project_root = str(Path(__file__).resolve().parent.parent.parent)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from game_data import GameDatabase, Character, GameSettings


class GameSession:
    """Single-player game session wrapping GameDatabase and current player state."""

    def __init__(self) -> None:
        self.db = GameDatabase()
        self.player: Optional[Character] = None
        self.settings = GameSettings.load()

    def create_player(self, name: str, gender: str, class_type: str) -> Character:
        player = Character(name=name, gender=gender, class_type=class_type)
        self.db.save_player(player)
        self.player = player
        return player

    def select_player(self, name: str) -> Optional[Character]:
        player = self.db.load_player(name)
        if player:
            self.player = player
        return player

    def list_players(self) -> list[Character]:
        return self.db.get_all_players()

    def save_player(self) -> None:
        if self.player:
            self.db.save_player(self.player)

    def require_player(self) -> Character:
        if self.player is None:
            raise ValueError("No player selected")
        return self.player


# Global singleton
session = GameSession()

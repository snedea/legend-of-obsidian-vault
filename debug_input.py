#!/usr/bin/env python3
"""
Debug script to test Textual input handling
"""

from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Header, Footer, Static, Button
from textual.screen import Screen
from textual import events

class DebugScreen(Screen):
    """Simple debug screen to test input"""

    can_focus = True

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Debug Input Test", classes="title")
        yield Static("")
        yield Static("This tests if keyboard/mouse input works:")
        yield Static("")
        yield Button("Click me!", id="test_button")
        yield Static("")
        yield Static("Press any key - should show message below:")
        yield Static("", id="debug_output")
        yield Footer()

    def on_mount(self) -> None:
        self.focus()
        self.notify("Screen loaded - try clicking or pressing keys")

    def on_key(self, event: events.Key) -> None:
        output = self.query_one("#debug_output", Static)
        output.update(f"✅ Key pressed: '{event.key}' - keyboard input works!")
        self.notify(f"Key: {event.key}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        output = self.query_one("#debug_output", Static)
        output.update(f"✅ Button clicked: {event.button.id} - mouse input works!")
        self.notify("Button clicked!")

    def on_click(self, event) -> None:
        self.notify("Mouse click detected anywhere on screen")

class DebugApp(App):
    """Simple debug app"""

    def on_mount(self) -> None:
        self.push_screen(DebugScreen())

if __name__ == "__main__":
    app = DebugApp()
    app.run()
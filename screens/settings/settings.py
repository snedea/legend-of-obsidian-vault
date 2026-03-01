"""
Settings screen for Legend of the Obsidian Vault
Configure game options including enemy difficulty mode and AI provider
"""
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button, Input
from textual.containers import Container
from textual import events

from game_data import game_settings, DifficultyMode, GameSettings, AIProviderType, CLAUDE_MODELS


class SettingsScreen(Screen):
    """Game Settings - Configure difficulty and other options"""

    def compose(self) -> ComposeResult:
        current_mode = game_settings.difficulty_mode
        current_provider = game_settings.ai_provider

        # Get provider display name
        provider_names = {
            AIProviderType.TINYLLAMA: "TinyLlama (Local)",
            AIProviderType.CLAUDE_CLI: "Claude CLI",
            AIProviderType.CLAUDE_API: "Claude API",
            AIProviderType.OLLAMA: "Ollama (Remote GPU)",
        }

        with Container(classes="main-border") as container:
            container.border_title = "GAME SETTINGS"
            container.border_subtitle = "Configure Your Adventure"

            # ASCII Art Header - Settings Gear Theme
            yield Static("[cyan]          ___  SETTINGS ARCANUM  ___[/cyan]", classes="settings-header")
            yield Static("")
            yield Static("[yellow]                  _____[/yellow]")
            yield Static("[yellow]              ,-~'     '~-,[/yellow]")
            yield Static("[yellow]            ,'    [/yellow][white]_____[/white][yellow]    ',[/yellow]")
            yield Static("[yellow]           /    [/yellow][white]/     \\[/white][yellow]    \\[/yellow]")
            yield Static("[yellow]          |    [/yellow][white]| [/white][cyan]O[/cyan][white]   |[/white][yellow]    |[/yellow]")
            yield Static("[yellow]          |    [/yellow][white]|  [/white][cyan]O[/cyan][white]  |[/white][yellow]    |[/yellow]")
            yield Static("[yellow]          |    [/yellow][white]|   [/white][cyan]O[/cyan][white] |[/white][yellow]    |[/yellow]")
            yield Static("[yellow]           \\    [/yellow][white]\\_____/[/white][yellow]    /[/yellow]")
            yield Static("[yellow]            ',[/yellow][white]==========[/white][yellow],'[/yellow]")
            yield Static("[yellow]              '-,_____,-'[/yellow]")
            yield Static("")
            yield Static("[cyan]     'Adjust the mystical gears of your adventure.'[/cyan]")
            yield Static("")
            yield Static("[white]=-[/white]" * 24, classes="separator")
            yield Static("")

            # Current AI Provider Status Display
            yield Static(f"[green]  Current AI Provider:[/green] [bold white]{provider_names[current_provider]}[/bold white]")
            yield Static("")

            # Current mode display
            mode_names = {
                DifficultyMode.AGE_BASED: "Age-Based (Older notes = Harder)",
                DifficultyMode.RANDOM: "Random (Chaos mode)",
                DifficultyMode.PLAYER_LEVEL: "Player Level (Balanced)",
                DifficultyMode.CONTENT_COMPLEXITY: "Content Complexity",
                DifficultyMode.AI_DETERMINED: "AI-Determined (Mixed factors)"
            }
            yield Static(f"[green]  Difficulty Mode:[/green] [bold white]{mode_names[current_mode]}[/bold white]")
            yield Static("")
            yield Static("[white]=-[/white]" * 24, classes="separator")
            yield Static("")

            yield Static("[yellow]  --- ENEMY DIFFICULTY OPTIONS ---[/yellow]")
            yield Static("")

            # Age-based option
            marker = "[bold cyan]>[/bold cyan]" if current_mode == DifficultyMode.AGE_BASED else " "
            yield Button(
                f"(1) Age-Based - Older notes spawn harder enemies",
                id="mode_age",
                classes="settings-option" + (" selected" if current_mode == DifficultyMode.AGE_BASED else "")
            )

            # Random option
            marker = "[bold cyan]>[/bold cyan]" if current_mode == DifficultyMode.RANDOM else " "
            yield Button(
                f"(2) Random - Pure chaos, any difficulty",
                id="mode_random",
                classes="settings-option" + (" selected" if current_mode == DifficultyMode.RANDOM else "")
            )

            # Player Level option
            marker = "[bold cyan]>[/bold cyan]" if current_mode == DifficultyMode.PLAYER_LEVEL else " "
            yield Button(
                f"(3) Player Level - Enemies scale to you",
                id="mode_player",
                classes="settings-option" + (" selected" if current_mode == DifficultyMode.PLAYER_LEVEL else "")
            )

            # Content Complexity option
            marker = "[bold cyan]>[/bold cyan]" if current_mode == DifficultyMode.CONTENT_COMPLEXITY else " "
            yield Button(
                f"(4) Content Complexity - Detailed notes = harder",
                id="mode_content",
                classes="settings-option" + (" selected" if current_mode == DifficultyMode.CONTENT_COMPLEXITY else "")
            )

            # AI-Determined option
            marker = "[bold cyan]>[/bold cyan]" if current_mode == DifficultyMode.AI_DETERMINED else " "
            yield Button(
                f"(5) AI-Determined - Multiple factors",
                id="mode_ai",
                classes="settings-option" + (" selected" if current_mode == DifficultyMode.AI_DETERMINED else "")
            )

            yield Static("")
            yield Static("[white]=-[/white]" * 24, classes="separator")
            yield Static("")
            yield Static("  [bold yellow](A)[/bold yellow] AI Provider Settings", classes="settings-return")
            yield Static("  [bold yellow](Q)[/bold yellow] Return to Town", classes="settings-return")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle difficulty mode selection"""
        mode_map = {
            "mode_age": DifficultyMode.AGE_BASED,
            "mode_random": DifficultyMode.RANDOM,
            "mode_player": DifficultyMode.PLAYER_LEVEL,
            "mode_content": DifficultyMode.CONTENT_COMPLEXITY,
            "mode_ai": DifficultyMode.AI_DETERMINED
        }

        if event.button.id in mode_map:
            game_settings.difficulty_mode = mode_map[event.button.id]
            game_settings.save()
            self._refresh_screen()

    def _refresh_screen(self):
        """Refresh the screen to show updated settings"""
        self.app.pop_screen()
        self.app.push_screen(SettingsScreen())

    def on_key(self, event: events.Key) -> None:
        """Handle keyboard shortcuts"""
        key = event.key.lower()

        if key == "q" or key == "escape":
            self.app.pop_screen()
        elif key == "a":
            self.app.push_screen(AISettingsScreen())
        elif key == "1":
            game_settings.difficulty_mode = DifficultyMode.AGE_BASED
            game_settings.save()
            self._refresh_screen()
        elif key == "2":
            game_settings.difficulty_mode = DifficultyMode.RANDOM
            game_settings.save()
            self._refresh_screen()
        elif key == "3":
            game_settings.difficulty_mode = DifficultyMode.PLAYER_LEVEL
            game_settings.save()
            self._refresh_screen()
        elif key == "4":
            game_settings.difficulty_mode = DifficultyMode.CONTENT_COMPLEXITY
            game_settings.save()
            self._refresh_screen()
        elif key == "5":
            game_settings.difficulty_mode = DifficultyMode.AI_DETERMINED
            game_settings.save()
            self._refresh_screen()


class AISettingsScreen(Screen):
    """AI Provider Settings - Configure which AI to use for quiz and narrative generation"""

    def __init__(self):
        super().__init__()
        self._editing_api_key = False
        self._api_key_input = ""

    def compose(self) -> ComposeResult:
        current_provider = game_settings.ai_provider
        current_model = game_settings.claude_model

        # Get model display name
        model_display = current_model
        for model_id, model_name in CLAUDE_MODELS:
            if model_id == current_model:
                model_display = model_name
                break

        # Mask API key for display
        api_key = game_settings.claude_api_key
        if api_key:
            masked_key = f"{api_key[:10]}...{api_key[-4:]}" if len(api_key) > 14 else "****"
        else:
            masked_key = "(not set)"

        with Container(classes="main-border") as container:
            container.border_title = "AI ORACLE SETTINGS"
            container.border_subtitle = "Configure the Mind Behind the Magic"

            # Provider-specific ASCII Art Headers
            if current_provider == AIProviderType.TINYLLAMA:
                # BrainBot ASCII Art for TinyLlama
                yield Static("[cyan]  ╔═══════════════════════════════════════════╗[/cyan]")
                yield Static("[cyan]  ║[/cyan][yellow]     _____  _____   _____ _   _ _____      [/yellow][cyan]║[/cyan]")
                yield Static("[cyan]  ║[/cyan][yellow]    | __  ||  _  | |_   _| \\ | |_   _|     [/yellow][cyan]║[/cyan]")
                yield Static("[cyan]  ║[/cyan][yellow]    | __ -||     |   | | |  \\| | | |       [/yellow][cyan]║[/cyan]")
                yield Static("[cyan]  ║[/cyan][yellow]    |_____||__|__|   |_| |_|\\__| |_|       [/yellow][cyan]║[/cyan]")
                yield Static("[cyan]  ║[/cyan]                                           [cyan]║[/cyan]")
                yield Static("[cyan]  ║[/cyan][white]        ┌──────────────────────┐           [/white][cyan]║[/cyan]")
                yield Static("[cyan]  ║[/cyan][white]        │  [/white][green]◉[/green][white]    BRAIN    [/white][green]◉[/green][white]    │           [/white][cyan]║[/cyan]")
                yield Static("[cyan]  ║[/cyan][white]        │ [/white][magenta]╔══╗[/magenta][white]  BOT    [/white][magenta]╔══╗[/magenta][white]   │           [/white][cyan]║[/cyan]")
                yield Static("[cyan]  ║[/cyan][white]        │ [/white][magenta]║▓▓║[/magenta][white] ~~~~~~~ [/white][magenta]║▓▓║[/magenta][white]   │           [/white][cyan]║[/cyan]")
                yield Static("[cyan]  ║[/cyan][white]        │ [/white][magenta]╚══╝[/magenta][white]         [/white][magenta]╚══╝[/magenta][white]   │           [/white][cyan]║[/cyan]")
                yield Static("[cyan]  ║[/cyan][white]        │   ╲    [/white][yellow]___[/yellow][white]    ╱     │           [/white][cyan]║[/cyan]")
                yield Static("[cyan]  ║[/cyan][white]        │    ╲__│   │__╱      │           [/white][cyan]║[/cyan]")
                yield Static("[cyan]  ║[/cyan][white]        └──────────────────────┘           [/white][cyan]║[/cyan]")
                yield Static("[cyan]  ║[/cyan][green]      TinyLlama AI Narrative Engine        [/green][cyan]║[/cyan]")
                yield Static("[cyan]  ╚═══════════════════════════════════════════╝[/cyan]")
                yield Static("")
            elif current_provider == AIProviderType.CLAUDE_CLI:
                # Claude CLI Art
                yield Static("[magenta]  ╔═══════════════════════════════════════════╗[/magenta]")
                yield Static("[magenta]  ║[/magenta][white]      _____ _                 _           [/white][magenta]║[/magenta]")
                yield Static("[magenta]  ║[/magenta][white]     / ____| |               | |          [/white][magenta]║[/magenta]")
                yield Static("[magenta]  ║[/magenta][white]    | |    | | __ _ _   _  __| | ___      [/white][magenta]║[/magenta]")
                yield Static("[magenta]  ║[/magenta][white]    | |    | |/ _` | | | |/ _` |/ _ \\     [/white][magenta]║[/magenta]")
                yield Static("[magenta]  ║[/magenta][white]    | |____| | (_| | |_| | (_| |  __/     [/white][magenta]║[/magenta]")
                yield Static("[magenta]  ║[/magenta][white]     \\_____|_|\\__,_|\\__,_|\\__,_|\\___|     [/white][magenta]║[/magenta]")
                yield Static("[magenta]  ║[/magenta]                                           [magenta]║[/magenta]")
                yield Static("[magenta]  ║[/magenta][yellow]            ┌─────────────┐               [/yellow][magenta]║[/magenta]")
                yield Static("[magenta]  ║[/magenta][yellow]            │  [/yellow][cyan]CLI MODE[/cyan][yellow]  │               [/yellow][magenta]║[/magenta]")
                yield Static("[magenta]  ║[/magenta][yellow]            │   [/yellow][white]>_[/white][yellow]       │               [/yellow][magenta]║[/magenta]")
                yield Static("[magenta]  ║[/magenta][yellow]            └─────────────┘               [/yellow][magenta]║[/magenta]")
                yield Static("[magenta]  ║[/magenta][cyan]       Anthropic CLI Subscription          [/cyan][magenta]║[/magenta]")
                yield Static("[magenta]  ╚═══════════════════════════════════════════╝[/magenta]")
                yield Static("")
            elif current_provider == AIProviderType.OLLAMA:
                # Ollama Art
                yield Static("[green]  ╔═══════════════════════════════════════════╗[/green]")
                yield Static("[green]  ║[/green][yellow]       ___  _ _                            [/yellow][green]║[/green]")
                yield Static("[green]  ║[/green][yellow]      / _ \\| | |__ _ _ __  __ _            [/yellow][green]║[/green]")
                yield Static("[green]  ║[/green][yellow]     | (_) | | / _` | '  \\/ _` |           [/yellow][green]║[/green]")
                yield Static("[green]  ║[/green][yellow]      \\___/|_|_\\__,_|_|_|_\\__,_|           [/yellow][green]║[/green]")
                yield Static("[green]  ║[/green]                                           [green]║[/green]")
                yield Static("[green]  ║[/green][white]            ┌─────────────┐               [/white][green]║[/green]")
                yield Static("[green]  ║[/green][white]            │  [/white][cyan]GPU MODE[/cyan][white]  │               [/white][green]║[/green]")
                yield Static("[green]  ║[/green][white]            │   [/white][yellow]🦙[/yellow][white]       │               [/white][green]║[/green]")
                yield Static("[green]  ║[/green][white]            └─────────────┘               [/white][green]║[/green]")
                yield Static("[green]  ║[/green][cyan]       Remote GPU Inference Engine          [/cyan][green]║[/green]")
                yield Static("[green]  ╚═══════════════════════════════════════════╝[/green]")
                yield Static("")
            else:
                # Claude API Art
                yield Static("[yellow]  ╔═══════════════════════════════════════════╗[/yellow]")
                yield Static("[yellow]  ║[/yellow][white]      _____ _                 _           [/white][yellow]║[/yellow]")
                yield Static("[yellow]  ║[/yellow][white]     / ____| |               | |          [/white][yellow]║[/yellow]")
                yield Static("[yellow]  ║[/yellow][white]    | |    | | __ _ _   _  __| | ___      [/white][yellow]║[/yellow]")
                yield Static("[yellow]  ║[/yellow][white]    | |    | |/ _` | | | |/ _` |/ _ \\     [/white][yellow]║[/yellow]")
                yield Static("[yellow]  ║[/yellow][white]    | |____| | (_| | |_| | (_| |  __/     [/white][yellow]║[/yellow]")
                yield Static("[yellow]  ║[/yellow][white]     \\_____|_|\\__,_|\\__,_|\\__,_|\\___|     [/white][yellow]║[/yellow]")
                yield Static("[yellow]  ║[/yellow]                                           [yellow]║[/yellow]")
                yield Static("[yellow]  ║[/yellow][magenta]            ┌─────────────┐               [/magenta][yellow]║[/yellow]")
                yield Static("[yellow]  ║[/yellow][magenta]            │  [/magenta][cyan]API MODE[/cyan][magenta]  │               [/magenta][yellow]║[/yellow]")
                yield Static("[yellow]  ║[/yellow][magenta]            │   [/magenta][green]🔑[/green][magenta]       │               [/magenta][yellow]║[/yellow]")
                yield Static("[yellow]  ║[/yellow][magenta]            └─────────────┘               [/magenta][yellow]║[/yellow]")
                yield Static("[yellow]  ║[/yellow][cyan]        Anthropic API Direct Access        [/cyan][yellow]║[/yellow]")
                yield Static("[yellow]  ╚═══════════════════════════════════════════╝[/yellow]")
                yield Static("")

            yield Static("[white]=-[/white]" * 24, classes="separator")
            yield Static("")

            # Current provider display
            provider_names = {
                AIProviderType.TINYLLAMA: "TinyLlama (Local)",
                AIProviderType.CLAUDE_CLI: "Claude CLI (Subscription)",
                AIProviderType.CLAUDE_API: "Claude API (API Key)",
                AIProviderType.OLLAMA: "Ollama (Remote GPU)",
            }
            yield Static(f"[green]  Current Provider:[/green] [bold white]{provider_names[current_provider]}[/bold white]")
            yield Static("")

            yield Static("[white]=-[/white]" * 24, classes="separator")
            yield Static("")

            yield Static("[yellow]  --- SELECT AI PROVIDER ---[/yellow]")
            yield Static("")

            # TinyLlama option
            yield Button(
                f"(1) TinyLlama (Local) - Free, offline",
                id="provider_tinyllama",
                classes="settings-option" + (" selected" if current_provider == AIProviderType.TINYLLAMA else "")
            )
            yield Static("       [dim]Runs locally, no internet needed.[/dim]", classes="settings-desc")

            # Claude CLI option
            yield Button(
                f"(2) Claude CLI - Uses your subscription",
                id="provider_claude_cli",
                classes="settings-option" + (" selected" if current_provider == AIProviderType.CLAUDE_CLI else "")
            )
            yield Static("       [dim]Leverages existing `claude` auth.[/dim]", classes="settings-desc")

            # Claude API option
            yield Button(
                f"(3) Claude API - Requires API key",
                id="provider_claude_api",
                classes="settings-option" + (" selected" if current_provider == AIProviderType.CLAUDE_API else "")
            )
            yield Static("       [dim]Direct API access, separate billing.[/dim]", classes="settings-desc")

            # Ollama option
            yield Button(
                f"(4) Ollama (Remote GPU) - Your server",
                id="provider_ollama",
                classes="settings-option" + (" selected" if current_provider == AIProviderType.OLLAMA else "")
            )
            yield Static(f"       [dim]{game_settings.ollama_host} / {game_settings.ollama_model}[/dim]", classes="settings-desc")

            yield Static("")
            yield Static("[white]=-[/white]" * 24, classes="separator")
            yield Static("")

            # Claude-specific settings (only shown when Claude provider selected)
            if current_provider in [AIProviderType.CLAUDE_CLI, AIProviderType.CLAUDE_API]:
                yield Static("[yellow]  --- CLAUDE MODEL SELECTION ---[/yellow]")
                yield Static("")

                if current_provider == AIProviderType.CLAUDE_API:
                    yield Static(f"  [cyan]API Key:[/cyan] {masked_key}")
                    yield Static("  [bold yellow](K)[/bold yellow] Set API Key")
                    yield Static("")

                yield Static(f"  [cyan]Current Model:[/cyan] [bold white]{model_display}[/bold white]")
                yield Static("")
                yield Static("  [bold yellow](H)[/bold yellow] Haiku 3.5 - [green]Fast/Cheap[/green]")
                yield Static("  [bold yellow](S)[/bold yellow] Sonnet 4 - [cyan]Balanced[/cyan]")
                yield Static("  [bold yellow](O)[/bold yellow] Opus 4.5 - [magenta]Best Quality[/magenta]")
                yield Static("")

                yield Static("[white]=-[/white]" * 24, classes="separator")
                yield Static("")

            yield Static("  [bold yellow](T)[/bold yellow] Test Current Provider")
            yield Static("  [bold yellow](Q)[/bold yellow] Return to Settings")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle provider selection"""
        provider_map = {
            "provider_tinyllama": AIProviderType.TINYLLAMA,
            "provider_claude_cli": AIProviderType.CLAUDE_CLI,
            "provider_claude_api": AIProviderType.CLAUDE_API,
            "provider_ollama": AIProviderType.OLLAMA,
        }

        if event.button.id in provider_map:
            game_settings.ai_provider = provider_map[event.button.id]
            game_settings.save()
            self._refresh_screen()

    def _refresh_screen(self):
        """Refresh the screen to show updated settings"""
        self.app.pop_screen()
        self.app.push_screen(AISettingsScreen())

    def _set_model(self, model_id: str):
        """Set the Claude model"""
        game_settings.claude_model = model_id
        game_settings.save()
        self._refresh_screen()

    def _prompt_api_key(self):
        """Show API key input prompt"""
        from textual.widgets import Input
        # For now, just show a message - full input would need more complex UI
        self.notify("Enter API key in saves/settings.json or set ANTHROPIC_API_KEY env var", title="API Key")

    def _test_provider(self):
        """Test the current AI provider"""
        from brainbot import ai_provider_manager, get_current_provider_name

        provider = ai_provider_manager.get_current_provider()
        if provider:
            self.notify(f"Testing {get_current_provider_name()}...", title="Testing")
            try:
                success = provider.initialize()
                if success:
                    self.notify(f"{get_current_provider_name()} is working!", title="Success")
                else:
                    self.notify(f"{get_current_provider_name()} failed to initialize", title="Failed")
            except Exception as e:
                self.notify(f"Error: {e}", title="Failed")
        else:
            self.notify("No provider configured", title="Error")

    def on_key(self, event: events.Key) -> None:
        """Handle keyboard shortcuts"""
        key = event.key.lower()

        if key == "q" or key == "escape":
            self.app.pop_screen()
        elif key == "1":
            game_settings.ai_provider = AIProviderType.TINYLLAMA
            game_settings.save()
            self._refresh_screen()
        elif key == "2":
            game_settings.ai_provider = AIProviderType.CLAUDE_CLI
            game_settings.save()
            self._refresh_screen()
        elif key == "3":
            game_settings.ai_provider = AIProviderType.CLAUDE_API
            game_settings.save()
            self._refresh_screen()
        elif key == "4":
            game_settings.ai_provider = AIProviderType.OLLAMA
            game_settings.save()
            self._refresh_screen()
        elif key == "h":
            self._set_model("claude-3-5-haiku-20241022")
        elif key == "s":
            self._set_model("claude-sonnet-4-20250514")
        elif key == "o":
            self._set_model("claude-opus-4-5-20250131")
        elif key == "k":
            self._prompt_api_key()
        elif key == "t":
            self._test_provider()

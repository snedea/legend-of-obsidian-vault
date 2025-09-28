"""
WereWolf Den IGM for Legend of the Obsidian Vault
Learn werewolf curse, transformation during PvP, and stat stealing mechanics
"""
import datetime
import random
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button
from textual import events


class WereWolfDenScreen(Screen):
    """WereWolf Den - Learn the curse and transformation abilities"""

    def __init__(self):
        super().__init__()
        self.learning_mode = False

    def compose(self) -> ComposeResult:
        # Delayed import to avoid circular dependency
        import lov

        # Colored WereWolf Den ASCII Art Header
        yield Static("        ✦ THE WEREWOLF'S DEN ✦", classes="werewolf-title")
        yield Static("    🌙🐺🌙🐺🌙🐺🌙🐺🌙🐺🌙🐺🌙🐺", classes="werewolf-decoration")
        yield Static("   ╔═══════════════════════════════════════════╗", classes="werewolf-border")
        yield Static("   ║  🌕 ⚔️  PRIMAL TRANSFORMATION  ⚔️ 🌕   ║", classes="werewolf-banner")
        yield Static("   ║        「Embrace the Beast Within」       ║", classes="werewolf-banner")
        yield Static("   ╚═══════════════════════════════════════════╝", classes="werewolf-border")
        yield Static("     🔥   ⚡   💀   ⚡   🔥   💀   ⚡   🔥", classes="werewolf-decoration")
        yield Static("═══════════════════════════════════════════════════", classes="werewolf-ground")

        # Two blank lines below header
        yield Static("")
        yield Static("")

        # Check if player is already a werewolf
        is_werewolf = getattr(lov.current_player, 'is_werewolf', False)
        transformations_today = getattr(lov.current_player, 'werewolf_uses_today', 0)
        total_transformations = getattr(lov.current_player, 'werewolf_transformations', 0)

        if is_werewolf:
            yield Static("The curse flows through your veins, beast-brother.", classes="werewolf-content")
            yield Static(f"Transformations today: {transformations_today}/3", classes="werewolf-content")
            yield Static(f"Total transformations: {total_transformations}", classes="werewolf-content")
            yield Static("")

            # Werewolf abilities and information
            yield Static("═ WEREWOLF ABILITIES ═", classes="werewolf-content")
            yield Static("• Transform during PvP combat for massive stat boost", classes="werewolf-content")
            yield Static("• Steal 10% of defeated opponent's stats permanently", classes="werewolf-content")
            yield Static("• Risk: 20% chance of losing control and taking damage", classes="werewolf-content")
            yield Static("• Limit: 3 transformations per day", classes="werewolf-content")
            yield Static("")

            yield Static("(P)ractice transformation (safe)", classes="werewolf-content")
            yield Static("(M)editate with the pack", classes="werewolf-content")
            yield Static("(H)owl at the moon (+1 random stat)", classes="werewolf-content")

        else:
            yield Static("A massive werewolf emerges from the shadows, eyes glowing with ancient hunger.", classes="werewolf-content")
            yield Static("'Mortal,' it growls, 'would you accept the curse of the wolf?'", classes="werewolf-content")
            yield Static("")

            # Curse details
            yield Static("═ THE WEREWOLF CURSE ═", classes="werewolf-content")
            yield Static("Cost: 5000 gold", classes="werewolf-content")
            yield Static("Benefits:", classes="werewolf-content")
            yield Static("  • +50% STR/DEF during PvP transformation", classes="werewolf-content")
            yield Static("  • Steal stats from defeated players", classes="werewolf-content")
            yield Static("  • Enhanced combat abilities", classes="werewolf-content")
            yield Static("Risks:", classes="werewolf-content")
            yield Static("  • 20% chance to lose control", classes="werewolf-content")
            yield Static("  • Take 25% current HP damage if lose control", classes="werewolf-content")
            yield Static("  • Permanent curse (cannot be removed)", classes="werewolf-content")
            yield Static("")

            if lov.current_player.gold >= 5000:
                yield Static("(A)ccept the werewolf curse", classes="werewolf-content")
            else:
                yield Static("(Insufficient gold - need 5000)", classes="werewolf-content")

            yield Static("(L)earn more about the curse", classes="werewolf-content")

        # Common options
        yield Static("(R)eturn to Other Places", classes="werewolf-content")

        # Status and command area
        self._compose_status_area()

    def _compose_status_area(self):
        """Compose the status and command prompt area"""
        # Delayed import to avoid circular dependency
        import lov

        # One blank line before status
        yield Static("")

        # Player status line with werewolf indicator
        hp_text = f"({lov.current_player.hitpoints} of {lov.current_player.max_hitpoints})"
        werewolf_status = "🐺 Werewolf" if getattr(lov.current_player, 'is_werewolf', False) else "Human"
        status_line = f"HitPoints: {hp_text}  Gold: {lov.current_player.gold}  Form: {werewolf_status}"
        yield Static(status_line, classes="werewolf-status")

        # One blank line before command area
        yield Static("")

        # Command prompt area
        now = datetime.datetime.now()
        time_str = f"{now.hour:02d}:{now.minute:02d}"

        location_commands = f"WereWolf Den (A,P,M,H,L,R)  (? for menu)"
        yield Static(location_commands, classes="werewolf-location-commands")

        # Command prompt with time and cursor
        yield Static(f"Your command, {lov.current_player.name}? [{time_str}]: █", classes="werewolf-prompt")

    def on_key(self, event: events.Key) -> None:
        # Delayed import to avoid circular dependency
        import lov

        key = event.key.upper()

        is_werewolf = getattr(lov.current_player, 'is_werewolf', False)

        if key == "A" and not is_werewolf:
            # Accept werewolf curse
            if lov.current_player.gold >= 5000:
                self._accept_werewolf_curse()
            else:
                self.notify("You need 5000 gold to accept the curse.")
        elif key == "P" and is_werewolf:
            # Practice transformation
            self._practice_transformation()
        elif key == "M" and is_werewolf:
            # Meditate with pack
            self._meditate_with_pack()
        elif key == "H" and is_werewolf:
            # Howl at the moon
            self._howl_at_moon()
        elif key == "L":
            # Learn about curse
            self._learn_about_curse()
        elif key == "R":
            self.app.pop_screen()
        elif key == "?":
            if is_werewolf:
                self.notify("P = Practice, M = Meditate, H = Howl, L = Learn, R = Return")
            else:
                self.notify("A = Accept curse, L = Learn about curse, R = Return")

    def _accept_werewolf_curse(self):
        """Accept the werewolf curse"""
        # Delayed import to avoid circular dependency
        import lov

        # Deduct gold and grant curse
        lov.current_player.gold -= 5000
        lov.current_player.is_werewolf = True

        # Initialize werewolf stats
        if not hasattr(lov.current_player, 'werewolf_uses_today'):
            lov.current_player.werewolf_uses_today = 0
        if not hasattr(lov.current_player, 'werewolf_transformations'):
            lov.current_player.werewolf_transformations = 0

        # Immediate benefits
        lov.current_player.strength += 3
        lov.current_player.defense += 2
        lov.current_player.max_hitpoints += 10
        lov.current_player.hitpoints += 10

        self.notify("🌕 THE CURSE AWAKENS! 🌕")
        self.notify("Primal power surges through your veins!")
        self.notify("You feel the beast stirring within... (+3 STR, +2 DEF, +10 Max HP)")
        self.notify("The werewolf grins, showing massive fangs.")
        self.notify("'Welcome to the pack, brother. Use your power wisely.'")

        lov.game_db.save_player(lov.current_player)
        self._refresh_screen()

    def _practice_transformation(self):
        """Practice safe transformation"""
        # Delayed import to avoid circular dependency
        import lov

        practice_roll = random.randint(1, 100)

        self.notify("You feel the beast stirring within...")
        self.notify("Claws extend, muscles bulge, senses sharpen...")

        if practice_roll <= 70:
            # Successful practice
            benefit_roll = random.randint(1, 3)
            if benefit_roll == 1:
                lov.current_player.strength += 1
                self.notify("Your practice strengthens your primal form! (+1 Strength)")
            elif benefit_roll == 2:
                lov.current_player.defense += 1
                self.notify("You learn to control the transformation better! (+1 Defense)")
            else:
                heal_amount = random.randint(10, 20)
                lov.current_player.hitpoints = min(lov.current_player.max_hitpoints,
                                                 lov.current_player.hitpoints + heal_amount)
                self.notify(f"Your werewolf vitality heals your wounds! (+{heal_amount} HP)")

        elif practice_roll <= 90:
            # Neutral practice
            self.notify("You practice the transformation safely, learning control.")
            self.notify("The beast is patient today.")

        else:
            # Minor mishap
            damage = random.randint(3, 8)
            lov.current_player.hitpoints = max(1, lov.current_player.hitpoints - damage)
            self.notify(f"The beast fights back! You lose control briefly. (-{damage} HP)")

        lov.game_db.save_player(lov.current_player)

    def _meditate_with_pack(self):
        """Meditate with the werewolf pack"""
        # Delayed import to avoid circular dependency
        import lov

        meditation_messages = [
            "The pack shares ancient wisdom about the hunt and the moon.",
            "You learn to balance the human mind with the wolf's instincts.",
            "The alpha teaches you about controlling the beast within.",
            "Pack bonds strengthen your resolve and primal power.",
            "Ancient werewolf lore flows through the collective consciousness."
        ]

        message = random.choice(meditation_messages)
        self.notify(f"During meditation: {message}")

        # Benefits from pack meditation
        benefit_roll = random.randint(1, 100)

        if benefit_roll <= 30:
            # Wisdom boost
            lov.current_player.intelligence += 1
            self.notify("Ancient werewolf wisdom enhances your intellect! (+1 Intelligence)")
        elif benefit_roll <= 50:
            # Pack loyalty - charm boost
            lov.current_player.charm += 1
            self.notify("Your bond with the pack strengthens your leadership! (+1 Charm)")
        elif benefit_roll <= 70:
            # Primal strength
            lov.current_player.strength += 1
            self.notify("The pack's strength flows through you! (+1 Strength)")
        else:
            # Inner peace - reset daily uses
            if lov.current_player.werewolf_uses_today > 0:
                lov.current_player.werewolf_uses_today = max(0, lov.current_player.werewolf_uses_today - 1)
                self.notify("Deep meditation restores your transformation energy!")
            else:
                self.notify("You achieve inner balance between human and wolf.")

        lov.game_db.save_player(lov.current_player)

    def _howl_at_moon(self):
        """Howl at the moon for stat boost"""
        # Delayed import to avoid circular dependency
        import lov

        self.notify("You throw back your head and release a primal howl...")
        self.notify("AWOOOOOOOOO!")
        self.notify("The moon responds to your call...")

        # Random stat boost
        stats = ['strength', 'defense', 'charm', 'intelligence']
        chosen_stat = random.choice(stats)

        if chosen_stat == 'strength':
            lov.current_player.strength += 1
            self.notify("Lunar power enhances your physical might! (+1 Strength)")
        elif chosen_stat == 'defense':
            lov.current_player.defense += 1
            self.notify("Moonlight hardens your hide! (+1 Defense)")
        elif chosen_stat == 'charm':
            lov.current_player.charm += 1
            self.notify("Your howl carries primal magnetism! (+1 Charm)")
        elif chosen_stat == 'intelligence':
            lov.current_player.intelligence += 1
            self.notify("Lunar wisdom fills your mind! (+1 Intelligence)")

        # Small chance for bonus
        if random.randint(1, 100) <= 20:
            bonus_hp = random.randint(5, 15)
            lov.current_player.max_hitpoints += bonus_hp
            lov.current_player.hitpoints += bonus_hp
            self.notify(f"The moon's blessing strengthens your life force! (+{bonus_hp} Max HP)")

        lov.game_db.save_player(lov.current_player)

    def _learn_about_curse(self):
        """Learn detailed information about the werewolf curse"""
        lore_messages = [
            "The werewolf explains: 'The curse grants power, but demands control.'",
            "'In PvP combat, transformation doubles your strength and defense.'",
            "'But beware - 1 in 5 transformations, the beast may turn on you.'",
            "'When you defeat cursed opponents, you steal their essence permanently.'",
            "'The pack grows stronger with each fallen enemy.'",
            "'Remember: transformation is limited. Use it wisely in battle.'",
            "'Some say the curse can drive warriors to legendary status... or madness.'"
        ]

        for message in lore_messages:
            self.notify(message)

    def _refresh_screen(self):
        """Refresh the screen to show updated interface"""
        self.app.pop_screen()
        self.app.push_screen(WereWolfDenScreen())
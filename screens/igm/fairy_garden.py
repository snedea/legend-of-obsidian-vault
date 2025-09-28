"""
Fairy Garden IGM for Legend of the Obsidian Vault
Learn Fairy Lore healing abilities and interact with mystical creatures
"""
import datetime
import random
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static
from textual import events


class FairyGardenScreen(Screen):
    """Fairy Garden - Learn healing arts and mystical abilities"""

    def __init__(self):
        super().__init__()
        self.fairy_present = True
        self.learning_session = False

    def compose(self) -> ComposeResult:
        # Delayed import to avoid circular dependency
        import lov

        # Colored Fairy Garden ASCII Art Header
        yield Static("        ✦ THE ENCHANTED FAIRY GARDEN ✦", classes="fairy-title")
        yield Static("    🌸✨🦋✨🌸✨🦋✨🌸✨🦋✨🌸✨🦋✨🌸", classes="fairy-decoration")
        yield Static("   ╭─────────────────────────────────────────────╮", classes="fairy-border")
        yield Static("   │  🧚‍♀️  ･ﾟ✧ Healing Sanctuary ✧ﾟ･ 🧚‍♀️   │", classes="fairy-banner")
        yield Static("   │        ✨ Learn Ancient Arts ✨         │", classes="fairy-banner")
        yield Static("   ╰─────────────────────────────────────────────╯", classes="fairy-border")
        yield Static("     🌺   🌷   🌻   🌺   🌷   🌻   🌺", classes="fairy-decoration")
        yield Static("═══════════════════════════════════════════════════", classes="fairy-ground")

        # Two blank lines below header
        yield Static("")
        yield Static("")

        # Check if player already has fairy lore
        has_fairy_lore = lov.current_player.fairy_lore

        if has_fairy_lore:
            yield Static("The fairy recognizes you as a student of the healing arts.", classes="fairy-content")
            yield Static("Your knowledge of Fairy Lore allows you to heal during combat!", classes="fairy-content")
            yield Static("")
            yield Static("(P)ractice healing techniques", classes="fairy-content")
            yield Static("(M)editate with the fairy", classes="fairy-content")
            yield Static("(A)dvanced healing training", classes="fairy-content")
        else:
            yield Static("A shimmering fairy approaches, her wings sparkling with ancient magic.", classes="fairy-content")
            yield Static("'Mortal,' she chimes, 'would you learn the sacred art of Fairy Lore?'", classes="fairy-content")
            yield Static("")
            yield Static("(L)earn Fairy Lore healing (Costs 1000 gold)", classes="fairy-content")
            yield Static("(A)sk about healing arts", classes="fairy-content")

        # Common options
        yield Static("(G)ather mystical herbs", classes="fairy-content")
        yield Static("(R)eturn to Other Places", classes="fairy-content")

        # Status and command area
        self._compose_status_area()

    def _compose_status_area(self):
        """Compose the status and command prompt area"""
        # Delayed import to avoid circular dependency
        import lov

        # One blank line before status
        yield Static("")

        # Player status line with fairy lore indicator
        hp_text = f"({lov.current_player.hitpoints} of {lov.current_player.max_hitpoints})"
        fairy_status = "✨ Fairy Lore" if lov.current_player.fairy_lore else "No Fairy Lore"
        status_line = f"HitPoints: {hp_text}  Gold: {lov.current_player.gold}  {fairy_status}"
        yield Static(status_line, classes="fairy-status")

        # One blank line before command area
        yield Static("")

        # Command prompt area
        now = datetime.datetime.now()
        time_str = f"{now.hour:02d}:{now.minute:02d}"

        location_commands = f"Fairy Garden (L,P,M,A,G,R)  (? for menu)"
        yield Static(location_commands, classes="fairy-location-commands")

        # Command prompt with time and cursor
        yield Static(f"Your command, {lov.current_player.name}? [{time_str}]: █", classes="fairy-prompt")

    def on_key(self, event: events.Key) -> None:
        # Delayed import to avoid circular dependency
        import lov

        key = event.key.upper()

        if key == "L":
            # Learn Fairy Lore
            self._learn_fairy_lore()
        elif key == "P":
            # Practice healing
            if lov.current_player.fairy_lore:
                self._practice_healing()
            else:
                self.notify("You must first learn Fairy Lore to practice healing.")
        elif key == "M":
            # Meditate with fairy
            if lov.current_player.fairy_lore:
                self._meditate_with_fairy()
            else:
                self.notify("The fairy will only meditate with those who know Fairy Lore.")
        elif key == "A":
            # Advanced training or ask about healing
            if lov.current_player.fairy_lore:
                self._advanced_healing_training()
            else:
                self._ask_about_healing()
        elif key == "G":
            # Gather herbs
            self._gather_herbs()
        elif key == "R":
            self.app.pop_screen()
        elif key == "?":
            if lov.current_player.fairy_lore:
                self.notify("L = Learn more, P = Practice, M = Meditate, A = Advanced training, G = Gather herbs, R = Return")
            else:
                self.notify("L = Learn Fairy Lore, A = Ask about healing, G = Gather herbs, R = Return")

    def _learn_fairy_lore(self):
        """Learn the Fairy Lore healing ability"""
        # Delayed import to avoid circular dependency
        import lov

        if lov.current_player.fairy_lore:
            self.notify("You already possess the knowledge of Fairy Lore!")
            return

        cost = 1000
        if lov.current_player.gold < cost:
            self.notify(f"The fairy shakes her head sadly. 'You need {cost} gold to learn this ancient art.'")
            return

        # Deduct gold and grant ability
        lov.current_player.gold -= cost
        lov.current_player.fairy_lore = True

        self.notify("✨ The fairy's magic flows through you! ✨")
        self.notify("'You now possess Fairy Lore,' she whispers. 'Use (H)eal during combat!'")
        self.notify("You can now heal 25-40% of your maximum HP during battle!")

        lov.game_db.save_player(lov.current_player)
        self._refresh_screen()

    def _practice_healing(self):
        """Practice healing techniques"""
        # Delayed import to avoid circular dependency
        import lov

        practice_roll = random.randint(1, 100)

        if practice_roll <= 60:
            # Successful practice - heal some HP
            heal_amount = random.randint(10, 25)
            lov.current_player.hitpoints = min(lov.current_player.max_hitpoints,
                                             lov.current_player.hitpoints + heal_amount)
            self.notify(f"Your practice session heals you! (+{heal_amount} HP)")

        elif practice_roll <= 80:
            # Learn something - boost a stat
            stat_boost = random.choice(['intelligence', 'charm'])
            if stat_boost == 'intelligence':
                lov.current_player.intelligence += 1
                self.notify("Your understanding of healing deepens! (+1 Intelligence)")
            else:
                lov.current_player.charm += 1
                self.notify("Your connection to nature grows! (+1 Charm)")

        else:
            # Nothing happens
            self.notify("Your practice session yields no immediate results, but knowledge grows slowly.")

        lov.game_db.save_player(lov.current_player)

    def _meditate_with_fairy(self):
        """Meditate with the fairy for spiritual benefits"""
        # Delayed import to avoid circular dependency
        import lov

        meditation_messages = [
            "The fairy shares ancient wisdom about the balance of life and death.",
            "You learn that healing comes from understanding, not just magic.",
            "The fairy shows you how nature's energy flows through all living things.",
            "She teaches you that true healing heals the spirit as well as the body.",
            "You glimpse the interconnectedness of all magical forces."
        ]

        message = random.choice(meditation_messages)
        self.notify(f"During meditation: {message}")

        # Random benefit from meditation
        benefit_roll = random.randint(1, 100)

        if benefit_roll <= 30:
            # Spiritual enlightenment
            lov.current_player.spirit_level = "high"
            self.notify("Your spirits are lifted to new heights! (High Spirits achieved)")
        elif benefit_roll <= 50:
            # Boost max HP temporarily
            hp_boost = random.randint(5, 15)
            lov.current_player.max_hitpoints += hp_boost
            lov.current_player.hitpoints += hp_boost
            self.notify(f"The fairy's blessing strengthens your life force! (+{hp_boost} Max HP)")
        elif benefit_roll <= 70:
            # Gain gems
            gems_found = random.randint(1, 3)
            lov.current_player.gems += gems_found
            self.notify(f"The fairy gifts you mystical gems! (+{gems_found} gems)")
        else:
            # Inner peace
            self.notify("You feel inner peace and clarity. Your mind is focused.")

        lov.game_db.save_player(lov.current_player)

    def _advanced_healing_training(self):
        """Advanced healing training for experienced fairy lore practitioners"""
        # Delayed import to avoid circular dependency
        import lov

        training_cost = 500
        if lov.current_player.gold < training_cost:
            self.notify(f"Advanced training requires {training_cost} gold.")
            return

        lov.current_player.gold -= training_cost

        # Advanced training benefits
        training_roll = random.randint(1, 100)

        if training_roll <= 40:
            # Improved healing efficiency
            self.notify("You learn to channel healing energy more efficiently!")
            self.notify("Your combat healing will be more powerful!")
            # This could set a flag for improved healing in combat

        elif training_roll <= 70:
            # Learn to heal others (future feature)
            self.notify("The fairy teaches you to extend your healing to others.")
            self.notify("This knowledge may prove useful in the future...")

        else:
            # Master level insight
            lov.current_player.intelligence += 2
            lov.current_player.charm += 1
            self.notify("You achieve master-level insight into healing arts!")
            self.notify("Your understanding transcends mortal limitations! (+2 INT, +1 Charm)")

        lov.game_db.save_player(lov.current_player)

    def _ask_about_healing(self):
        """Ask the fairy about healing arts before learning"""
        info_messages = [
            "The fairy explains: 'Fairy Lore allows healing during combat.'",
            "'With this knowledge, you can restore 25-40% of your health in battle.'",
            "'The cost is 1000 gold, but the knowledge lasts forever.'",
            "'Many warriors find this art invaluable in dangerous encounters.'",
            "'Choose wisely, mortal, for true power comes with responsibility.'"
        ]

        for message in info_messages:
            self.notify(message)

    def _gather_herbs(self):
        """Gather mystical herbs in the garden"""
        # Delayed import to avoid circular dependency
        import lov

        herb_roll = random.randint(1, 100)

        if herb_roll <= 30:
            # Find healing herbs
            heal_amount = random.randint(15, 30)
            lov.current_player.hitpoints = min(lov.current_player.max_hitpoints,
                                             lov.current_player.hitpoints + heal_amount)
            self.notify(f"You find healing herbs and feel better! (+{heal_amount} HP)")

        elif herb_roll <= 50:
            # Find valuable herbs to sell
            gold_value = random.randint(50, 150)
            lov.current_player.gold += gold_value
            self.notify(f"You gather rare herbs worth {gold_value} gold!")

        elif herb_roll <= 70:
            # Find mystical ingredients
            self.notify("You gather mystical ingredients that tingle with magic.")
            self.notify("These may be useful for future enchantments...")

        elif herb_roll <= 90:
            # Nothing useful
            self.notify("You search carefully but find only common weeds.")

        else:
            # Fairy gifts you something special
            if random.choice([True, False]):
                lov.current_player.gems += 1
                self.notify("A friendly fairy notices your efforts and gifts you a gem!")
            else:
                lov.current_player.charm += 1
                self.notify("Your gentle approach to nature increases your charm!")

        lov.game_db.save_player(lov.current_player)

    def _refresh_screen(self):
        """Refresh the screen to show updated interface"""
        self.app.pop_screen()
        self.app.push_screen(FairyGardenScreen())
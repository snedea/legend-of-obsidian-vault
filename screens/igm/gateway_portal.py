"""
Gateway Portal IGM for Legend of the Obsidian Vault
Access to special scripted IGMs: Zycho Zircus, Death's Mansion, and random events
"""
import datetime
import random
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button
from textual import events


class GatewayPortalScreen(Screen):
    """Gateway Portal - Access to special scripted IGM adventures"""

    def __init__(self):
        super().__init__()
        self.portal_destination = None

    def compose(self) -> ComposeResult:
        # Delayed import to avoid circular dependency
        import lov

        # Colored Gateway Portal ASCII Art Header
        yield Static("        ✦ THE DIMENSIONAL GATEWAY ✦", classes="gateway-title")
        yield Static("    🌌⭐🌌⭐🌌⭐🌌⭐🌌⭐🌌⭐🌌⭐🌌", classes="gateway-decoration")
        yield Static("   ╔═══════════════════════════════════════════╗", classes="gateway-border")
        yield Static("   ║  🚪 ⚡ PORTALS TO OTHER REALMS ⚡ 🚪   ║", classes="gateway-banner")
        yield Static("   ║        「Step Through to Adventure」       ║", classes="gateway-banner")
        yield Static("   ╚═══════════════════════════════════════════╝", classes="gateway-border")
        yield Static("     ✨   🔮   ⚡   🔮   ✨   🔮   ⚡   ✨", classes="gateway-decoration")
        yield Static("═══════════════════════════════════════════════════", classes="gateway-ground")

        # Two blank lines below header
        yield Static("")
        yield Static("")

        # Gateway description
        yield Static("Swirling portals of energy hum with otherworldly power.", classes="gateway-content")
        yield Static("Each gateway leads to a realm of unique challenges and rewards.", classes="gateway-content")
        yield Static("")

        # Portal destinations
        yield Static("═ AVAILABLE PORTALS ═", classes="gateway-content")
        yield Static("Portal activation cost: 1 gem per destination", classes="gateway-content")
        yield Static("")

        # Check if player has gems for portal travel
        can_travel = lov.current_player.gems > 0

        yield Button("(Z)ycho Zircus - Carnival of Chaos", id="zircus", disabled=not can_travel)
        yield Button("(D)eath's Mansion - House of Horrors", id="mansion", disabled=not can_travel)
        yield Button("(R)andom Portal - Unknown Destination", id="random", disabled=not can_travel)

        if not can_travel:
            yield Static("")
            yield Static("⚠️ Portal travel requires at least 1 gem for activation", classes="gateway-content")

        yield Static("")
        yield Static("(I)nspect portals (no cost)", classes="gateway-content")
        yield Static("(L)eave gateway chamber", classes="gateway-content")

        # Status and command area
        self._compose_status_area()

    def _compose_status_area(self):
        """Compose the status and command prompt area"""
        # Delayed import to avoid circular dependency
        import lov

        # One blank line before status
        yield Static("")

        # Player status line
        hp_text = f"({lov.current_player.hitpoints} of {lov.current_player.max_hitpoints})"
        status_line = f"HitPoints: {hp_text}  Gold: {lov.current_player.gold}  Gems: {lov.current_player.gems}"
        yield Static(status_line, classes="gateway-status")

        # One blank line before command area
        yield Static("")

        # Command prompt area
        now = datetime.datetime.now()
        time_str = f"{now.hour:02d}:{now.minute:02d}"

        location_commands = f"Gateway Portal (Z,D,R,I,L)  (? for menu)"
        yield Static(location_commands, classes="gateway-location-commands")

        # Command prompt with time and cursor
        yield Static(f"Your command, {lov.current_player.name}? [{time_str}]: █", classes="gateway-prompt")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle portal selections"""
        action = event.button.id

        if action == "zircus":
            self._enter_zycho_zircus()
        elif action == "mansion":
            self._enter_deaths_mansion()
        elif action == "random":
            self._enter_random_portal()

    def on_key(self, event: events.Key) -> None:
        # Delayed import to avoid circular dependency
        import lov

        key = event.key.upper()

        if key == "Z":
            if lov.current_player.gems > 0:
                self._enter_zycho_zircus()
            else:
                self.notify("You need at least 1 gem to activate the portal!")
        elif key == "D":
            if lov.current_player.gems > 0:
                self._enter_deaths_mansion()
            else:
                self.notify("You need at least 1 gem to activate the portal!")
        elif key == "R":
            if lov.current_player.gems > 0:
                self._enter_random_portal()
            else:
                self.notify("You need at least 1 gem to activate the portal!")
        elif key == "I":
            self._inspect_portals()
        elif key == "L":
            self.app.pop_screen()
        elif key == "?":
            self.notify("Z = Zycho Zircus, D = Death's Mansion, R = Random portal, I = Inspect, L = Leave")

    def _enter_zycho_zircus(self):
        """Enter the Zycho Zircus portal"""
        # Delayed import to avoid circular dependency
        import lov

        # Deduct gem cost
        lov.current_player.gems -= 1

        self.notify("🎪 The Zycho Zircus portal swirls to life!")
        self.notify("You step through into a realm of carnival chaos...")

        # Zycho Zircus encounters
        encounter_roll = random.randint(1, 100)

        if encounter_roll <= 30:
            # Carnival game - win or lose gold
            self._carnival_game()
        elif encounter_roll <= 50:
            # Freakshow encounter - stat changes
            self._freakshow_encounter()
        elif encounter_roll <= 70:
            # Ring master challenge
            self._ringmaster_challenge()
        elif encounter_roll <= 85:
            # Funhouse mirrors - identity confusion
            self._funhouse_mirrors()
        else:
            # Special zircus blessing
            self._zircus_blessing()

        lov.game_db.save_player(lov.current_player)

    def _carnival_game(self):
        """Carnival game event"""
        # Delayed import to avoid circular dependency
        import lov

        games = [
            "Ring Toss", "Strength Test", "Fortune Wheel", "Duck Pond", "Dart Throw"
        ]
        game = random.choice(games)

        self.notify(f"A carnival barker calls you to play {game}!")
        self.notify("'Step right up! Test your luck!'")

        # Random outcome
        if random.randint(1, 100) <= 50:
            # Win
            winnings = random.randint(100, 500) * lov.current_player.level
            lov.current_player.gold += winnings
            self.notify(f"🎉 You win {winnings:,} gold! 🎉")
        else:
            # Lose
            loss = random.randint(50, 200)
            lov.current_player.gold = max(0, lov.current_player.gold - loss)
            self.notify(f"💸 You lose {loss} gold to the game!")

    def _freakshow_encounter(self):
        """Freakshow encounter with stat changes"""
        # Delayed import to avoid circular dependency
        import lov

        encounters = [
            "The Bearded Lady shares ancient wisdom",
            "The Strong Man teaches you about power",
            "The Contortionist shows flexibility of mind",
            "The Fire Breather grants elemental knowledge"
        ]

        encounter = random.choice(encounters)
        self.notify(f"🎭 {encounter}!")

        # Random stat change
        stats = ['strength', 'defense', 'charm', 'intelligence']
        stat = random.choice(stats)

        if random.randint(1, 100) <= 70:
            # Positive change
            if stat == 'strength':
                lov.current_player.strength += 1
                self.notify(f"Your strength increases! (+1 Strength)")
            elif stat == 'defense':
                lov.current_player.defense += 1
                self.notify(f"Your resilience grows! (+1 Defense)")
            elif stat == 'charm':
                lov.current_player.charm += 1
                self.notify(f"Your presence becomes more magnetic! (+1 Charm)")
            else:
                lov.current_player.intelligence += 1
                self.notify(f"Your mind expands! (+1 Intelligence)")
        else:
            # Negative change
            self.notify("The freakshow's strangeness unsettles you...")
            damage = random.randint(5, 15)
            lov.current_player.hitpoints = max(1, lov.current_player.hitpoints - damage)
            self.notify(f"You feel drained by the experience. (-{damage} HP)")

    def _ringmaster_challenge(self):
        """Challenge from the ringmaster"""
        # Delayed import to avoid circular dependency
        import lov

        self.notify("🎩 The Ringmaster approaches with a sinister grin!")
        self.notify("'Welcome to my circus! Care for a... special challenge?'")

        # High risk, high reward challenge
        if random.randint(1, 100) <= 60:
            # Success
            reward_type = random.choice(['gold', 'gems', 'stats'])
            if reward_type == 'gold':
                reward = 1000 * lov.current_player.level
                lov.current_player.gold += reward
                self.notify(f"The Ringmaster applauds! You earn {reward:,} gold!")
            elif reward_type == 'gems':
                gems = random.randint(2, 5)
                lov.current_player.gems += gems
                self.notify(f"The Ringmaster gifts you {gems} mystical gems!")
            else:
                lov.current_player.strength += 1
                lov.current_player.defense += 1
                self.notify("The Ringmaster's approval strengthens you! (+1 STR, +1 DEF)")
        else:
            # Failure - cursed by the ringmaster
            self.notify("The Ringmaster's eyes flash with anger!")
            self.notify("'You have failed me! Accept this curse!'")
            penalty = random.randint(100, 300)
            lov.current_player.gold = max(0, lov.current_player.gold - penalty)
            self.notify(f"Dark magic drains {penalty} gold from your purse!")

    def _funhouse_mirrors(self):
        """Funhouse mirrors - identity confusion"""
        # Delayed import to avoid circular dependency
        import lov

        self.notify("🪞 You enter a hall of twisted mirrors...")
        self.notify("Your reflection shows... something else entirely!")

        # Random effect
        effect_roll = random.randint(1, 100)

        if effect_roll <= 40:
            # Swap stats temporarily
            old_str = lov.current_player.strength
            old_def = lov.current_player.defense
            lov.current_player.strength = old_def
            lov.current_player.defense = old_str
            self.notify("The mirrors scramble your abilities! STR and DEF swapped!")

        elif effect_roll <= 70:
            # See true self - boost charm
            lov.current_player.charm += 2
            self.notify("You see your true self clearly! (+2 Charm)")

        else:
            # Mirror fragments - random stat boost
            stat_boosts = random.randint(2, 4)
            stats = ['strength', 'defense', 'charm', 'intelligence']
            for _ in range(stat_boosts):
                stat = random.choice(stats)
                if stat == 'strength':
                    lov.current_player.strength += 1
                elif stat == 'defense':
                    lov.current_player.defense += 1
                elif stat == 'charm':
                    lov.current_player.charm += 1
                else:
                    lov.current_player.intelligence += 1

            self.notify(f"Mirror magic enhances you! (+{stat_boosts} random stats)")

    def _zircus_blessing(self):
        """Special Zycho Zircus blessing"""
        # Delayed import to avoid circular dependency
        import lov

        self.notify("✨ The entire circus suddenly falls silent...")
        self.notify("🎪 Zycho himself appears in a flash of rainbow light!")
        self.notify("'You have brought joy to my realm, warrior!'")

        # Major blessing
        lov.current_player.gold += 2000
        lov.current_player.gems += 3
        lov.current_player.max_hitpoints += 15
        lov.current_player.hitpoints += 15

        self.notify("Zycho's blessing flows through you!")
        self.notify("(+2000 gold, +3 gems, +15 max HP)")

    def _enter_deaths_mansion(self):
        """Enter Death's Mansion portal"""
        # Delayed import to avoid circular dependency
        import lov

        # Deduct gem cost
        lov.current_player.gems -= 1

        self.notify("💀 Death's Mansion portal opens with an ominous groan...")
        self.notify("You step into a realm where death itself dwells...")

        # Death's Mansion is high-risk, high-reward
        encounter_roll = random.randint(1, 100)

        if encounter_roll <= 25:
            # Death's trial - survive for massive rewards
            self._deaths_trial()
        elif encounter_roll <= 50:
            # Haunted room - ghost encounters
            self._haunted_room()
        elif encounter_roll <= 75:
            # Death's library - forbidden knowledge
            self._deaths_library()
        else:
            # Meet Death himself
            self._meet_death()

        lov.game_db.save_player(lov.current_player)

    def _deaths_trial(self):
        """Trial by Death himself"""
        # Delayed import to avoid circular dependency
        import lov

        self.notify("💀 Death appears before you in flowing black robes!")
        self.notify("'Mortal, you dare enter my domain? Face my trial!'")

        # High-stakes challenge
        if lov.current_player.level >= 10 and random.randint(1, 100) <= 40:
            # Success - massive rewards
            lov.current_player.gold += 5000
            lov.current_player.gems += 10
            lov.current_player.strength += 3
            lov.current_player.defense += 3
            self.notify("💀 Death nods approvingly!")
            self.notify("'You have impressed me, warrior.'")
            self.notify("(+5000 gold, +10 gems, +3 STR, +3 DEF)")
        else:
            # Failure - death penalty
            self.notify("💀 Death's trial overwhelms you!")
            damage = lov.current_player.hitpoints // 2
            lov.current_player.hitpoints = max(1, lov.current_player.hitpoints - damage)
            self.notify(f"You barely escape with your life! (-{damage} HP)")

    def _haunted_room(self):
        """Encounter with mansion ghosts"""
        # Delayed import to avoid circular dependency
        import lov

        self.notify("👻 Ethereal spirits swirl around you!")
        self.notify("The ghosts whisper secrets of the afterlife...")

        # Moderate risk/reward
        if random.randint(1, 100) <= 60:
            # Friendly ghosts
            reward_roll = random.randint(1, 3)
            if reward_roll == 1:
                gold_found = random.randint(500, 1500)
                lov.current_player.gold += gold_found
                self.notify(f"Grateful spirits gift you {gold_found:,} gold!")
            elif reward_roll == 2:
                lov.current_player.intelligence += 2
                self.notify("Ghost wisdom enhances your mind! (+2 Intelligence)")
            else:
                lov.current_player.gems += 2
                self.notify("Spectral gems materialize! (+2 gems)")
        else:
            # Hostile spirits
            self.notify("The spirits grow angry and attack!")
            damage = random.randint(10, 25)
            lov.current_player.hitpoints = max(1, lov.current_player.hitpoints - damage)
            self.notify(f"Ghostly claws rake your soul! (-{damage} HP)")

    def _deaths_library(self):
        """Death's library of forbidden knowledge"""
        # Delayed import to avoid circular dependency
        import lov

        self.notify("📚 You enter Death's vast library...")
        self.notify("Ancient tomes glow with forbidden knowledge!")

        # Knowledge always has a price
        knowledge_gained = random.choice(['combat', 'magic', 'life', 'death'])

        if knowledge_gained == 'combat':
            lov.current_player.strength += 2
            lov.current_player.defense += 1
            self.notify("Combat techniques from fallen warriors! (+2 STR, +1 DEF)")
        elif knowledge_gained == 'magic':
            lov.current_player.intelligence += 3
            self.notify("Arcane secrets expand your mind! (+3 Intelligence)")
        elif knowledge_gained == 'life':
            hp_boost = random.randint(20, 40)
            lov.current_player.max_hitpoints += hp_boost
            lov.current_player.hitpoints += hp_boost
            self.notify(f"Life force knowledge strengthens you! (+{hp_boost} Max HP)")
        else:  # death knowledge
            lov.current_player.charm += 3
            self.notify("Understanding death makes you more charismatic! (+3 Charm)")

        # But knowledge demands payment
        price = random.randint(200, 800)
        lov.current_player.gold = max(0, lov.current_player.gold - price)
        self.notify(f"Forbidden knowledge costs {price} gold...")

    def _meet_death(self):
        """Personal audience with Death"""
        # Delayed import to avoid circular dependency
        import lov

        self.notify("💀 Death sits upon his obsidian throne...")
        self.notify("'So, another mortal seeks to cheat death?'")
        self.notify("'I offer you a choice, brave one.'")

        # Death's bargain
        if lov.current_player.gold >= 1000:
            # Can afford death's bargain
            lov.current_player.gold -= 1000
            lov.current_player.max_hitpoints += 25
            lov.current_player.hitpoints += 25
            lov.current_player.strength += 2
            lov.current_player.defense += 2

            self.notify("💀 'For 1000 gold, I grant you resilience against death.'")
            self.notify("(+25 Max HP, +2 STR, +2 DEF)")
        else:
            # Too poor - Death takes pity
            self.notify("💀 'You are too poor to interest me.'")
            self.notify("'But I admire your courage. Take this small gift.'")
            lov.current_player.gems += 1
            self.notify("Death grants you 1 mystical gem.")

    def _enter_random_portal(self):
        """Enter a random portal with unknown destination"""
        # Delayed import to avoid circular dependency
        import lov

        # Deduct gem cost
        lov.current_player.gems -= 1

        self.notify("🌀 You step through a swirling portal of unknown energy...")
        self.notify("Reality shifts around you...")

        # Completely random outcomes
        outcomes = ['treasure_realm', 'void_dimension', 'mirror_world', 'time_distortion', 'elemental_plane']
        outcome = random.choice(outcomes)

        if outcome == 'treasure_realm':
            treasure = random.randint(1000, 3000) * lov.current_player.level
            gems = random.randint(1, 5)
            lov.current_player.gold += treasure
            lov.current_player.gems += gems
            self.notify(f"💰 You discover a treasure realm! (+{treasure:,} gold, +{gems} gems)")

        elif outcome == 'void_dimension':
            self.notify("🌌 You float in an endless void...")
            self.notify("The experience transcends mortal understanding.")
            lov.current_player.intelligence += 3
            lov.current_player.charm += 2
            self.notify("Your consciousness expands! (+3 INT, +2 Charm)")

        elif outcome == 'mirror_world':
            self.notify("🪞 You enter a world where everything is reversed...")
            # Swap two random stats
            stats = ['strength', 'defense', 'charm', 'intelligence']
            stat1, stat2 = random.sample(stats, 2)
            val1 = getattr(lov.current_player, stat1)
            val2 = getattr(lov.current_player, stat2)
            setattr(lov.current_player, stat1, val2)
            setattr(lov.current_player, stat2, val1)
            self.notify(f"Reality flips! {stat1.title()} and {stat2.title()} values swapped!")

        elif outcome == 'time_distortion':
            self.notify("⏰ Time flows strangely here...")
            # Reset daily limits
            lov.current_player.forest_fights = 15
            lov.current_player.cavern_searches_today = 0
            lov.current_player.werewolf_uses_today = 0
            lov.current_player.bank_robberies_today = 0
            self.notify("Time distortion resets your daily limits!")

        else:  # elemental_plane
            elements = ['Fire', 'Water', 'Earth', 'Air']
            element = random.choice(elements)
            self.notify(f"🔥 You arrive in the {element} Elemental Plane!")

            if element == 'Fire':
                lov.current_player.strength += 2
                self.notify("Fire's passion burns within you! (+2 Strength)")
            elif element == 'Water':
                heal = random.randint(20, 40)
                lov.current_player.hitpoints = min(lov.current_player.max_hitpoints,
                                                 lov.current_player.hitpoints + heal)
                self.notify(f"Water's flow heals your wounds! (+{heal} HP)")
            elif element == 'Earth':
                lov.current_player.defense += 2
                self.notify("Earth's stability fortifies you! (+2 Defense)")
            else:  # Air
                lov.current_player.charm += 2
                self.notify("Air's freedom lifts your spirit! (+2 Charm)")

        lov.game_db.save_player(lov.current_player)

    def _inspect_portals(self):
        """Inspect the portals without entering"""
        info_messages = [
            "The Zycho Zircus portal sparkles with carnival music and laughter.",
            "Death's Mansion portal emanates cold dread and whispers of mortality.",
            "The Random Portal shifts constantly, showing glimpses of infinite realms.",
            "Each portal requires 1 gem to activate the dimensional gateway.",
            "Portal travel is dangerous but can yield incredible rewards.",
            "Some say the portals reflect the traveler's inner nature...",
            "The gateway chamber was built by ancient mages long forgotten."
        ]

        for message in info_messages:
            self.notify(message)
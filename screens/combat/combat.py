"""
Combat screen for Legend of the Obsidian Vault
"""
import random
from typing import List
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static
from textual.containers import Horizontal, Vertical
from textual import events

# Import will be updated after refactor
from game_data import CLASS_TYPES, can_level_up
# Import globals - delayed to avoid circular import
from obsidian import vault


class CombatScreen(Screen):
    """Forest combat with Obsidian integration"""

    can_focus = True

    def __init__(self):
        super().__init__()
        self.enemy = None
        self.combat_log = []
        self.player_turn = True
        self.quiz_available = True
        self.is_master_fight = False
        self.master_level = None
        self.master_data = None

    def compose(self) -> ComposeResult:
        # Delayed import to avoid circular dependency
        import lov

        # Generate enemy based on player level and Obsidian notes (unless it's a master fight)
        if not self.is_master_fight and self.enemy is None:
            self.enemy = vault.get_enemy_for_level(lov.current_player.level)

        # Line 1-3: Header (3 lines) - Fixed alignment
        yield Static("╔═══════════════════════════════════════════════════════════════════════════╗", classes="bbs-header")
        yield Static("║                          ⚔️  MYSTICAL ENCOUNTER  ⚔️                       ║", classes="bbs-header")
        yield Static("╚═══════════════════════════════════════════════════════════════════════════╝", classes="bbs-header")

        # Narrative Section (4 lines)
        if hasattr(self.enemy, 'encounter_narrative') and self.enemy.encounter_narrative:
            narrative_lines = self._wrap_narrative_text_smart(self.enemy.encounter_narrative, 75, max_lines=4)
            for line in narrative_lines:
                yield Static(f" {line}", classes="narrative")
        else:
            yield Static(f" You discover the essence of '{self.enemy.note_title}' made manifest!", classes="narrative")
            yield Static(" Reality bends as knowledge takes physical form in this mystical realm.", classes="narrative")
            yield Static(" The air crackles with power as battle becomes inevitable...", classes="narrative")
            yield Static("", classes="narrative")

        # Separator line
        yield Static("═" * 79, classes="separator")

        # Enemy Status Section
        yield Static("", classes="separator")
        yield Static("【 ENEMY STATUS 】", classes="enemy-stats")
        yield Static(f"Name: {self.enemy.name[:50]}", classes="enemy-stats")

        enemy_max_hp = getattr(self.enemy, 'max_hitpoints', self.enemy.hitpoints)
        enemy_hp_bar = self._create_hp_bar(self.enemy.hitpoints, enemy_max_hp, 10)
        yield Static(f"HP:   {enemy_hp_bar}", classes="enemy-hp-bar", id="enemy_hp_display")

        enemy_attack = getattr(self.enemy, 'attack', 0)
        enemy_defense = getattr(self.enemy, 'defense', 0)
        yield Static(f"Level: {self.enemy.level}   ATK: {enemy_attack}   DEF: {enemy_defense}", classes="enemy-stats")

        enemy_weapon = getattr(self.enemy, 'weapon', 'Unknown')
        enemy_armor = getattr(self.enemy, 'armor', 'Unknown')
        yield Static(f"Weapon: {enemy_weapon[:30]}   Armor: {enemy_armor[:30]}", classes="enemy-stats")

        # Separator between enemy and player
        yield Static("─" * 79, classes="separator")

        # Player Status Section
        yield Static("【 PLAYER STATUS 】", classes="player-stats")
        yield Static(f"Name: {lov.current_player.name}", classes="player-stats")

        player_hp_bar = self._create_hp_bar(lov.current_player.hitpoints, lov.current_player.max_hitpoints, 10)
        yield Static(f"HP:   {player_hp_bar}", classes="player-hp-bar", id="player_hp_display")

        yield Static(f"Level: {lov.current_player.level}   ATK: {lov.current_player.attack_power}   DEF: {lov.current_player.defense_power}   Gold: {lov.current_player.gold}", classes="player-stats")

        from game_data import WEAPONS, ARMOR
        player_weapon = WEAPONS[lov.current_player.weapon_num][0]
        player_armor = ARMOR[lov.current_player.armor_num][0]
        yield Static(f"Weapon: {player_weapon[:30]}   Armor: {player_armor[:30]}", classes="player-stats")

        yield Static("═" * 79, classes="separator")

        # Commands Section
        yield Static("", classes="separator")
        yield Static("⚔️  BATTLE COMMANDS  ⚔️", classes="combat-commands")
        yield Static("(A)ttack  (K)nowledge Quiz  (S)skill  (R)un Away", classes="combat-commands")

        # Combat Log and Input
        yield Static("", classes="separator")
        yield Static("Ready for combat...", id="combat_feedback", classes="combat-log")
        yield Static("> Your command? _", classes="prompt")

    def _create_hp_bar(self, current_hp: int, max_hp: int, width: int = 10, bar_type: str = "player") -> str:
        """Create a visual HP bar using Unicode blocks like █░░░░░░░░░ 10%"""
        if max_hp <= 0:
            return "░" * width + " 0%"

        # Calculate percentage
        percentage = current_hp / max_hp
        percent_value = round(percentage * 100)

        # Calculate filled blocks (out of width)
        filled_blocks = round(percentage * width)
        empty_blocks = width - filled_blocks

        # Ensure we don't exceed width
        filled_blocks = max(0, min(filled_blocks, width))
        empty_blocks = max(0, width - filled_blocks)

        # Create bar with filled (█) and empty (░) Unicode blocks
        # Use different characters that are more visually distinct
        filled_char = "█"  # Full block
        empty_char = "░"   # Light shade

        hp_bar = filled_char * filled_blocks + empty_char * empty_blocks
        return f"{hp_bar} {percent_value}%"

    def _wrap_narrative_text(self, text: str, width: int) -> List[str]:
        """Wrap narrative text to fit within specified width"""
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            if len(test_line) <= width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines

    def _wrap_narrative_text_smart(self, text: str, width: int, max_lines: int = 6) -> List[str]:
        """Smart wrap narrative text with sentence awareness and overflow handling"""
        # Split by sentences first to avoid mid-sentence cuts
        import re
        sentences = re.split(r'([.!?]+\s+)', text)
        combined_text = ''.join(sentences)  # Rejoin to maintain original text

        # Use basic word wrapping
        words = combined_text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            if len(test_line) <= width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

                # Stop if we're approaching the max lines limit
                if len(lines) >= max_lines - 1:
                    break

        # Add the last line if we have content
        if current_line and len(lines) < max_lines:
            lines.append(current_line)

        # If we have more content, add ellipsis to the last line
        if len(lines) == max_lines and len(' '.join(words)) > sum(len(line) for line in lines):
            if lines:
                last_line = lines[-1]
                if len(last_line) > width - 3:
                    lines[-1] = last_line[:width-3] + "..."
                else:
                    lines[-1] = last_line + "..."

        # Ensure we return exactly max_lines (pad with empty if needed)
        while len(lines) < max_lines:
            lines.append("")

        return lines[:max_lines]

    def on_mount(self) -> None:
        """Focus the screen when it loads"""
        self.focus()

    def on_key(self, event) -> None:
        """Handle keyboard input for combat"""
        # Delayed import to avoid circular dependency
        import lov

        key = event.key.upper()

        if key == "A":
            self._player_attack()
        elif key == "K":
            self._knowledge_attack()
        elif key == "S":
            # Check if they mean skill attack or show stats
            if hasattr(lov.current_player, 'can_use_skill') and lov.current_player.can_use_skill():
                self._skill_attack()
            else:
                self._show_stats()
        elif key == "R":
            self._run_away()

    def _generate_attack_narrative(self, damage: int, attack_type: str, skill_name: str = "", mastery_msg: str = "") -> str:
        """Generate narrative attack descriptions based on enemy lore"""

        if hasattr(self.enemy, 'knowledge_domain') and self.enemy.knowledge_domain:
            domain = self.enemy.knowledge_domain

            if attack_type == "normal":
                # Normal attack narratives based on knowledge domain
                domain_attacks = {
                    "Code Mysteries": [
                        f"Your programming logic cuts through the guardian's defensive syntax for {damage} insight!",
                        f"You exploit a logical vulnerability, dealing {damage} computational damage!",
                        f"Your understanding of algorithms pierces through for {damage} processing power!"
                    ],
                    "Memory Fragments": [
                        f"Your empathy connects with buried memories, dealing {damage} emotional resonance!",
                        f"You channel personal understanding for {damage} heartfelt damage!",
                        f"Your compassion breaks through protective barriers for {damage} soul damage!"
                    ],
                    "Council Echoes": [
                        f"Your leadership experience counters their authority for {damage} decisive damage!",
                        f"You challenge their organizational structure, dealing {damage} hierarchical disruption!",
                        f"Your diplomatic skills break through for {damage} persuasive impact!"
                    ],
                    "Project Forge": [
                        f"Your project management skills disrupt their workflow for {damage} efficiency damage!",
                        f"You apply methodical precision, dealing {damage} structured impact!",
                        f"Your organizational prowess cuts through chaos for {damage} systematic damage!"
                    ]
                }

                # Get domain-specific attacks or use generic ones
                attack_options = domain_attacks.get(domain, [
                    f"Your knowledge of {domain} strikes true for {damage} wisdom damage!",
                    f"You channel understanding of {domain}, dealing {damage} intellectual impact!",
                    f"Your comprehension pierces their defenses for {damage} enlightenment damage!"
                ])

                return random.choice(attack_options)

            elif attack_type == "skill":
                # Skill-based attacks with domain integration
                skill_narratives = {
                    "Death Strike": f"Your Death Knight mastery channels through {domain}, unleashing {damage} necromantic force!{mastery_msg}",
                    "Mystical Blast": f"Your mystical energies resonate with {domain}, dealing {damage} arcane damage!{mastery_msg}",
                    "Sneak Attack": f"You slip past their defenses using knowledge of {domain} for {damage} cunning damage!{mastery_msg}"
                }

                return skill_narratives.get(skill_name,
                    f"{skill_name}! Your expertise channels through {domain} for {damage} enhanced damage!{mastery_msg}")

        else:
            # Fallback for enemies without lore
            if attack_type == "normal":
                return f"You strike for {damage} damage!"
            else:
                return f"{skill_name}! You hit for {damage} damage!{mastery_msg}"

    def _generate_enemy_attack_narrative(self, damage: int) -> str:
        """Generate narrative enemy attack descriptions"""

        if hasattr(self.enemy, 'combat_phrases') and self.enemy.combat_phrases:
            # Use enemy's combat phrases occasionally
            if random.random() < 0.3:  # 30% chance to speak during attack
                phrase = random.choice(self.enemy.combat_phrases)
                return f'{self.enemy.name} snarls: "{phrase}" - The attack deals {damage} damage!'

        if hasattr(self.enemy, 'knowledge_domain') and self.enemy.knowledge_domain:
            domain = self.enemy.knowledge_domain

            domain_attacks = {
                "Code Mysteries": [
                    f"{self.enemy.name} compiles a syntax error, dealing {damage} confusion damage!",
                    f"A recursive loop of logic crashes into you for {damage} processing damage!",
                    f"{self.enemy.name} executes a debugging nightmare for {damage} mental strain!"
                ],
                "Memory Fragments": [
                    f"{self.enemy.name} projects painful memories, dealing {damage} emotional damage!",
                    f"Waves of nostalgia overwhelm you for {damage} sentimental damage!",
                    f"Forgotten regrets materialize, striking for {damage} psychological impact!"
                ],
                "Council Echoes": [
                    f"{self.enemy.name} unleashes bureaucratic confusion for {damage} administrative damage!",
                    f"A barrage of meeting jargon deals {damage} corporate fatigue!",
                    f"Endless procedure protocols strike for {damage} organizational chaos!"
                ],
                "Project Forge": [
                    f"{self.enemy.name} hurls shifting deadlines, dealing {damage} stress damage!",
                    f"Scope creep materializes around you for {damage} requirement damage!",
                    f"A cascade of dependencies crashes down for {damage} project disruption!"
                ]
            }

            attack_options = domain_attacks.get(domain, [
                f"{self.enemy.name} channels the power of {domain} for {damage} knowledge damage!",
                f"Mystical energy from {domain} strikes you for {damage} wisdom drain!",
                f"The guardian's {domain} mastery deals {damage} understanding damage!"
            ])

            return random.choice(attack_options)

        else:
            # Fallback for basic enemies
            return f"{self.enemy.name} attacks you for {damage} damage!"

    def _update_combat_display(self):
        """Update both HP bars and combat status in real-time"""
        # Delayed import to avoid circular dependency
        import lov

        try:
            # Update enemy HP bar
            enemy_hp_element = self.query_one("#enemy_hp_display")
            enemy_max_hp = getattr(self.enemy, 'max_hitpoints', self.enemy.hitpoints)
            enemy_hp_bar = self._create_hp_bar(self.enemy.hitpoints, enemy_max_hp, 10)
            enemy_hp_element.update(f"HP:   {enemy_hp_bar}")

            # Update player HP bar
            player_hp_element = self.query_one("#player_hp_display")
            player_hp_bar = self._create_hp_bar(lov.current_player.hitpoints, lov.current_player.max_hitpoints, 10)
            player_hp_element.update(f"HP:   {player_hp_bar}")

            # Update combat feedback
            feedback_element = self.query_one("#combat_feedback")
            status_msg = f"⚔️ Battle continues... You: {lov.current_player.hitpoints} HP | {self.enemy.name[:20]}: {self.enemy.hitpoints} HP"
            feedback_element.update(status_msg)

        except Exception as e:
            # Fallback to notification if update fails
            self.notify(f"HP Update: You {lov.current_player.hitpoints}, Enemy {self.enemy.hitpoints}")

    def _refresh_combat_display(self, message: str = ""):
        """Refresh the entire combat display with optional message"""
        self._update_combat_display()
        if message:
            try:
                feedback_element = self.query_one("#combat_feedback")
                feedback_element.update(message)
            except:
                self.notify(message)

    def _player_attack(self):
        # Delayed import to avoid circular dependency
        import lov

        """Player normal attack"""
        try:
            damage = random.randint(1, lov.current_player.attack_power)
            self.enemy.hitpoints -= damage

            # Generate narrative attack message
            attack_message = self._generate_attack_narrative(damage, "normal")
            self._refresh_combat_display(f"⚔️ {attack_message}")

            if self.enemy.hitpoints <= 0:
                self._victory()
            else:
                self._enemy_attack()

        except Exception as e:
            self.notify(f"Combat error: {str(e)}")
            # Return to forest if combat fails
            self.app.pop_screen()

    def _knowledge_attack(self):
        """Player knowledge attack (quiz)"""
        if not hasattr(self.enemy, 'note_title') or not self.enemy.note_title:
            self.notify("No knowledge to test with this enemy!")
            return

        # Switch to quiz screen
        from .quiz import QuizScreen
        self.app.push_screen(QuizScreen(self.enemy, self))

    def _show_stats(self):
        """Show player stats"""
        from ..character.stats import StatsScreen
        self.app.push_screen(StatsScreen())

    def _skill_attack(self):
        # Delayed import to avoid circular dependency
        import lov

        """Player special skill attack"""
        if not lov.current_player.can_use_skill():
            self.notify("You have no skill uses remaining today!")
            return

        lov.current_player.use_skill()
        skill_type = lov.current_player.class_type
        skill_points = lov.current_player.get_skill_points(skill_type)

        # Calculate damage based on skill points
        base_damage = lov.current_player.attack_power
        skill_multiplier = 1.0 + (skill_points * 0.05)  # 5% per skill point

        if skill_type == 'K':  # Death Knight
            damage = int(base_damage * skill_multiplier * random.uniform(1.5, 2.5))
            skill_name = "Death Knight Strike"
        elif skill_type == 'P':  # Mystical
            damage = int(base_damage * skill_multiplier * random.uniform(1.3, 2.0))
            skill_name = "Mystical Blast"
        elif skill_type == 'D':  # Thieving
            damage = int(base_damage * skill_multiplier * random.uniform(1.2, 2.2))
            skill_name = "Sneak Attack"
        else:
            damage = base_damage
            skill_name = "Skill Attack"

        self.enemy.hitpoints -= damage

        # Ultra-mastery bonus message
        mastery_msg = ""
        if lov.current_player.has_ultra_mastery(skill_type):
            mastery_msg = " **ULTRA MASTERY!**"

        uses_left = CLASS_TYPES[skill_type]['daily_uses'] - lov.current_player.skills_used_today

        # Generate narrative skill attack description
        skill_description = self._generate_attack_narrative(damage, "skill", skill_name, mastery_msg)
        self._refresh_combat_display(f"✨ {skill_description} ({uses_left} uses left)")

        if self.enemy.hitpoints <= 0:
            self._victory()
        else:
            self._enemy_attack()

    def quiz_attack(self, correct: bool):
        """Quiz-based attack from QuizScreen"""
        # Delayed import to avoid circular dependency
        import lov

        self.quiz_available = False

        if correct:
            damage = lov.current_player.attack_power * 2
            self.enemy.hitpoints -= damage
            self._refresh_combat_display(f"⭐ **CRITICAL HIT** Your knowledge strikes for {damage} damage!")
        else:
            self._refresh_combat_display("❌ Your knowledge fails you! No damage dealt.")

        if self.enemy.hitpoints <= 0:
            self._victory()
        else:
            self._enemy_attack()

    def _enemy_attack(self):
        # Delayed import to avoid circular dependency
        import lov

        """Enemy attacks player"""
        try:
            damage = random.randint(1, self.enemy.attack)
            damage = max(1, damage - (lov.current_player.defense_power // 2))
            lov.current_player.hitpoints -= damage

            # Generate narrative enemy attack message
            attack_message = self._generate_enemy_attack_narrative(damage)
            self._refresh_combat_display(f"🔥 {attack_message}")

            if lov.current_player.hitpoints <= 0:
                self._defeat()

        except Exception as e:
            self.notify(f"Enemy attack error: {str(e)}")
            # Continue combat despite error

    def _victory(self):
        # Delayed import to avoid circular dependency
        import lov

        """Player wins combat"""
        if self.is_master_fight:
            # Master fight - level up automatically
            lov.current_player.experience += self.enemy.exp_reward
            lov.current_player.gold += self.enemy.gold_reward

            self.notify(f"{self.enemy.death_phrase}")
            self.notify(f"You receive {self.enemy.exp_reward} experience and {self.enemy.gold_reward} gold!")

            # Perform authentic level up
            lov.current_player.level_up_authentic()

            # Show master's victory message
            victory_msg = self.master_data.get('victory', 'You have defeated the master!')
            self.notify(f'Master {self.master_data["name"]} says:')
            self.notify(f'"{victory_msg}"')

            # Award weapon
            weapon_name = self.master_data['weapon']
            self.notify(f"You have earned the {weapon_name}!")

            # Show level up text
            level_up_text = self.master_data.get('level_up_text', f'You are now level {lov.current_player.level}!')
            self.notify(f'"{level_up_text}"')

        else:
            # Regular forest fight
            lov.current_player.forest_fights -= 1
            lov.current_player.experience += self.enemy.exp_reward
            lov.current_player.gold += self.enemy.gold_reward
            lov.current_player.total_kills += 1  # Track total kills for Hall of Honours

            # Use enemy's defeat message if available
            if hasattr(self.enemy, 'defeat_message') and self.enemy.defeat_message:
                self.notify(f'💀 {self.enemy.defeat_message}')
            else:
                self.notify(f"You have defeated {self.enemy.name}!")

            self.notify(f"✨ You receive {self.enemy.exp_reward} experience and {self.enemy.gold_reward} gold!")

            # Check for level up (but not automatic)
            if can_level_up(lov.current_player):
                self.notify("You have enough experience to visit a master for training!")

        lov.game_db.save_player(lov.current_player)
        self.app.pop_screen()

    def _defeat(self):
        # Delayed import to avoid circular dependency
        import lov

        """Player loses combat"""
        lov.current_player.hitpoints = 0
        lov.current_player.alive = False
        lov.current_player.gold = 0  # Lose all carried gold

        self.notify("You have been defeated!")
        self.notify("You lose all your gold and awaken in the healer's hut tomorrow.")

        lov.game_db.save_player(lov.current_player)
        self.app.pop_screen()

    def _run_away(self):
        """Player runs from combat"""
        self.notify(f"You run away from {self.enemy.name}!")
        self.app.pop_screen()
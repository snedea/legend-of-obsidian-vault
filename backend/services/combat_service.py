from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Optional

import sys
from pathlib import Path

_project_root = str(Path(__file__).resolve().parent.parent.parent)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from game_data import (
    Character, Enemy, CLASS_TYPES, FOREST_ENEMIES,
    can_level_up, create_master_enemy, MASTERS,
)
from obsidian import vault
from brainbot import sync_generate_quiz_question


@dataclass
class CombatState:
    enemy: Enemy
    combat_active: bool = True
    player_turn: bool = True
    quiz_available: bool = True
    is_master_fight: bool = False
    master_level: Optional[int] = None
    master_data: Optional[dict] = None
    log: list[str] = field(default_factory=list)
    # Stored quiz so answer validates against the same question that was served
    pending_quiz: Optional[dict] = None


class CombatService:
    """Stateless combat logic extracted from CombatScreen."""

    def enter_forest(self, player: Character) -> CombatState:
        """Generate an enemy and create a new combat state."""
        enemy = vault.get_enemy_for_level(player.level)
        state = CombatState(enemy=enemy)
        state.log.append(f"You encounter {enemy.name}!")
        return state

    def start_master_fight(self, player: Character, level: int) -> CombatState:
        """Start a master challenge fight."""
        master_data = MASTERS.get(level)
        if not master_data:
            raise ValueError(f"No master at level {level}")
        enemy = create_master_enemy(level, master_data)
        state = CombatState(
            enemy=enemy,
            is_master_fight=True,
            master_level=level,
            master_data=master_data,
        )
        state.log.append(f"You challenge Master {master_data['name']}!")
        return state

    def player_attack(self, player: Character, state: CombatState) -> dict:
        """Execute player normal attack + enemy counterattack. Returns result dict."""
        enemy = state.enemy

        # LORD v4.00a formula: monsters have NO defense
        strength = player.attack_power
        hit_amount = (strength // 2) + random.randint(0, strength // 2)

        player_hit = hit_amount > 0
        player_damage = max(0, hit_amount)

        if player_hit:
            enemy.hitpoints -= player_damage
            player_msg = self._attack_narrative(player_damage, enemy, "normal")
        else:
            player_msg = "You swing wildly and MISS!"

        state.log.append(player_msg)

        # Check victory
        if enemy.hitpoints <= 0:
            rewards = self._victory(player, state)
            return self._result(
                player, state, player_damage, player_hit, player_msg,
                0, False, "", combat_over=True, victory=True, rewards=rewards,
            )

        # Enemy counterattack
        e_damage, e_hit, e_msg = self._enemy_attack(player, state)

        combat_over = player.hitpoints <= 0
        if combat_over:
            self._defeat(player, state)

        return self._result(
            player, state, player_damage, player_hit, player_msg,
            e_damage, e_hit, e_msg, combat_over=combat_over, victory=False,
        )

    def skill_attack(self, player: Character, state: CombatState) -> dict:
        """Execute player skill attack + enemy counterattack."""
        if not player.can_use_skill():
            return self._result(
                player, state, 0, False, "No skill uses remaining!",
                0, False, "", combat_over=False, victory=False,
            )

        player.use_skill()
        skill_type = player.class_type
        skill_points = player.get_skill_points(skill_type)
        base_damage = player.attack_power
        skill_multiplier = 1.0 + (skill_points * 0.05)

        if skill_type == "K":
            damage = int(base_damage * skill_multiplier * random.uniform(1.5, 2.5))
            skill_name = "Death Knight Strike"
        elif skill_type == "P":
            damage = int(base_damage * skill_multiplier * random.uniform(1.3, 2.0))
            skill_name = "Mystical Blast"
        elif skill_type == "D":
            damage = int(base_damage * skill_multiplier * random.uniform(1.2, 2.2))
            skill_name = "Sneak Attack"
        else:
            damage = base_damage
            skill_name = "Skill Attack"

        state.enemy.hitpoints -= damage
        mastery = " ULTRA MASTERY!" if player.has_ultra_mastery(skill_type) else ""
        player_msg = f"{skill_name}! You hit for {damage} damage!{mastery}"
        state.log.append(player_msg)

        if state.enemy.hitpoints <= 0:
            rewards = self._victory(player, state)
            return self._result(
                player, state, damage, True, player_msg,
                0, False, "", combat_over=True, victory=True, rewards=rewards,
            )

        e_damage, e_hit, e_msg = self._enemy_attack(player, state)
        combat_over = player.hitpoints <= 0
        if combat_over:
            self._defeat(player, state)

        return self._result(
            player, state, damage, True, player_msg,
            e_damage, e_hit, e_msg, combat_over=combat_over, victory=False,
        )

    def fairy_heal(self, player: Character, state: CombatState) -> dict:
        """Fairy lore heal + enemy counterattack."""
        if not player.fairy_lore:
            return {"success": False, "message": "You don't know Fairy Lore healing!"}

        max_heal = int(player.max_hitpoints * 0.40)
        min_heal = int(player.max_hitpoints * 0.25)
        heal_amount = random.randint(min_heal, max_heal)

        old_hp = player.hitpoints
        player.hitpoints = min(player.max_hitpoints, player.hitpoints + heal_amount)
        actual_heal = player.hitpoints - old_hp

        heal_msg = f"Fairy magic restores {actual_heal} HP!"
        state.log.append(heal_msg)

        # Enemy counterattack
        e_damage, e_hit, e_msg = self._enemy_attack(player, state)
        combat_over = player.hitpoints <= 0
        if combat_over:
            self._defeat(player, state)

        return {
            "heal_amount": actual_heal,
            "player_hp": player.hitpoints,
            "player_max_hp": player.max_hitpoints,
            "message": heal_msg,
            "enemy_damage": e_damage,
            "enemy_hit": e_hit,
            "enemy_message": e_msg,
            "enemy_hp": state.enemy.hitpoints,
            "combat_over": combat_over,
            "victory": False,
        }

    def quiz_start(self, state: CombatState) -> dict:
        """Generate a quiz question for the current enemy and store it in state."""
        enemy = state.enemy
        if not enemy.note_title or not enemy.note_content:
            return {"error": "No knowledge to test with this enemy"}

        quiz = sync_generate_quiz_question(enemy.note_title, enemy.note_content)
        # Store the quiz so quiz_answer validates against the same question
        state.pending_quiz = {
            "question": quiz.question,
            "options": quiz.options,
            "correct_index": quiz.correct_index,
            "difficulty": quiz.difficulty,
            "question_type": quiz.question_type,
        }
        return state.pending_quiz

    def quiz_answer(self, player: Character, state: CombatState, selected_index: int) -> dict:
        """Process quiz answer. Correct = 2x damage critical hit."""
        if not state.pending_quiz:
            return {"error": "No pending quiz question"}

        correct = selected_index == state.pending_quiz["correct_index"]
        state.pending_quiz = None
        state.quiz_available = False

        enemy = state.enemy
        if correct:
            damage = player.attack_power * 2
            enemy.hitpoints -= damage
            player_msg = f"CRITICAL HIT! Knowledge strikes for {damage} damage!"
        else:
            damage = 0
            player_msg = "Your knowledge fails you! No damage dealt."

        state.log.append(player_msg)

        if enemy.hitpoints <= 0:
            rewards = self._victory(player, state)
            return {
                "correct": correct,
                "damage": damage,
                "message": player_msg,
                "enemy_damage": 0,
                "enemy_hit": False,
                "enemy_message": "",
                "enemy_hp": enemy.hitpoints,
                "player_hp": player.hitpoints,
                "combat_over": True,
                "victory": True,
                "rewards": rewards,
            }

        e_damage, e_hit, e_msg = self._enemy_attack(player, state)
        combat_over = player.hitpoints <= 0
        if combat_over:
            self._defeat(player, state)

        return {
            "correct": correct,
            "damage": damage,
            "message": player_msg,
            "enemy_damage": e_damage,
            "enemy_hit": e_hit,
            "enemy_message": e_msg,
            "enemy_hp": enemy.hitpoints,
            "player_hp": player.hitpoints,
            "combat_over": combat_over,
            "victory": False,
        }

    def flee(self, state: CombatState) -> dict:
        """Player flees combat."""
        state.combat_active = False
        msg = f"You run away from {state.enemy.name}!"
        state.log.append(msg)
        return {"success": True, "message": msg}

    # -- Private helpers --

    def _enemy_attack(self, player: Character, state: CombatState) -> tuple[int, bool, str]:
        """Enemy attacks player. Returns (damage, hit, message)."""
        strength = state.enemy.attack
        defense = player.defense_power
        hit_amount = (strength // 2) + random.randint(0, strength // 2) - defense

        if hit_amount <= 0:
            msg = "The enemy's attack is deflected by your defenses!"
            state.log.append(msg)
            return 0, False, msg

        damage = hit_amount
        player.hitpoints -= damage
        msg = f"{state.enemy.name} attacks you for {damage} damage!"
        state.log.append(msg)
        return damage, True, msg

    def _victory(self, player: Character, state: CombatState) -> dict:
        """Handle victory. Returns rewards dict."""
        enemy = state.enemy
        state.combat_active = False

        rewards: dict = {
            "gold": enemy.gold_reward,
            "experience": enemy.exp_reward,
            "level_up": False,
            "level_up_gains": None,
            "can_train": False,
        }

        if state.is_master_fight:
            player.experience += enemy.exp_reward
            player.gold += enemy.gold_reward
            gains = player.level_up_authentic()
            if gains:
                rewards["level_up"] = True
                rewards["level_up_gains"] = gains
        else:
            player.forest_fights -= 1
            player.experience += enemy.exp_reward
            player.gold += enemy.gold_reward
            player.total_kills += 1
            rewards["can_train"] = can_level_up(player)

        return rewards

    def _defeat(self, player: Character, state: CombatState) -> None:
        """Handle defeat."""
        state.combat_active = False
        player.hitpoints = 0
        player.alive = False
        player.gold = 0

    def _attack_narrative(self, damage: int, enemy: Enemy, attack_type: str) -> str:
        domain = getattr(enemy, "knowledge_domain", "")
        if domain and attack_type == "normal":
            return f"Your knowledge of {domain} strikes true for {damage} wisdom damage!"
        return f"You strike for {damage} damage!"

    def _result(
        self,
        player: Character,
        state: CombatState,
        player_damage: int,
        player_hit: bool,
        player_message: str,
        enemy_damage: int,
        enemy_hit: bool,
        enemy_message: str,
        combat_over: bool,
        victory: bool,
        rewards: Optional[dict] = None,
    ) -> dict:
        return {
            "player_damage": player_damage,
            "player_hit": player_hit,
            "player_message": player_message,
            "enemy_damage": enemy_damage,
            "enemy_hit": enemy_hit,
            "enemy_message": enemy_message,
            "enemy_hp": state.enemy.hitpoints,
            "player_hp": player.hitpoints,
            "combat_over": combat_over,
            "victory": victory,
            "rewards": rewards,
            "log": list(state.log),
        }


# Global singleton
combat_service = CombatService()

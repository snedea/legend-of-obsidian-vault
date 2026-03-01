from __future__ import annotations

import random
import sys
from pathlib import Path

_project_root = str(Path(__file__).resolve().parent.parent.parent)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from game_data import Character, WEAPONS, ARMOR, HEALING_COSTS


class ShopService:
    """Buy/sell logic for weapons, armor, and healing."""

    def list_weapons(self, player: Character) -> list[dict]:
        items = []
        for i, (name, price, attack) in enumerate(WEAPONS):
            can_buy = i <= player.weapon_num + 1 and i != player.weapon_num and player.gold >= price
            items.append({
                "index": i,
                "name": name,
                "price": price,
                "stat_value": attack,
                "owned": i == player.weapon_num,
                "can_buy": can_buy,
            })
        return items

    def buy_weapon(self, player: Character, index: int) -> dict:
        if index < 0 or index >= len(WEAPONS):
            return {"success": False, "message": "Invalid weapon", "gold_remaining": player.gold, "item_name": ""}
        if index > player.weapon_num + 1:
            return {"success": False, "message": "You must buy weapons in order", "gold_remaining": player.gold, "item_name": ""}
        name, price, _attack = WEAPONS[index]
        if player.gold < price:
            return {"success": False, "message": "Not enough gold", "gold_remaining": player.gold, "item_name": name}
        player.gold -= price
        player.weapon_num = index
        player.weapon = name
        return {"success": True, "message": f"You purchased {name}!", "gold_remaining": player.gold, "item_name": name}

    def list_armor(self, player: Character) -> list[dict]:
        items = []
        for i, (name, price, defense) in enumerate(ARMOR):
            can_buy = i <= player.armor_num + 1 and i != player.armor_num and player.gold >= price
            items.append({
                "index": i,
                "name": name,
                "price": price,
                "stat_value": defense,
                "owned": i == player.armor_num,
                "can_buy": can_buy,
            })
        return items

    def buy_armor(self, player: Character, index: int) -> dict:
        if index < 0 or index >= len(ARMOR):
            return {"success": False, "message": "Invalid armor", "gold_remaining": player.gold, "item_name": ""}
        if index > player.armor_num + 1:
            return {"success": False, "message": "You must buy armor in order", "gold_remaining": player.gold, "item_name": ""}
        name, price, _defense = ARMOR[index]
        if player.gold < price:
            return {"success": False, "message": "Not enough gold", "gold_remaining": player.gold, "item_name": name}
        player.gold -= price
        player.armor_num = index
        player.armor = name
        return {"success": True, "message": f"You purchased {name}!", "gold_remaining": player.gold, "item_name": name}

    def get_healer_info(self, player: Character) -> dict:
        full_cost = HEALING_COSTS.get(player.level, 50)
        hp_missing = player.max_hitpoints - player.hitpoints
        return {
            "full_heal_cost": full_cost,
            "per_hp_cost": 1,
            "hp_missing": hp_missing,
            "current_hp": player.hitpoints,
            "max_hp": player.max_hitpoints,
            "current_gold": player.gold,
        }

    def heal_full(self, player: Character) -> dict:
        cost = HEALING_COSTS.get(player.level, 50)
        if player.gold < cost:
            return {"success": False, "message": "Not enough gold", "hp_healed": 0, "gold_spent": 0,
                    "current_hp": player.hitpoints, "current_gold": player.gold}
        if player.hitpoints >= player.max_hitpoints:
            return {"success": False, "message": "Already at full health", "hp_healed": 0, "gold_spent": 0,
                    "current_hp": player.hitpoints, "current_gold": player.gold}
        hp_healed = player.max_hitpoints - player.hitpoints
        player.gold -= cost
        player.hitpoints = player.max_hitpoints
        return {"success": True, "message": f"Fully healed for {cost} gold!", "hp_healed": hp_healed,
                "gold_spent": cost, "current_hp": player.hitpoints, "current_gold": player.gold}

    def heal_partial(self, player: Character, amount: int) -> dict:
        hp_missing = player.max_hitpoints - player.hitpoints
        heal_amount = min(amount, hp_missing)
        cost = heal_amount  # 1 gold per HP
        if player.gold < cost:
            heal_amount = player.gold
            cost = heal_amount
        if heal_amount <= 0:
            return {"success": False, "message": "Nothing to heal or no gold", "hp_healed": 0, "gold_spent": 0,
                    "current_hp": player.hitpoints, "current_gold": player.gold}
        player.gold -= cost
        player.hitpoints += heal_amount
        return {"success": True, "message": f"Healed {heal_amount} HP for {cost} gold!", "hp_healed": heal_amount,
                "gold_spent": cost, "current_hp": player.hitpoints, "current_gold": player.gold}

    def bank_deposit(self, player: Character, amount: int) -> dict:
        amount = min(amount, player.gold)
        if amount <= 0:
            return {"success": False, "message": "No gold to deposit", "gold": player.gold, "bank_gold": player.bank_gold}
        player.gold -= amount
        player.bank_gold += amount
        return {"success": True, "message": f"Deposited {amount:,} gold", "gold": player.gold, "bank_gold": player.bank_gold}

    def bank_withdraw(self, player: Character, amount: int) -> dict:
        amount = min(amount, player.bank_gold)
        if amount <= 0:
            return {"success": False, "message": "No gold to withdraw", "gold": player.gold, "bank_gold": player.bank_gold}
        player.bank_gold -= amount
        player.gold += amount
        return {"success": True, "message": f"Withdrew {amount:,} gold", "gold": player.gold, "bank_gold": player.bank_gold}

    def bank_rob(self, player: Character) -> dict:
        if player.class_type != "D":
            return {"success": False, "message": "Only thieves can rob the bank", "gold_change": 0,
                    "gold": player.gold, "bank_gold": player.bank_gold}
        if not player.fairy_lore:
            return {"success": False, "message": "You need fairy lore to attempt robbery", "gold_change": 0,
                    "gold": player.gold, "bank_gold": player.bank_gold}
        if player.bank_robberies_today > 0:
            return {"success": False, "message": "Already attempted robbery today", "gold_change": 0,
                    "gold": player.gold, "bank_gold": player.bank_gold}

        player.bank_robberies_today += 1
        thieving_points = player.get_skill_points("D")
        success_chance = min(80, 30 + (thieving_points * 5) + (player.level * 2))

        if random.randint(1, 100) <= success_chance:
            pool = max(1000, player.bank_gold * 5)
            steal_pct = random.randint(10, 30) / 100
            stolen = int(pool * steal_pct)
            player.gold += stolen
            player.successful_robberies += 1
            player.add_skill_points("D", 1)
            return {"success": True, "message": f"You steal {stolen:,} gold!", "gold_change": stolen,
                    "gold": player.gold, "bank_gold": player.bank_gold}
        else:
            fine = player.gold // 2
            player.gold -= fine
            return {"success": False, "message": f"Caught! Fined {fine:,} gold.", "gold_change": -fine,
                    "gold": player.gold, "bank_gold": player.bank_gold}


shop_service = ShopService()

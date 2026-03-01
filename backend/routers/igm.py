from __future__ import annotations

import random
from fastapi import APIRouter, HTTPException

from backend.models.requests import RiddlerAnswerRequest, XenonTransactionRequest
from backend.models.responses import (
    CavernResultResponse, FairyResultResponse, BarakResultResponse,
    XenonStatusResponse, XenonResultResponse,
    WerewolfStatusResponse, WerewolfResultResponse,
    GatewayResultResponse,
)
from backend.services.game_service import session

router = APIRouter(prefix="/api/igm", tags=["igm"])

# Riddler puzzles (same as cavern.py)
_RIDDLES = [
    ("I have cities, but no houses. I have mountains, but no trees. I have water, but no fish. What am I?", "map"),
    ("The more you take, the more you leave behind. What am I?", "footsteps"),
    ("I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?", "echo"),
    ("I have keys but no locks. I have space but no room. You can enter but can't go inside. What am I?", "keyboard"),
    ("What has a heart that doesn't beat?", "artichoke"),
]

# Stored riddle so answer validates against the served question
_pending_riddle: dict | None = None


# -- Cavern --

@router.post("/cavern/explore")
def cavern_explore() -> CavernResultResponse:
    player = session.require_player()
    if player.cavern_searches_today >= 3:
        return CavernResultResponse(
            action="explore", success=False,
            message="You've searched the cavern enough today (3/3).",
            searches_remaining=0,
        )
    player.cavern_searches_today += 1
    roll = random.randint(1, 100)

    rewards = {}
    if roll <= 30:
        gold = random.randint(50, 200) * player.level
        player.gold += gold
        msg = f"You find {gold:,} gold hidden in the cavern walls!"
        rewards["gold"] = gold
    elif roll <= 50:
        gems = random.randint(1, 3)
        player.gems += gems
        msg = f"Glittering gems! You find {gems} gem(s)!"
        rewards["gems"] = gems
    elif roll <= 70:
        dmg = random.randint(5, 15)
        player.hitpoints = max(1, player.hitpoints - dmg)
        msg = f"A trap! You take {dmg} damage!"
        rewards["damage"] = dmg
    elif roll <= 85:
        msg = "You explore the dark passages but find nothing of interest."
    else:
        msg = "You sense ancient power but cannot harness it."

    session.save_player()
    return CavernResultResponse(
        action="explore", success=roll <= 50,
        message=msg, rewards=rewards if rewards else None,
        searches_remaining=3 - player.cavern_searches_today,
    )


@router.post("/cavern/search")
def cavern_search() -> CavernResultResponse:
    player = session.require_player()
    if player.cavern_searches_today >= 3:
        return CavernResultResponse(
            action="search", success=False,
            message="Too tired to search more today.",
            searches_remaining=0,
        )
    player.cavern_searches_today += 1
    roll = random.randint(1, 100)
    rewards = {}

    if roll <= 40:
        gold = random.randint(25, 100) * player.level
        player.gold += gold
        msg = f"You find {gold:,} gold!"
        rewards["gold"] = gold
    elif roll <= 60:
        exp = random.randint(50, 150)
        player.experience += exp
        msg = f"You gain {exp} experience from ancient writings!"
        rewards["experience"] = exp
    elif roll <= 80:
        msg = "Nothing found this time."
    else:
        bonus = random.randint(1, 5)
        player.hitpoints = min(player.max_hitpoints, player.hitpoints + bonus)
        msg = f"A healing spring restores {bonus} HP!"
        rewards["hp_restored"] = bonus

    session.save_player()
    return CavernResultResponse(
        action="search", success=roll <= 60,
        message=msg, rewards=rewards if rewards else None,
        searches_remaining=3 - player.cavern_searches_today,
    )


@router.get("/cavern/riddle")
def get_riddle() -> dict:
    global _pending_riddle
    riddle, answer = random.choice(_RIDDLES)
    _pending_riddle = {"riddle": riddle, "answer": answer}
    return {"riddle": riddle, "answer_length": len(answer)}


@router.post("/cavern/riddle")
def answer_riddle(req: RiddlerAnswerRequest) -> CavernResultResponse:
    global _pending_riddle
    player = session.require_player()
    if not _pending_riddle:
        raise HTTPException(400, "No riddle has been served. GET /cavern/riddle first.")
    # Validate against the specific riddle that was served
    correct = _pending_riddle["answer"].lower() in req.answer.lower()
    _pending_riddle = None

    rewards = {}
    if correct:
        reward_type = random.choice(["gems", "gold", "charm"])
        if reward_type == "gems":
            player.gems += 2
            msg = "Correct! The Riddler rewards you with 2 gems!"
            rewards["gems"] = 2
        elif reward_type == "gold":
            gold = 500 * player.level
            player.gold += gold
            msg = f"Correct! You receive {gold:,} gold!"
            rewards["gold"] = gold
        else:
            player.charm += 1
            msg = "Correct! Your charm increases!"
            rewards["charm"] = 1
    else:
        msg = "Wrong answer! The Riddler vanishes."

    session.save_player()
    return CavernResultResponse(
        action="riddle", success=correct,
        message=msg, rewards=rewards if rewards else None,
        searches_remaining=3 - player.cavern_searches_today,
    )


# -- Fairy Garden --

@router.post("/fairy/learn")
def fairy_learn() -> FairyResultResponse:
    player = session.require_player()
    if player.fairy_lore:
        return FairyResultResponse(action="learn", success=False, message="You already know Fairy Lore!")
    if player.gold < 1000:
        return FairyResultResponse(action="learn", success=False, message="You need 1000 gold to learn Fairy Lore.")
    player.gold -= 1000
    player.fairy_lore = True
    session.save_player()
    return FairyResultResponse(action="learn", success=True, message="You have learned Fairy Lore! You can now heal in combat.")


@router.post("/fairy/practice")
def fairy_practice() -> FairyResultResponse:
    player = session.require_player()
    heal = random.randint(5, 15)
    player.hitpoints = min(player.max_hitpoints, player.hitpoints + heal)
    session.save_player()
    return FairyResultResponse(
        action="practice", success=True,
        message=f"You practice healing arts and restore {heal} HP!",
        rewards={"hp_restored": heal},
    )


@router.post("/fairy/meditate")
def fairy_meditate() -> FairyResultResponse:
    player = session.require_player()
    roll = random.randint(1, 4)
    rewards = {}
    if roll == 1:
        player.spirit_level = "high"
        msg = "Your spirit soars! Spirit level set to HIGH."
        rewards["spirit_level"] = "high"
    elif roll == 2:
        hp_bonus = random.randint(2, 5)
        player.max_hitpoints += hp_bonus
        player.hitpoints += hp_bonus
        msg = f"Meditation strengthens you! +{hp_bonus} max HP!"
        rewards["max_hp"] = hp_bonus
    elif roll == 3:
        player.gems += 1
        msg = "A fairy gift! +1 gem."
        rewards["gems"] = 1
    else:
        msg = "Inner peace washes over you. You feel calm."
    session.save_player()
    return FairyResultResponse(action="meditate", success=True, message=msg, rewards=rewards if rewards else None)


@router.post("/fairy/gather")
def fairy_gather() -> FairyResultResponse:
    player = session.require_player()
    roll = random.randint(1, 3)
    rewards = {}
    if roll == 1:
        heal = random.randint(3, 10)
        player.hitpoints = min(player.max_hitpoints, player.hitpoints + heal)
        msg = f"Healing herbs restore {heal} HP!"
        rewards["hp_restored"] = heal
    elif roll == 2:
        gold = random.randint(50, 200)
        player.gold += gold
        msg = f"You find {gold} gold among the flowers!"
        rewards["gold"] = gold
    else:
        player.gems += 1
        msg = "A crystallized fairy tear! +1 gem."
        rewards["gems"] = 1
    session.save_player()
    return FairyResultResponse(action="gather", success=True, message=msg, rewards=rewards if rewards else None)


# -- Barak's House --

@router.post("/barak/read")
def barak_read() -> BarakResultResponse:
    return BarakResultResponse(action="read", message="You read ancient texts about combat techniques.")


@router.post("/barak/study")
def barak_study() -> BarakResultResponse:
    return BarakResultResponse(action="study", message="You study Barak's combat scrolls. Knowledge flows through you.")


@router.post("/barak/talk")
def barak_talk() -> BarakResultResponse:
    messages = [
        "Barak shares tales of ancient battles.",
        "Barak tells you about hidden treasures in the forest.",
        "Barak warns you about the dangers of the cavern.",
    ]
    return BarakResultResponse(action="talk", message=random.choice(messages))


# -- Xenon's Storage --

@router.get("/xenon")
def xenon_status() -> XenonStatusResponse:
    player = session.require_player()
    return XenonStatusResponse(
        stored_gold=player.stored_gold,
        stored_gems=player.stored_gems,
        has_horse=player.horse,
        horse_name=player.horse_name,
        children=player.children,
        gold=player.gold,
        gems=player.gems,
    )


@router.post("/xenon/transaction")
def xenon_transaction(req: XenonTransactionRequest) -> XenonResultResponse:
    player = session.require_player()

    if req.action == "store_gold":
        amount = min(req.amount or 0, player.gold)
        if amount <= 0:
            return _xenon_fail("No gold to store", player)
        player.gold -= amount
        player.stored_gold += amount
        msg = f"Stored {amount:,} gold."

    elif req.action == "retrieve_gold":
        amount = min(req.amount or 0, player.stored_gold)
        if amount <= 0:
            return _xenon_fail("No stored gold to retrieve", player)
        player.stored_gold -= amount
        player.gold += amount
        msg = f"Retrieved {amount:,} gold."

    elif req.action == "store_gems":
        amount = min(req.amount or 0, player.gems)
        if amount <= 0:
            return _xenon_fail("No gems to store", player)
        player.gems -= amount
        player.stored_gems += amount
        msg = f"Stored {amount} gem(s)."

    elif req.action == "retrieve_gems":
        amount = min(req.amount or 0, player.stored_gems)
        if amount <= 0:
            return _xenon_fail("No stored gems to retrieve", player)
        player.stored_gems -= amount
        player.gems += amount
        msg = f"Retrieved {amount} gem(s)."

    elif req.action == "buy_horse":
        if player.horse:
            return _xenon_fail("You already have a horse!", player)
        if player.gold < 500:
            return _xenon_fail("Need 500 gold for a horse.", player)
        player.gold -= 500
        player.horse = True
        player.horse_name = req.horse_name or "Horse"
        msg = f"You bought a horse named {player.horse_name}!"

    elif req.action == "trade_children":
        if player.children <= 0:
            return _xenon_fail("No children to trade.", player)
        player.children -= 1
        if req.trade_type == "gold":
            player.gold += 2000
            msg = "Traded 1 child for 2000 gold."
        elif req.trade_type == "gems":
            player.gems += 5
            msg = "Traded 1 child for 5 gems."
        else:
            msg = "Traded 1 child for mystical training."
    else:
        raise HTTPException(400, "Invalid xenon action")

    session.save_player()
    return XenonResultResponse(
        action=req.action, success=True, message=msg,
        stored_gold=player.stored_gold, stored_gems=player.stored_gems,
        gold=player.gold, gems=player.gems,
    )


def _xenon_fail(msg: str, player) -> XenonResultResponse:
    return XenonResultResponse(
        action="error", success=False, message=msg,
        stored_gold=player.stored_gold, stored_gems=player.stored_gems,
        gold=player.gold, gems=player.gems,
    )


# -- WereWolf Den --

@router.get("/werewolf")
def werewolf_status() -> WerewolfStatusResponse:
    player = session.require_player()
    return WerewolfStatusResponse(
        is_werewolf=player.is_werewolf,
        transformations=player.werewolf_transformations,
        uses_today=player.werewolf_uses_today,
        gold=player.gold,
    )


@router.post("/werewolf/accept")
def werewolf_accept() -> WerewolfResultResponse:
    player = session.require_player()
    if player.is_werewolf:
        return WerewolfResultResponse(action="accept", success=False, message="Already a werewolf!")
    if player.gold < 5000:
        return WerewolfResultResponse(action="accept", success=False, message="Need 5000 gold.")
    player.gold -= 5000
    player.is_werewolf = True
    player.max_hitpoints += 10
    player.hitpoints += 10
    session.save_player()
    return WerewolfResultResponse(
        action="accept", success=True,
        message="The curse takes hold! +10 max HP!",
        stat_changes={"max_hp": 10},
    )


@router.post("/werewolf/practice")
def werewolf_practice() -> WerewolfResultResponse:
    player = session.require_player()
    if not player.is_werewolf:
        return WerewolfResultResponse(action="practice", success=False, message="You are not a werewolf.")
    roll = random.randint(1, 3)
    changes = {}
    if roll == 1:
        player.max_hitpoints += 3
        player.hitpoints += 3
        msg = "Transformation practice! +3 max HP."
        changes["max_hp"] = 3
    elif roll == 2:
        msg = "A mishap! You take minor damage."
        player.hitpoints = max(1, player.hitpoints - 5)
        changes["damage"] = 5
    else:
        msg = "You hone your werewolf instincts."
    session.save_player()
    return WerewolfResultResponse(action="practice", success=True, message=msg, stat_changes=changes if changes else None)


@router.post("/werewolf/meditate")
def werewolf_meditate() -> WerewolfResultResponse:
    player = session.require_player()
    if not player.is_werewolf:
        return WerewolfResultResponse(action="meditate", success=False, message="You are not a werewolf.")
    roll = random.randint(1, 3)
    changes = {}
    if roll == 1:
        player.charm += 1
        msg = "Pack meditation increases your charm!"
        changes["charm"] = 1
    elif roll == 2:
        if player.werewolf_uses_today > 0:
            player.werewolf_uses_today -= 1
            msg = "Meditation restores a transformation use."
            changes["uses_restored"] = 1
        else:
            msg = "Calm meditation. You feel at peace."
    else:
        msg = "The pack shares ancient wisdom."
    session.save_player()
    return WerewolfResultResponse(action="meditate", success=True, message=msg, stat_changes=changes if changes else None)


@router.post("/werewolf/howl")
def werewolf_howl() -> WerewolfResultResponse:
    player = session.require_player()
    if not player.is_werewolf:
        return WerewolfResultResponse(action="howl", success=False, message="You are not a werewolf.")
    changes = {}
    if random.random() < 0.2:
        player.max_hitpoints += 2
        player.hitpoints += 2
        msg = "Your howl echoes through the night! +2 max HP!"
        changes["max_hp"] = 2
    else:
        msg = "Your howl echoes through the night! The moon listens."
    session.save_player()
    return WerewolfResultResponse(action="howl", success=True, message=msg, stat_changes=changes if changes else None)


# -- Gateway Portal --

@router.post("/gateway/zycho")
def gateway_zycho() -> GatewayResultResponse:
    player = session.require_player()
    if player.gems < 1:
        return GatewayResultResponse(
            action="enter", destination="zycho", message="Need 1 gem to enter.",
            gems_remaining=player.gems,
        )
    player.gems -= 1
    outcomes = ["carnival_game", "freakshow", "ringmaster", "funhouse", "blessing"]
    outcome = random.choice(outcomes)
    rewards = {}

    if outcome == "carnival_game":
        gold = random.randint(100, 500) * player.level
        player.gold += gold
        msg = f"You win the carnival game! +{gold:,} gold!"
        rewards["gold"] = gold
    elif outcome == "blessing":
        player.charm += 2
        msg = "The Zircus master blesses you! +2 charm."
        rewards["charm"] = 2
    else:
        msg = f"You experience the {outcome.replace('_', ' ')}. Entertaining!"

    session.save_player()
    return GatewayResultResponse(
        action="enter", destination="zycho", message=msg,
        rewards=rewards if rewards else None, gems_remaining=player.gems,
    )


@router.post("/gateway/death")
def gateway_death() -> GatewayResultResponse:
    player = session.require_player()
    if player.gems < 1:
        return GatewayResultResponse(
            action="enter", destination="death", message="Need 1 gem to enter.",
            gems_remaining=player.gems,
        )
    player.gems -= 1
    outcomes = ["deaths_trial", "haunted_room", "deaths_library", "meet_death"]
    outcome = random.choice(outcomes)
    rewards = {}

    if outcome == "deaths_library":
        exp = random.randint(100, 500)
        player.experience += exp
        msg = f"Death's Library grants you {exp} experience!"
        rewards["experience"] = exp
    elif outcome == "deaths_trial":
        if random.random() < 0.5:
            player.gems += 2
            msg = "You survive Death's trial! +2 gems."
            rewards["gems"] = 2
        else:
            dmg = random.randint(10, 30)
            player.hitpoints = max(1, player.hitpoints - dmg)
            msg = f"Death's trial hurts! -{dmg} HP."
            rewards["damage"] = dmg
    else:
        msg = f"You experience the {outcome.replace('_', ' ')}. Eerie."

    session.save_player()
    return GatewayResultResponse(
        action="enter", destination="death", message=msg,
        rewards=rewards if rewards else None, gems_remaining=player.gems,
    )


@router.post("/gateway/random")
def gateway_random() -> GatewayResultResponse:
    player = session.require_player()
    if player.gems < 1:
        return GatewayResultResponse(
            action="enter", destination="random", message="Need 1 gem to enter.",
            gems_remaining=player.gems,
        )
    player.gems -= 1
    outcomes = ["treasure_realm", "void_dimension", "mirror_world", "time_distortion", "elemental_plane"]
    outcome = random.choice(outcomes)
    rewards = {}

    if outcome == "treasure_realm":
        gold = random.randint(200, 1000) * player.level
        player.gold += gold
        msg = f"The Treasure Realm! +{gold:,} gold!"
        rewards["gold"] = gold
    elif outcome == "time_distortion":
        player.forest_fights = 15
        player.cavern_searches_today = 0
        player.werewolf_uses_today = 0
        player.bank_robberies_today = 0
        msg = "Time distortion! All daily limits reset!"
        rewards["daily_reset"] = True
    elif outcome == "elemental_plane":
        player.max_hitpoints += 5
        player.hitpoints = min(player.max_hitpoints, player.hitpoints + 5)
        msg = "Elemental energy! +5 max HP!"
        rewards["max_hp"] = 5
    else:
        msg = f"You drift through the {outcome.replace('_', ' ')}. Strange."

    session.save_player()
    return GatewayResultResponse(
        action="enter", destination=outcome, message=msg,
        rewards=rewards if rewards else None, gems_remaining=player.gems,
    )

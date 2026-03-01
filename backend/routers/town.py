from __future__ import annotations

from fastapi import APIRouter, HTTPException

from backend.models.requests import (
    BankTransactionRequest, HealRequest, BuyItemRequest,
    GemTradeRequest, VioletFlirtRequest, BribeRequest, NameChangeRequest,
)
from backend.models.responses import (
    ShopListResponse, ShopItemResponse, BuyResultResponse,
    HealerResponse, HealerResultResponse,
    BankResponse, BankTransactionResponse, RobberyResultResponse,
    TrainingStatusResponse, MasterResponse,
    WarriorListResponse, WarriorResponse,
    MessageResponse,
    InnStatusResponse, RoomRentalResponse, GemTradeResponse,
    VioletStatusResponse, VioletResultResponse,
    BribeStatusResponse, BribeResultResponse,
    NameChangeResponse,
)
from backend.services.game_service import session
from backend.services.shop_service import shop_service

import sys
from pathlib import Path
_project_root = str(Path(__file__).resolve().parent.parent.parent)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from game_data import (
    MASTERS, LEVEL_EXP, can_level_up,
    INN_ROOM_COSTS, BRIBE_COSTS, RESERVED_NAMES,
    VIOLET_FLIRT_OPTIONS,
)

router = APIRouter(prefix="/api/town", tags=["town"])


# -- Bank --

@router.get("/bank")
def get_bank() -> BankResponse:
    player = session.require_player()
    can_rob = (
        player.class_type == "D"
        and player.fairy_lore
        and player.bank_robberies_today == 0
    )
    return BankResponse(gold=player.gold, bank_gold=player.bank_gold, can_rob=can_rob)


@router.post("/bank/deposit")
def bank_deposit(req: BankTransactionRequest) -> BankTransactionResponse:
    player = session.require_player()
    result = shop_service.bank_deposit(player, req.amount)
    session.save_player()
    return BankTransactionResponse(**result)


@router.post("/bank/withdraw")
def bank_withdraw(req: BankTransactionRequest) -> BankTransactionResponse:
    player = session.require_player()
    result = shop_service.bank_withdraw(player, req.amount)
    session.save_player()
    return BankTransactionResponse(**result)


@router.post("/bank/rob")
def bank_rob() -> RobberyResultResponse:
    player = session.require_player()
    result = shop_service.bank_rob(player)
    session.save_player()
    return RobberyResultResponse(**result)


# -- Healer --

@router.get("/healer")
def get_healer() -> HealerResponse:
    player = session.require_player()
    info = shop_service.get_healer_info(player)
    return HealerResponse(**info)


@router.post("/healer/heal")
def healer_heal(req: HealRequest) -> HealerResultResponse:
    player = session.require_player()
    if req.heal_type == "full":
        result = shop_service.heal_full(player)
    elif req.heal_type == "partial":
        if req.amount is None or req.amount <= 0:
            raise HTTPException(400, "Amount required for partial heal")
        result = shop_service.heal_partial(player, req.amount)
    else:
        raise HTTPException(400, "heal_type must be 'full' or 'partial'")
    session.save_player()
    return HealerResultResponse(**result)


# -- Weapons --

@router.get("/weapons")
def list_weapons() -> ShopListResponse:
    player = session.require_player()
    items = shop_service.list_weapons(player)
    return ShopListResponse(
        items=[ShopItemResponse(**i) for i in items],
        current_gold=player.gold,
        current_item_index=player.weapon_num,
    )


@router.post("/weapons/buy")
def buy_weapon(req: BuyItemRequest) -> BuyResultResponse:
    player = session.require_player()
    result = shop_service.buy_weapon(player, req.item_index)
    session.save_player()
    return BuyResultResponse(**result)


# -- Armor --

@router.get("/armor")
def list_armor() -> ShopListResponse:
    player = session.require_player()
    items = shop_service.list_armor(player)
    return ShopListResponse(
        items=[ShopItemResponse(**i) for i in items],
        current_gold=player.gold,
        current_item_index=player.armor_num,
    )


@router.post("/armor/buy")
def buy_armor(req: BuyItemRequest) -> BuyResultResponse:
    player = session.require_player()
    result = shop_service.buy_armor(player, req.item_index)
    session.save_player()
    return BuyResultResponse(**result)


# -- Training --

@router.get("/training")
def get_training() -> TrainingStatusResponse:
    player = session.require_player()
    masters_list = []
    for lvl in range(1, 12):
        m = MASTERS.get(lvl)
        if not m:
            continue
        exp_needed = LEVEL_EXP.get(lvl + 1, 0)
        masters_list.append(MasterResponse(
            level=lvl,
            name=m["name"],
            greeting=m.get("greeting", ""),
            can_challenge=player.level == lvl and player.experience >= exp_needed,
            exp_needed=exp_needed,
            current_exp=player.experience,
        ))
    return TrainingStatusResponse(
        current_level=player.level,
        masters=masters_list,
        can_challenge_current=can_level_up(player),
    )


# -- Warriors List --

@router.get("/warriors")
def list_warriors() -> WarriorListResponse:
    players = session.list_players()
    return WarriorListResponse(
        warriors=[
            WarriorResponse(
                name=p.name,
                level=p.level,
                experience=p.experience,
                class_type=p.class_type,
                weapon=p.weapon,
                armor=p.armor,
                alive=p.alive,
                total_kills=p.total_kills,
                dragon_kills=p.dragon_kills,
            )
            for p in players[:20]
        ]
    )


# -- Daily News --

@router.get("/daily-news")
def get_daily_news() -> MessageResponse:
    from game_data import get_daily_happening
    return MessageResponse(message=get_daily_happening())


# -- Inn --

@router.get("/inn")
def get_inn_status() -> InnStatusResponse:
    player = session.require_player()
    level_idx = min(player.level - 1, 11)
    return InnStatusResponse(
        level=player.level,
        gold=player.gold,
        gems=player.gems,
        charm=player.charm,
        inn_room=player.inn_room,
        room_cost=INN_ROOM_COSTS[level_idx],
        bribe_cost=BRIBE_COSTS[level_idx],
        can_access_bar=player.level > 1,
        married_to=player.married_to,
        flirted_violet=player.flirted_violet,
    )


@router.post("/inn/rent-room")
def rent_room() -> RoomRentalResponse:
    player = session.require_player()
    if player.inn_room:
        return RoomRentalResponse(success=False, message="You already have a room for tonight!", gold=player.gold)
    level_idx = min(player.level - 1, 11)
    cost = INN_ROOM_COSTS[level_idx]
    if player.charm > 100:
        player.inn_room = True
        session.save_player()
        return RoomRentalResponse(success=True, message="'No charge for such a charming warrior!'", gold=player.gold)
    if player.gold < cost:
        return RoomRentalResponse(success=False, message=f"You need {cost} gold pieces for a room.", gold=player.gold)
    player.gold -= cost
    player.inn_room = True
    session.save_player()
    return RoomRentalResponse(success=True, message=f"'That'll be {cost} gold pieces.' You have a room for tonight.", gold=player.gold)


@router.post("/inn/gem-trade")
def gem_trade(req: GemTradeRequest) -> GemTradeResponse:
    player = session.require_player()
    if player.gems < 2:
        raise HTTPException(400, "You need at least 2 gems!")
    if req.stat not in ("defense", "strength", "hitpoints"):
        raise HTTPException(400, "stat must be 'defense', 'strength', or 'hitpoints'")
    player.gems -= 2
    if req.stat == "defense":
        player.defense += 1
        val = player.defense
        stat_name = "Defense"
    elif req.stat == "strength":
        player.strength += 1
        val = player.strength
        stat_name = "Strength"
    else:
        player.max_hitpoints += 1
        player.hitpoints += 1
        val = player.max_hitpoints
        stat_name = "Hit Points"
    session.save_player()
    return GemTradeResponse(success=True, message=f"Your {stat_name} increases by 1!", gems=player.gems, stat_changed=req.stat, stat_value=val)


# -- Violet --

@router.get("/inn/violet")
def violet_status() -> VioletStatusResponse:
    player = session.require_player()
    violet_married = session.db.is_violet_married() if hasattr(session.db, 'is_violet_married') else False
    violet_husband = None
    if violet_married and hasattr(session.db, 'get_violet_husband'):
        violet_husband = session.db.get_violet_husband()
    options = []
    if not violet_married:
        for charm_req, option_data in sorted(VIOLET_FLIRT_OPTIONS.items()):
            if player.charm >= charm_req:
                if charm_req == 100 and player.married_to:
                    continue
                options.append({
                    "charm_level": charm_req,
                    "action": option_data["action"],
                    "special": option_data.get("special"),
                })
    return VioletStatusResponse(
        charm=player.charm,
        married_to=player.married_to,
        violet_married=violet_married,
        violet_husband=violet_husband,
        flirted_today=player.flirted_violet,
        options=options,
    )


@router.post("/inn/violet/flirt")
def violet_flirt(req: VioletFlirtRequest) -> VioletResultResponse:
    player = session.require_player()
    violet_married = session.db.is_violet_married() if hasattr(session.db, 'is_violet_married') else False
    if violet_married:
        raise HTTPException(400, "Violet has married someone and moved away!")
    option_data = VIOLET_FLIRT_OPTIONS.get(req.charm_level)
    if not option_data:
        raise HTTPException(400, "Invalid charm level option")
    if player.charm < req.charm_level:
        raise HTTPException(400, "Not enough charm for this action")
    special = option_data.get("special")
    exp_gain = player.level * option_data["exp_multiplier"]
    message = option_data["message"]
    if special == "marry":
        if player.married_to:
            raise HTTPException(400, "You are already married!")
        player.married_to = "Violet"
        player.experience += exp_gain
        if hasattr(session.db, 'marry_violet'):
            session.db.marry_violet(player.name)
    elif special == "laid":
        player.laid_today = True
        player.flirted_violet = True
        player.experience += exp_gain
        player.hitpoints = min(player.max_hitpoints, player.hitpoints + 1)
    else:
        player.flirted_violet = True
        player.experience += exp_gain
    session.save_player()
    return VioletResultResponse(
        success=True, message=message, exp_gained=exp_gain,
        special=special, charm=player.charm, married_to=player.married_to,
    )


# -- Bribe --

@router.get("/inn/bribe")
def bribe_status() -> BribeStatusResponse:
    player = session.require_player()
    level_idx = min(player.level - 1, 11)
    cost = BRIBE_COSTS[level_idx]
    sleeping = session.db.get_players_at_inn() if hasattr(session.db, 'get_players_at_inn') else []
    targets = [
        {"name": t.name, "level": t.level, "gold": t.gold}
        for t in sleeping
        if t.name != player.name and t.level >= player.level - 1
    ]
    return BribeStatusResponse(cost=cost, gold=player.gold, targets=targets)


@router.post("/inn/bribe")
def bribe_kill(req: BribeRequest) -> BribeResultResponse:
    player = session.require_player()
    level_idx = min(player.level - 1, 11)
    cost = BRIBE_COSTS[level_idx]
    if player.gold < cost:
        raise HTTPException(400, f"You need {cost} gold to bribe the bartender!")
    sleeping = session.db.get_players_at_inn() if hasattr(session.db, 'get_players_at_inn') else []
    target = None
    for t in sleeping:
        if t.name == req.target_name:
            target = t
            break
    if not target:
        raise HTTPException(404, "Target not found at the inn")
    player.gold -= cost
    exp_gain = target.level * 50
    gold_gain = target.gold // 2
    player.experience += exp_gain
    player.gold += gold_gain
    player.total_kills += 1
    target.inn_room = False
    target.alive = False
    session.db.save_player(target)
    session.save_player()
    return BribeResultResponse(
        success=True,
        message=f"The bartender slips a knife between {target.name}'s ribs... {target.name} has been eliminated!",
        exp_gained=exp_gain, gold_gained=gold_gain, gold=player.gold,
    )


# -- Name Change --

@router.post("/inn/name-change")
def change_name(req: NameChangeRequest) -> NameChangeResponse:
    player = session.require_player()
    new_name = req.new_name.strip()
    if not new_name:
        raise HTTPException(400, "Name cannot be empty!")
    if new_name.upper() in RESERVED_NAMES:
        raise HTTPException(400, RESERVED_NAMES[new_name.upper()])
    existing = session.db.load_player(new_name)
    if existing:
        raise HTTPException(400, "That name is already taken!")
    player.name = new_name
    session.save_player()
    return NameChangeResponse(success=True, message=f"Your name has been changed to {new_name}!", new_name=new_name)

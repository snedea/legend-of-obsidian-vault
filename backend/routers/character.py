from __future__ import annotations

from fastapi import APIRouter, HTTPException

from backend.models.requests import CreateCharacterRequest
from backend.models.responses import CharacterResponse, CharacterListResponse
from backend.services.game_service import session

router = APIRouter(prefix="/api/character", tags=["character"])


def _player_to_response(player) -> CharacterResponse:
    return CharacterResponse(
        name=player.name,
        gender=player.gender,
        class_type=player.class_type,
        level=player.level,
        experience=player.experience,
        hitpoints=player.hitpoints,
        max_hitpoints=player.max_hitpoints,
        forest_fights=player.forest_fights,
        player_fights=player.player_fights,
        gold=player.gold,
        bank_gold=player.bank_gold,
        weapon=player.weapon,
        weapon_num=player.weapon_num,
        armor=player.armor,
        armor_num=player.armor_num,
        strength=player.strength,
        defense=player.defense,
        charm=player.charm,
        gems=player.gems,
        horse=player.horse,
        fairy_blessing=player.fairy_blessing,
        fairy_lore=player.fairy_lore,
        alive=player.alive,
        days_played=player.days_played,
        skill_uses=player.skill_uses,
        attack_power=player.attack_power,
        defense_power=player.defense_power,
        death_knight_points=player.death_knight_points,
        mystical_points=player.mystical_points,
        thieving_points=player.thieving_points,
        skills_used_today=player.skills_used_today,
        is_werewolf=player.is_werewolf,
        werewolf_transformations=player.werewolf_transformations,
        dragon_kills=player.dragon_kills,
        total_kills=player.total_kills,
        times_won_game=player.times_won_game,
        stored_gold=player.stored_gold,
        stored_gems=player.stored_gems,
        spirit_level=player.spirit_level,
        children=player.children,
        horse_name=player.horse_name,
        bank_robberies_today=player.bank_robberies_today,
        successful_robberies=player.successful_robberies,
        cavern_searches_today=player.cavern_searches_today,
        married=player.married,
        married_to=player.married_to,
        inn_room=player.inn_room,
        flirted_violet=player.flirted_violet,
        laid_today=player.laid_today,
    )


@router.post("/create")
def create_character(req: CreateCharacterRequest) -> CharacterResponse:
    if not req.name.strip():
        raise HTTPException(400, "Name cannot be empty")
    if req.gender not in ("M", "F"):
        raise HTTPException(400, "Gender must be M or F")
    if req.class_type not in ("K", "P", "D"):
        raise HTTPException(400, "Class must be K, P, or D")

    # Check if name already exists
    existing = session.db.load_player(req.name.strip())
    if existing:
        raise HTTPException(409, "Character name already exists")

    player = session.create_player(req.name.strip(), req.gender, req.class_type)
    return _player_to_response(player)


@router.get("/list")
def list_characters() -> CharacterListResponse:
    players = session.list_players()
    return CharacterListResponse(
        characters=[_player_to_response(p) for p in players]
    )


@router.post("/select/{name}")
def select_character(name: str) -> CharacterResponse:
    player = session.select_player(name)
    if not player:
        raise HTTPException(404, "Character not found")
    return _player_to_response(player)


@router.get("/current")
def get_current_character() -> CharacterResponse:
    player = session.player
    if not player:
        raise HTTPException(404, "No character selected")
    return _player_to_response(player)

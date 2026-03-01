from __future__ import annotations

from fastapi import APIRouter, HTTPException

from backend.models.requests import QuizAnswerRequest
from backend.models.responses import (
    CombatStateResponse, AttackResultResponse, HealResultResponse,
    FleeResultResponse, QuizQuestionResponse, QuizResultResponse,
    EnemyResponse, RewardsResponse,
)
from backend.routers.character import _player_to_response
from backend.services.game_service import session
from backend.services.combat_service import combat_service, CombatState

router = APIRouter(prefix="/api/combat", tags=["combat"])

# In-memory combat state (single-player, one fight at a time)
_current_combat: CombatState | None = None


def _require_combat() -> CombatState:
    if _current_combat is None:
        raise HTTPException(400, "No active combat")
    if not _current_combat.combat_active:
        raise HTTPException(400, "Combat has ended")
    return _current_combat


def _enemy_response(enemy) -> EnemyResponse:
    return EnemyResponse(
        name=enemy.name,
        hitpoints=enemy.hitpoints,
        max_hitpoints=getattr(enemy, "max_hitpoints", enemy.hitpoints),
        attack=enemy.attack,
        gold_reward=enemy.gold_reward,
        exp_reward=enemy.exp_reward,
        level=enemy.level,
        note_title=getattr(enemy, "note_title", ""),
        note_content=getattr(enemy, "note_content", "")[:200],
        backstory=getattr(enemy, "backstory", ""),
        knowledge_domain=getattr(enemy, "knowledge_domain", ""),
        description=getattr(enemy, "description", ""),
        weapon=getattr(enemy, "weapon", "Unknown"),
        armor=getattr(enemy, "armor", "Unknown"),
        encounter_narrative=getattr(enemy, "encounter_narrative", ""),
        combat_phrases=getattr(enemy, "combat_phrases", []),
        defeat_message=getattr(enemy, "defeat_message", ""),
        victory_message=getattr(enemy, "victory_message", ""),
    )


def _combat_state_response(state: CombatState) -> CombatStateResponse:
    player = session.require_player()
    return CombatStateResponse(
        enemy=_enemy_response(state.enemy),
        player=_player_to_response(player),
        combat_active=state.combat_active,
        player_turn=state.player_turn,
        quiz_available=state.quiz_available,
        is_master_fight=state.is_master_fight,
        log=state.log,
    )


def _rewards_response(rewards: dict | None) -> RewardsResponse | None:
    if not rewards:
        return None
    return RewardsResponse(
        gold=rewards["gold"],
        experience=rewards["experience"],
        level_up=rewards.get("level_up", False),
        level_up_gains=rewards.get("level_up_gains"),
        can_train=rewards.get("can_train", False),
    )


@router.post("/enter-forest")
def enter_forest() -> CombatStateResponse:
    global _current_combat
    player = session.require_player()
    if player.forest_fights <= 0:
        raise HTTPException(400, "No forest fights remaining")
    _current_combat = combat_service.enter_forest(player)
    return _combat_state_response(_current_combat)


@router.post("/master-fight/{level}")
def start_master_fight(level: int) -> CombatStateResponse:
    global _current_combat
    player = session.require_player()
    if not player.can_challenge_master():
        raise HTTPException(400, "Cannot challenge master")
    _current_combat = combat_service.start_master_fight(player, level)
    return _combat_state_response(_current_combat)


@router.post("/attack")
def attack() -> AttackResultResponse:
    state = _require_combat()
    player = session.require_player()
    result = combat_service.player_attack(player, state)
    session.save_player()
    return AttackResultResponse(
        player_damage=result["player_damage"],
        player_hit=result["player_hit"],
        player_message=result["player_message"],
        enemy_damage=result["enemy_damage"],
        enemy_hit=result["enemy_hit"],
        enemy_message=result["enemy_message"],
        enemy_hp=result["enemy_hp"],
        player_hp=result["player_hp"],
        combat_over=result["combat_over"],
        victory=result["victory"],
        rewards=_rewards_response(result.get("rewards")),
        log=result["log"],
    )


@router.post("/skill")
def skill_attack() -> AttackResultResponse:
    state = _require_combat()
    player = session.require_player()
    result = combat_service.skill_attack(player, state)
    session.save_player()
    return AttackResultResponse(
        player_damage=result["player_damage"],
        player_hit=result["player_hit"],
        player_message=result["player_message"],
        enemy_damage=result["enemy_damage"],
        enemy_hit=result["enemy_hit"],
        enemy_message=result["enemy_message"],
        enemy_hp=result["enemy_hp"],
        player_hp=result["player_hp"],
        combat_over=result["combat_over"],
        victory=result["victory"],
        rewards=_rewards_response(result.get("rewards")),
        log=result["log"],
    )


@router.post("/heal")
def heal() -> HealResultResponse:
    state = _require_combat()
    player = session.require_player()
    result = combat_service.fairy_heal(player, state)
    if "success" in result and not result["success"]:
        raise HTTPException(400, result["message"])
    session.save_player()
    return HealResultResponse(**result)


@router.post("/run")
def run_away() -> FleeResultResponse:
    state = _require_combat()
    result = combat_service.flee(state)
    return FleeResultResponse(**result)


@router.post("/quiz/start")
def quiz_start() -> QuizQuestionResponse:
    state = _require_combat()
    result = combat_service.quiz_start(state)
    if "error" in result:
        raise HTTPException(400, result["error"])
    return QuizQuestionResponse(**result)


@router.post("/quiz/answer")
def quiz_answer(req: QuizAnswerRequest) -> QuizResultResponse:
    state = _require_combat()
    player = session.require_player()
    result = combat_service.quiz_answer(player, state, req.selected_index)
    if "error" in result:
        raise HTTPException(400, result["error"])
    session.save_player()
    return QuizResultResponse(
        correct=result["correct"],
        damage=result["damage"],
        message=result["message"],
        enemy_damage=result["enemy_damage"],
        enemy_hit=result["enemy_hit"],
        enemy_message=result["enemy_message"],
        enemy_hp=result["enemy_hp"],
        player_hp=result["player_hp"],
        combat_over=result["combat_over"],
        victory=result["victory"],
        rewards=_rewards_response(result.get("rewards")),
    )


@router.get("/state")
def get_combat_state() -> CombatStateResponse:
    state = _require_combat()
    return _combat_state_response(state)

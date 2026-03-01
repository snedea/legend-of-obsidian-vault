from __future__ import annotations

from typing import Optional
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str = "ok"
    version: str = "0.0.5"


class CharacterResponse(BaseModel):
    name: str
    gender: str
    class_type: str
    level: int
    experience: int
    hitpoints: int
    max_hitpoints: int
    forest_fights: int
    player_fights: int
    gold: int
    bank_gold: int
    weapon: str
    weapon_num: int
    armor: str
    armor_num: int
    strength: int
    defense: int
    charm: int
    gems: int
    horse: bool
    fairy_blessing: bool
    fairy_lore: bool
    alive: bool
    days_played: int
    skill_uses: int
    attack_power: int
    defense_power: int
    # Skill points
    death_knight_points: int
    mystical_points: int
    thieving_points: int
    skills_used_today: int
    # Werewolf
    is_werewolf: bool
    werewolf_transformations: int
    # Hall of Honours
    dragon_kills: int
    total_kills: int
    times_won_game: int
    # Storage
    stored_gold: int
    stored_gems: int
    # Misc
    spirit_level: str
    children: int
    horse_name: str
    bank_robberies_today: int
    successful_robberies: int
    cavern_searches_today: int
    married: bool
    married_to: str
    inn_room: bool
    flirted_violet: bool
    laid_today: bool


class CharacterListResponse(BaseModel):
    characters: list[CharacterResponse]


class EnemyResponse(BaseModel):
    name: str
    hitpoints: int
    max_hitpoints: int
    attack: int
    gold_reward: int
    exp_reward: int
    level: int
    note_title: str
    note_content: str
    # Lore
    backstory: str
    knowledge_domain: str
    description: str
    weapon: str
    armor: str
    encounter_narrative: str
    # Combat phrases
    combat_phrases: list[str]
    defeat_message: str
    victory_message: str


class CombatStateResponse(BaseModel):
    enemy: EnemyResponse
    player: CharacterResponse
    combat_active: bool
    player_turn: bool
    quiz_available: bool
    is_master_fight: bool
    log: list[str]


class AttackResultResponse(BaseModel):
    player_damage: int
    player_hit: bool
    player_message: str
    enemy_damage: int
    enemy_hit: bool
    enemy_message: str
    enemy_hp: int
    player_hp: int
    combat_over: bool
    victory: bool
    rewards: Optional[RewardsResponse] = None
    log: list[str]


class RewardsResponse(BaseModel):
    gold: int
    experience: int
    level_up: bool
    level_up_gains: Optional[dict] = None
    can_train: bool


class QuizQuestionResponse(BaseModel):
    question: str
    options: list[str]
    correct_index: int
    difficulty: int
    question_type: str


class QuizResultResponse(BaseModel):
    correct: bool
    damage: int
    message: str
    enemy_damage: int
    enemy_hit: bool
    enemy_message: str
    enemy_hp: int
    player_hp: int
    combat_over: bool
    victory: bool
    rewards: Optional[RewardsResponse] = None


class HealResultResponse(BaseModel):
    heal_amount: int
    player_hp: int
    player_max_hp: int
    message: str
    enemy_damage: int
    enemy_hit: bool
    enemy_message: str
    enemy_hp: int
    combat_over: bool
    victory: bool


class FleeResultResponse(BaseModel):
    success: bool
    message: str


class ShopItemResponse(BaseModel):
    index: int
    name: str
    price: int
    stat_value: int
    owned: bool
    can_buy: bool


class ShopListResponse(BaseModel):
    items: list[ShopItemResponse]
    current_gold: int
    current_item_index: int


class BuyResultResponse(BaseModel):
    success: bool
    message: str
    gold_remaining: int
    item_name: str


class HealerResponse(BaseModel):
    full_heal_cost: int
    per_hp_cost: int
    hp_missing: int
    current_hp: int
    max_hp: int
    current_gold: int


class HealerResultResponse(BaseModel):
    success: bool
    message: str
    hp_healed: int
    gold_spent: int
    current_hp: int
    current_gold: int


class BankResponse(BaseModel):
    gold: int
    bank_gold: int
    can_rob: bool


class BankTransactionResponse(BaseModel):
    success: bool
    message: str
    gold: int
    bank_gold: int


class RobberyResultResponse(BaseModel):
    success: bool
    message: str
    gold_change: int
    gold: int
    bank_gold: int


class MasterResponse(BaseModel):
    level: int
    name: str
    greeting: str
    can_challenge: bool
    exp_needed: int
    current_exp: int


class TrainingStatusResponse(BaseModel):
    current_level: int
    masters: list[MasterResponse]
    can_challenge_current: bool


class WarriorResponse(BaseModel):
    name: str
    level: int
    experience: int
    class_type: str
    weapon: str
    armor: str
    alive: bool
    total_kills: int
    dragon_kills: int


class WarriorListResponse(BaseModel):
    warriors: list[WarriorResponse]


class VaultStatusResponse(BaseModel):
    connected: bool
    path: Optional[str]
    note_count: int
    auto_detected: bool


class NoteResponse(BaseModel):
    title: str
    difficulty: int
    tags: list[str]
    age_days: int


class NoteListResponse(BaseModel):
    notes: list[NoteResponse]
    total: int


class SettingsResponse(BaseModel):
    difficulty_mode: str
    ai_narratives_enabled: bool
    quiz_attacks_enabled: bool
    ai_provider: str
    claude_model: str
    has_api_key: bool


class AIStatusResponse(BaseModel):
    provider: str
    available: bool
    status: str


class MessageResponse(BaseModel):
    message: str


# IGM responses

class CavernResultResponse(BaseModel):
    action: str
    success: bool
    message: str
    rewards: Optional[dict] = None
    searches_remaining: int


class FairyResultResponse(BaseModel):
    action: str
    success: bool
    message: str
    rewards: Optional[dict] = None


class BarakResultResponse(BaseModel):
    action: str
    message: str


class XenonStatusResponse(BaseModel):
    stored_gold: int
    stored_gems: int
    has_horse: bool
    horse_name: str
    children: int
    gold: int
    gems: int


class XenonResultResponse(BaseModel):
    action: str
    success: bool
    message: str
    stored_gold: int
    stored_gems: int
    gold: int
    gems: int


class WerewolfStatusResponse(BaseModel):
    is_werewolf: bool
    transformations: int
    uses_today: int
    gold: int


class WerewolfResultResponse(BaseModel):
    action: str
    success: bool
    message: str
    stat_changes: Optional[dict] = None


class GatewayResultResponse(BaseModel):
    action: str
    destination: str
    message: str
    rewards: Optional[dict] = None
    gems_remaining: int


# Inn sub-screen responses

class InnStatusResponse(BaseModel):
    level: int
    gold: int
    gems: int
    charm: int
    inn_room: bool
    room_cost: int
    bribe_cost: int
    can_access_bar: bool  # Level > 1
    married_to: str
    flirted_violet: bool


class RoomRentalResponse(BaseModel):
    success: bool
    message: str
    gold: int


class GemTradeResponse(BaseModel):
    success: bool
    message: str
    gems: int
    stat_changed: str
    stat_value: int


class VioletStatusResponse(BaseModel):
    charm: int
    married_to: str
    violet_married: bool
    violet_husband: Optional[str] = None
    flirted_today: bool
    options: list[dict]


class VioletResultResponse(BaseModel):
    success: bool
    message: str
    exp_gained: int
    special: Optional[str] = None
    charm: int
    married_to: str


class BribeStatusResponse(BaseModel):
    cost: int
    gold: int
    targets: list[dict]


class BribeResultResponse(BaseModel):
    success: bool
    message: str
    exp_gained: int
    gold_gained: int
    gold: int


class NameChangeResponse(BaseModel):
    success: bool
    message: str
    new_name: str

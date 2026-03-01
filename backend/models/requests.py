from __future__ import annotations

from typing import Optional
from pydantic import BaseModel


class CreateCharacterRequest(BaseModel):
    name: str
    gender: str  # "M" or "F"
    class_type: str  # "K", "P", or "D"


class QuizAnswerRequest(BaseModel):
    selected_index: int


class BankTransactionRequest(BaseModel):
    amount: int


class HealRequest(BaseModel):
    heal_type: str  # "full" or "partial"
    amount: Optional[int] = None  # only for partial


class BuyItemRequest(BaseModel):
    item_index: int


class SetVaultPathRequest(BaseModel):
    path: str


class UpdateSettingsRequest(BaseModel):
    difficulty_mode: Optional[str] = None
    ai_narratives_enabled: Optional[bool] = None
    quiz_attacks_enabled: Optional[bool] = None
    ai_provider: Optional[str] = None
    claude_model: Optional[str] = None
    claude_api_key: Optional[str] = None


class XenonTransactionRequest(BaseModel):
    action: str  # "store_gold", "retrieve_gold", "store_gems", "retrieve_gems", "buy_horse", "trade_children"
    amount: Optional[int] = None
    horse_name: Optional[str] = None
    trade_type: Optional[str] = None  # "gold", "gems", "stat"


class RiddlerAnswerRequest(BaseModel):
    answer: str


class GemTradeRequest(BaseModel):
    stat: str  # "defense", "strength", or "hitpoints"


class VioletFlirtRequest(BaseModel):
    charm_level: int  # The charm threshold of the chosen option


class BribeRequest(BaseModel):
    target_name: str


class NameChangeRequest(BaseModel):
    new_name: str

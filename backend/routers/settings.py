from __future__ import annotations

import sys
from pathlib import Path

from fastapi import APIRouter

_project_root = str(Path(__file__).resolve().parent.parent.parent)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from backend.models.requests import UpdateSettingsRequest
from backend.models.responses import SettingsResponse, AIStatusResponse
from game_data import game_settings, DifficultyMode, AIProviderType
from brainbot import ai_provider_manager, get_current_provider_name, is_ai_available

router = APIRouter(prefix="/api/settings", tags=["settings"])


@router.get("")
def get_settings() -> SettingsResponse:
    return SettingsResponse(
        difficulty_mode=game_settings.difficulty_mode.value,
        ai_narratives_enabled=game_settings.ai_narratives_enabled,
        quiz_attacks_enabled=game_settings.quiz_attacks_enabled,
        ai_provider=game_settings.ai_provider.value,
        claude_model=game_settings.claude_model,
        has_api_key=bool(game_settings.claude_api_key),
    )


@router.post("")
def update_settings(req: UpdateSettingsRequest) -> SettingsResponse:
    if req.difficulty_mode is not None:
        game_settings.difficulty_mode = DifficultyMode(req.difficulty_mode)
    if req.ai_narratives_enabled is not None:
        game_settings.ai_narratives_enabled = req.ai_narratives_enabled
    if req.quiz_attacks_enabled is not None:
        game_settings.quiz_attacks_enabled = req.quiz_attacks_enabled
    if req.ai_provider is not None:
        game_settings.ai_provider = AIProviderType(req.ai_provider)
    if req.claude_model is not None:
        game_settings.claude_model = req.claude_model
    if req.claude_api_key is not None:
        game_settings.claude_api_key = req.claude_api_key
    game_settings.save()
    return get_settings()


@router.get("/ai")
def ai_status() -> AIStatusResponse:
    return AIStatusResponse(
        provider=get_current_provider_name(),
        available=is_ai_available(wait_timeout=0.5),
        status=ai_provider_manager.initialization_status,
    )

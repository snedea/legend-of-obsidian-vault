from __future__ import annotations

import sys
from pathlib import Path

from fastapi import APIRouter, HTTPException

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
        ollama_host=game_settings.ollama_host,
        ollama_model=game_settings.ollama_model,
    )


@router.post("")
def update_settings(req: UpdateSettingsRequest) -> SettingsResponse:
    needs_reinit = False

    if req.difficulty_mode is not None:
        game_settings.difficulty_mode = DifficultyMode(req.difficulty_mode)
    if req.ai_narratives_enabled is not None:
        game_settings.ai_narratives_enabled = req.ai_narratives_enabled
    if req.quiz_attacks_enabled is not None:
        game_settings.quiz_attacks_enabled = req.quiz_attacks_enabled
    if req.ai_provider is not None:
        try:
            game_settings.ai_provider = AIProviderType(req.ai_provider)
        except ValueError:
            valid = [p.value for p in AIProviderType]
            raise HTTPException(status_code=422, detail=f"Invalid ai_provider. Valid: {valid}")
        needs_reinit = True
    if req.claude_model is not None:
        game_settings.claude_model = req.claude_model
        needs_reinit = True
    if req.claude_api_key is not None:
        game_settings.claude_api_key = req.claude_api_key
        needs_reinit = True
    if req.ollama_host is not None:
        game_settings.ollama_host = req.ollama_host
        needs_reinit = True
    if req.ollama_model is not None:
        game_settings.ollama_model = req.ollama_model
        needs_reinit = True
    game_settings.save()

    if needs_reinit:
        ai_provider_manager.reinitialize_provider()

    return get_settings()


@router.get("/ai")
def ai_status() -> AIStatusResponse:
    return AIStatusResponse(
        provider=get_current_provider_name(),
        available=is_ai_available(wait_timeout=0.5),
        status=ai_provider_manager.initialization_status,
    )

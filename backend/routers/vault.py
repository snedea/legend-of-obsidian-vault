from __future__ import annotations

import sys
from pathlib import Path

from fastapi import APIRouter, HTTPException

_project_root = str(Path(__file__).resolve().parent.parent.parent)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from backend.models.requests import SetVaultPathRequest
from backend.models.responses import VaultStatusResponse, NoteListResponse, NoteResponse
from obsidian import vault

router = APIRouter(prefix="/api/vault", tags=["vault"])


@router.get("/status")
def vault_status() -> VaultStatusResponse:
    connected = vault.vault_path is not None and vault.vault_path.exists()
    note_count = 0
    if connected:
        notes = vault.scan_notes()
        note_count = len(notes)
    return VaultStatusResponse(
        connected=connected,
        path=str(vault.vault_path) if vault.vault_path else None,
        note_count=note_count,
        auto_detected=False,
    )


@router.post("/auto-detect")
def auto_detect() -> VaultStatusResponse:
    found = vault.find_vault()
    if found:
        vault.vault_path = found
        notes = vault.scan_notes(force_rescan=True)
        return VaultStatusResponse(
            connected=True,
            path=str(found),
            note_count=len(notes),
            auto_detected=True,
        )
    return VaultStatusResponse(connected=False, path=None, note_count=0, auto_detected=False)


@router.post("/set-path")
def set_vault_path(req: SetVaultPathRequest) -> VaultStatusResponse:
    p = Path(req.path)
    if not p.exists() or not p.is_dir():
        raise HTTPException(400, "Path does not exist or is not a directory")
    vault.vault_path = p
    notes = vault.scan_notes(force_rescan=True)
    return VaultStatusResponse(
        connected=True,
        path=str(p),
        note_count=len(notes),
        auto_detected=False,
    )


@router.get("/notes")
def list_notes(limit: int = 50, offset: int = 0) -> NoteListResponse:
    notes = vault.scan_notes()
    total = len(notes)
    subset = notes[offset:offset + limit]
    return NoteListResponse(
        notes=[
            NoteResponse(
                title=n.title,
                difficulty=n.difficulty_level,
                tags=n.tags,
                age_days=n.age_days,
            )
            for n in subset
        ],
        total=total,
    )

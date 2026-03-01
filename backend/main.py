from __future__ import annotations

import sys
import threading
from pathlib import Path

# Add project root to sys.path so game_data, obsidian, brainbot are importable
_project_root = str(Path(__file__).resolve().parent.parent)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.models.responses import HealthResponse
from backend.routers import character, combat, town, igm, vault, settings

app = FastAPI(title="Legend of the Obsidian Vault", version="0.0.5")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(character.router)
app.include_router(combat.router)
app.include_router(town.router)
app.include_router(igm.router)
app.include_router(vault.router)
app.include_router(settings.router)


@app.get("/api/health")
def health() -> HealthResponse:
    return HealthResponse()


@app.on_event("startup")
def startup() -> None:
    from brainbot import initialize_ai
    thread = threading.Thread(target=initialize_ai, daemon=True)
    thread.start()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8742, reload=True)

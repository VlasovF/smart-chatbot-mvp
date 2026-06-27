from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, HTTPException

from src.api.deps import get_current_user
from src.core.config import settings
from src.db.models import User

router = APIRouter(prefix="/models", tags=["models"])


@router.get("/")
async def get_models(current_user: Annotated[User, Depends(get_current_user)]):
    """
    Получение списка доступных моделей из Ollama
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{settings.OLLAMA_BASE_URL}/api/tags")
            response.raise_for_status()

            data = response.json()
            models = [
                {
                    "name": model["name"],
                    "size": model.get("size", 0),
                    "modified_at": model.get("modified_at", ""),
                }
                for model in data.get("models", [])
            ]
            return {"models": models}

    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="Ollama service is not available. Please check if Ollama is running.",
        ) from None
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch models: {str(e)}"
        ) from e

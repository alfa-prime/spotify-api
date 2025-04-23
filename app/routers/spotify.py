from typing import Annotated

import httpx
from fastapi import APIRouter, Depends

from app.core import get_settings
from app.core.config import Settings

router = APIRouter(prefix="/spotify", tags=["spotify"])


@router.get("/token")
async def get_token(settings: Annotated[Settings, Depends(get_settings)]):
    async with httpx.AsyncClient() as client:
        url = "https://accounts.spotify.com/api/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        params = {
            "grant_type": "client_credentials",
            "client_id": settings.CLIENT_ID,
            "client_secret": settings.CLIENT_SECRET

        }

        response = await client.post(url, headers=headers, params=params)

    return response.json()

import time
from functools import lru_cache
from typing import Annotated

import httpx
import asyncio
from fastapi import HTTPException, Depends, status

from app.core import Settings, get_settings, get_httpx_client, get_refresh_lock

TOKEN_URL = "https://accounts.spotify.com/api/token"


async def fetch_fresh_token(
        settings: Settings,
        client: httpx.AsyncClient,
) -> tuple[str, float]:
    response = await client.post(
        TOKEN_URL,
        data={"grant_type": "client_credentials"},
        auth=(settings.CLIENT_ID, settings.CLIENT_SECRET),
    )
    if response.status_code != 200:
        raise HTTPException(response.status_code, response.text)

    if response.status_code >= 500:
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, detail="Upstream Spotify error")

    data = response.json()
    return data["access_token"], time.time() + data["expires_in"]


@lru_cache
def _token_holder() -> dict[str, tuple[str, float]]:
    return {}


async def get_token(
        settings: Annotated[Settings, Depends(get_settings)],
        client: Annotated[httpx.AsyncClient, Depends(get_httpx_client)],
        lock: Annotated[asyncio.Lock, Depends(get_refresh_lock)],
) -> str:
    bag = _token_holder()
    access, exp = bag.get("spotify", ("", 0.0))

    if not access or exp - time.time() < 30:
        async with lock:  # ☑ гарантируем один refresh
            access, exp = bag.get("spotify", ("", 0.0))
            if not access or exp - time.time() < 30:
                access, exp = await fetch_fresh_token(settings, client)
                bag["spotify"] = (access, exp)

    return access

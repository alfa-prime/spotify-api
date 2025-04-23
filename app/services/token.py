import time
from functools import lru_cache
from typing import Annotated

import httpx
from fastapi import HTTPException, Depends
from pydantic import BaseModel

from app.core import Settings, get_settings


TOKEN_URL = "https://accounts.spotify.com/api/token"

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_at: float


@lru_cache
def _token_holder() -> dict[str, Token]:
    return {}


async def fetch_fresh_token(settings: Settings) -> Token:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            TOKEN_URL,
            data={"grant_type": "client_credentials"},
            auth=(settings.CLIENT_ID, settings.CLIENT_SECRET)
        )

        if response.status_code != 200:
            raise HTTPException(response.status_code, response.text)

        data = response.json()

        return Token(
            access_token=data["access_token"],
            token_type=data["token_type"],
            expires_at=time.time() + data["expires_in"],
        )


async def get_token(settings: Annotated[Settings, Depends(get_settings)]) -> str:
    bag = _token_holder()
    token: Token | None = bag.get("spotify")

    if not token or token.expires_at - time.time() < 30:
        token = await fetch_fresh_token(settings)
        bag["spotify"] = token

    return token.access_token

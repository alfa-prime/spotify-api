from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, Query, HTTPException

from app.services import get_token

SEARCH_URL = "https://api.spotify.com/v1/search"

router = APIRouter(prefix="/spotify", tags=["spotify"])


@router.get("/search/playlists")
async def search_playlists(
        token: Annotated[str, Depends(get_token)],
        query: Annotated[str, Query(min_length=1, description="The search query")],
        limit: Annotated[int, Query(ge=1, le=50)] = 10,
        offset: Annotated[int, Query(ge=0)] = 0
):
    """
    Поиск публичных плейлистов по ключевым словам.
    Spotify API → GET /v1/search?type=playlist
    """
    async with httpx.AsyncClient(
            headers={"Authorization": f"Bearer {token}"}
    ) as client:
        response = await client.get(
            url=SEARCH_URL,
            params={
                "q": query,
                "type": "playlist",
                "limit": limit,
                "offset": offset,
            },
        )

    if response.status_code != 200:
        raise HTTPException(response.status_code, response.text)

    return response.json()


@router.get("/search/tracks")
async def search_tracks(
        token: Annotated[str, Depends(get_token)],
        query: Annotated[str, Query(min_length=1, description="Строка поиска")],
        limit: Annotated[int, Query(ge=1, le=50)] = 10,
        offset: Annotated[int, Query(ge=0)] = 0,
        market: Annotated[str | None, Query(min_length=2, max_length=2)] = None,  # ISO-3166 код, напр. RU

):
    """
    Ищем публичные треки.
    Spotify: GET /v1/search?type=track
    """
    async with httpx.AsyncClient(
            headers={"Authorization": f"Bearer {token}"}
    ) as client:
        resp = await client.get(
            url=SEARCH_URL,
            params={
                "q": query,
                "type": "track",
                "limit": limit,
                "offset": offset,
                **({"market": market} if market else {}),
            },
        )

    if resp.status_code != 200:
        raise HTTPException(resp.status_code, resp.text)

    return resp.json()


@router.get("/search/albums")
async def search_albums(
        token: Annotated[str, Depends(get_token)],
        query: Annotated[str, Query(min_length=1, description="Название/артист")],
        limit: Annotated[int, Query(ge=1, le=50)] = 10,
        offset: Annotated[int, Query(ge=0)] = 0,
        market: Annotated[str | None, Query(min_length=2, max_length=2)] = None,  # ISO-3166 код страны

):
    """
    Поиск публичных альбомов.
    Spotify → GET /v1/search?type=album
    """
    async with httpx.AsyncClient(
            headers={"Authorization": f"Bearer {token}"}
    ) as client:
        response = await client.get(
            url=SEARCH_URL,
            params={
                "q": query,
                "type": "album",
                "limit": limit,
                "offset": offset,
                **({"market": market} if market else {}),
            },
        )

    if response.status_code != 200:
        raise HTTPException(response.status_code, response.text)

    return response.json()

from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, Query, HTTPException, status

from app.services import get_token
from app.core import get_httpx_client

SEARCH_URL = "https://api.spotify.com/v1/search"

router = APIRouter(prefix="/spotify", tags=["spotify"])


@router.get("/search/playlists")
async def search_playlists(
        token: Annotated[str, Depends(get_token)],
        client: Annotated[httpx.AsyncClient, Depends(get_httpx_client)],
        query: Annotated[str, Query(min_length=1, description="The search query")],
        limit: Annotated[int, Query(ge=1, le=50)] = 10,
        offset: Annotated[int, Query(ge=0)] = 0
):
    """
    Поиск публичных плейлистов по ключевым словам.
    Spotify API → GET /v1/search?type=playlist
    """

    response = await client.get(
        url=SEARCH_URL,
        headers={"Authorization": f"Bearer {token}"},
        params={
            "q": query,
            "type": "playlist",
            "limit": limit,
            "offset": offset,
        },
    )

    if response.status_code != 200:
        raise HTTPException(response.status_code, response.text)

    if response.status_code >= 500:
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, detail="Upstream Spotify error")

    return response.json()


@router.get("/search/tracks")
async def search_tracks(
        token: Annotated[str, Depends(get_token)],
        client: Annotated[httpx.AsyncClient, Depends(get_httpx_client)],
        query: Annotated[str, Query(min_length=1, description="Строка поиска")],
        limit: Annotated[int, Query(ge=1, le=50)] = 10,
        offset: Annotated[int, Query(ge=0)] = 0,
        market: Annotated[str | None, Query(min_length=2, max_length=2)] = None,  # ISO-3166 код, напр. RU

):
    """
    Ищем публичные треки.
    Spotify: GET /v1/search?type=track
    """
    response = await client.get(
        url=SEARCH_URL,
        headers={"Authorization": f"Bearer {token}"},
        params={
            "q": query,
            "type": "track",
            "limit": limit,
            "offset": offset,
            **({"market": market} if market else {}),
        },
    )

    if response.status_code != 200:
        raise HTTPException(response.status_code, response.text)

    if response.status_code >= 500:
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, detail="Upstream Spotify error")

    return response.json()


@router.get("/search/albums")
async def search_albums(
        token: Annotated[str, Depends(get_token)],
        client: Annotated[httpx.AsyncClient, Depends(get_httpx_client)],
        query: Annotated[str, Query(min_length=1, description="Название/артист")],
        limit: Annotated[int, Query(ge=1, le=50)] = 10,
        offset: Annotated[int, Query(ge=0)] = 0,
        market: Annotated[str | None, Query(min_length=2, max_length=2)] = None,  # ISO-3166 код страны

):
    """
    Поиск публичных альбомов.
    Spotify → GET /v1/search?type=album
    """
    response = await client.get(
        url=SEARCH_URL,
        headers={"Authorization": f"Bearer {token}"},
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

    if response.status_code >= 500:
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, detail="Upstream Spotify error")

    return response.json()

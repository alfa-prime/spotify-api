from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, Query

from app.services import get_token, raise_if_error
from app.core import get_httpx_client
from app.models.spotify import PlaylistsPage, TracksPage, AlbumsPage

SEARCH_URL = "https://api.spotify.com/v1/search"

router = APIRouter(prefix="/spotify", tags=["spotify"])


@router.get("/search/playlists", response_model=PlaylistsPage)
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
    raise_if_error(response)

    raw = response.json()["playlists"]
    raw["items"] = [pl for pl in raw["items"] if pl is not None]
    return raw


@router.get("/search/tracks", response_model=TracksPage)
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
    raise_if_error(response)
    return response.json()["tracks"]


@router.get("/search/albums", response_model=AlbumsPage)
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
    raise_if_error(response)

    raw = response.json()["albums"]  # достаём вложенный объект
    raw["items"] = [alb for alb in raw["items"] if alb is not None]  # Spotify иногда шлёт null
    return raw

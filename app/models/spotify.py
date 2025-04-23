from typing import Any, List, Optional, Dict
from pydantic import BaseModel, Field, HttpUrl, ConfigDict


class Image(BaseModel):
    url: HttpUrl
    width: Optional[int] = None
    height: Optional[int] = None


# ── Треки ─────────────────────────────────
class ArtistMini(BaseModel):
    id: str
    name: str


class TrackItem(BaseModel):
    id: str
    name: str
    artists: List[ArtistMini]
    preview_url: Optional[HttpUrl] = Field(
        None, description="30-секундное превью трека"
    )
    external_urls: Dict[str, HttpUrl]

    @property
    def external_url(self) -> HttpUrl:  # noqa: D401
        """Удобный «плоский» доступ к ссылке Spotify."""
        return self.external_urls["spotify"]

    model_config = ConfigDict(extra="ignore")


class TracksPage(BaseModel):
    items: List[TrackItem]
    total: int
    offset: int
    limit: int

    model_config = ConfigDict(extra="ignore")


# ── Плейлисты ─────────────────────────────
class PlaylistOwner(BaseModel):
    display_name: str


class PlaylistItem(BaseModel):
    id: str
    name: str
    owner: PlaylistOwner
    images: List[Image]
    external_urls: Dict[str, HttpUrl]  # ← принимаем весь вложенный объект

    # хотим в Swagger видеть плоское поле – делаем property
    @property
    def external_url(self) -> HttpUrl:  # noqa: D401
        return self.external_urls["spotify"]

    model_config = ConfigDict(extra="ignore")


class PlaylistsPage(BaseModel):
    items: List[PlaylistItem]
    total: int
    offset: int
    limit: int

    model_config = ConfigDict(extra="ignore")


# ── Альбомы ───────────────────────────────
class AlbumItem(BaseModel):
    id: str
    name: str
    release_date: str
    images: List[Image]
    artists: List[ArtistMini]

    external_urls: Dict[str, HttpUrl]

    @property
    def external_url(self) -> HttpUrl:
        return self.external_urls["spotify"]

    model_config = ConfigDict(extra="ignore")


class AlbumsPage(BaseModel):
    items: List[AlbumItem]
    total: int
    offset: int
    limit: int

    model_config = ConfigDict(extra="ignore")

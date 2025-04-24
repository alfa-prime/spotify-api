from contextlib import asynccontextmanager

import httpx
import asyncio
from fastapi import FastAPI

from app.routers import router_spotify


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa
    app.state.httpx = httpx.AsyncClient(timeout=10, headers={'User-Agent': 'nord-cloud-music-api/1.0'})
    app.state.refresh_lock = asyncio.Lock()
    yield
    await app.state.httpx.aclose()


app = FastAPI(
    lifespan=lifespan,
    title="Nord-Cloud Music search API",
    summary="Бридж между GPT-шкой и Spotify",
    servers=[{"url": "https://api.nord-cloud.ru"}],
    version="0.1.0",
)

app.include_router(router_spotify)

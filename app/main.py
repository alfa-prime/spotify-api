from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI

from app.routers import router_spotify


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.httpx = httpx.AsyncClient(timeout=10)
    yield
    await app.state.httpx.aclose()


app = FastAPI(
    lifespan=lifespan,
    title="Nord-Cloud Music search API",
    summary="Бридж между GPT-шкой и Spotify | Youtube music",
    version="0.1.0",
)

app.include_router(router_spotify)

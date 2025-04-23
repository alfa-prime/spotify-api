from app.routers import router_spotify
from fastapi import FastAPI


app = FastAPI(
    title="Nord-Cloud Spotify API",
    summary="Бридж между GPT-шкой и Spotify",
    version="0.1.0",
)

app.include_router(router_spotify)
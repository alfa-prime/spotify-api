from fastapi import Request
import httpx
import asyncio


def get_httpx_client(request: Request) -> httpx.AsyncClient:
    """
    Возвращает общий httpx.AsyncClient, созданный в lifespan.
    """
    return request.app.state.httpx


def get_refresh_lock(request: Request) -> asyncio.Lock:
    return request.app.state.refresh_lock

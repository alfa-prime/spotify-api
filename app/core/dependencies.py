from fastapi import Request
import httpx

def get_httpx_client(request: Request) -> httpx.AsyncClient:
    """
    Возвращает общий httpx.AsyncClient, созданный в lifespan.
    """
    return request.app.state.httpx
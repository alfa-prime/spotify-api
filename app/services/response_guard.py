import httpx
from fastapi import HTTPException, status


def raise_if_error(response: httpx.Response, upstream: str = "Spotify") -> None:
    """
    Унифицирует обработку ответов.
    * 5xx → 502 Bad Gateway наружу
    * всё, что не 200 → проксируем как есть
    * 200 → ничего не делает
    """
    if response.status_code >= 500:
        raise HTTPException(
            status.HTTP_502_BAD_GATEWAY,
            detail=f"Upstream {upstream} error"
        )
    elif response.status_code != 200:
        # передадим тело Spotify, если там JSON с ошибкой
        try:
            detail = response.json()
        except ValueError:
            detail = response.text
        raise HTTPException(response.status_code, detail)

import httpx
from fastapi import Request


async def get_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.async_client

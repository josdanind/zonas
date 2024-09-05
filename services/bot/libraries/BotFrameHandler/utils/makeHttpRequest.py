import aiohttp
from libraries.BotFrameHandler.utils import print_error_detail, print_test
from libraries.BotFrameHandler.utils import http_exception_handler

@http_exception_handler
async def fetch(
    session: aiohttp.ClientSession,
    url:str,
    method: str = "GET",
    data: dict | None = None,
    params: dict | None = None,
    headers: dict | None = None
) -> dict:
    async with session.request(
        method=method,
        url=url,
        params=params,
        json=data,
        headers=headers
    ) as response:
        response.raise_for_status

        return await response.json()
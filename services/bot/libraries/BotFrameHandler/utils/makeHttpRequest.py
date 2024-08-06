import aiohttp

async def fetch(
    session: aiohttp.ClientSession,
    url:str,
    method: str = "GET",
    data: dict | None = None,
    params: dict | None = None,
    headers: dict | None = None
) -> dict:
    try:
        async with session.request(
            method=method,
            url=url,
            params=params,
            json=data,
            headers=headers
        ) as response:
            response.raise_for_status
            return await response.json()
    except aiohttp.ClientError as e:
        print(f"Client error: {e}")
        return {"error": str(e)}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"error": str(e)}
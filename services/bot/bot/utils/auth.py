# Standard Library
import json

# Environment variables
from config import API_CRUD_URL

# aiohttp
import aiohttp


async def user_auth(user):
    endpoint = API_CRUD_URL + f"/login/{user}"

    async with aiohttp.ClientSession() as session:
        async with session.post(url=endpoint) as response:
            user = await response.json()

            return user if response.status == 200 else None

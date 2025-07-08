from . import config
import asyncio
import aiohttp

async def is_bot_public(bot_token: str) -> bool:
    url = "https://discord.com/api/v10/oauth2/applications/@me"
    headers = {
        "Authorization": f"Bot {bot_token}"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                text = await response.text()
                raise Exception(f"Failed to retrieve app info: {response.status} {text}")
            
            data = await response.json()
            return data.get("bot_public", True)  # Default to True if missing

def run_pb_check():
    check = asyncio.run(is_bot_public(config.config['setup']['token']))
    if check:
        err = "This bot cannot be run with 'Public bot' enabled. Please disable it in your devloper portal."
        raise RuntimeError(err)
    else:
        print("[INFO]: PB check passed")
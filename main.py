import discord
from discord.ext import commands
from discord import app_commands
import os
import json
import utils.config
import aiohttp
import asyncio
from utils.checks import *
client = commands.Bot(command_prefix=utils.config.config['setup']['command_prefix'], intents=discord.Intents.all())



@client.event
async def on_ready():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and not filename.startswith('_'):
            cog_name = f'cogs.{filename[:-3]}'
            try:
                await client.load_extension(cog_name)
                print(f'[SUCCESS] Loaded extension {cog_name}')
            except Exception as e:
                print(f'[ERROR] Failed to load {cog_name}: {e}')
    await client.tree.sync()
    print(f"Online as {client.user.name}")




run_pb_check()

client.run(utils.config.config['setup']['token'])

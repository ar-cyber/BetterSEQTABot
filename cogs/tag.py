import discord
from discord.ext import commands
from discord.ext.commands import Cog
from discord import app_commands
import json, os
class Tag(Cog):
    def __init__(self, bot):
        self.client = bot
    
    @app_commands.command(name = "tag", description = "Show a tag (please ask robinand to add the tag)")
    async def _tagslash(self, ctx: discord.Interaction, tag: str):
        
        found = False
        for item in os.listdir('cogs/embed'):
            if tag != item.replace(".json", ""):
                pass
            else:
                tagitem = item
                found = True
                break
        if not found:
            return await ctx.response.send_message("This tag does not exist!", ephemeral=True)
        f = json.load(open(f"cogs/embed/{tagitem}", 'rb'))['embed']

        embed = discord.Embed(title = f['title'], description = f['description'])
        if 'fields' in f:
            for field in f['fields']:
                embed.add_field(name = field['title'], value = field['value'], inline = True if ('inline' in f) and f['inline'] else False)
        if 'image' in f:
            embed.set_image(url = f['image'])
        await ctx.response.send_message(embed=embed)

    @commands.command(name = "tag", description = "Show a tag (please ask robinand to add the tag)")
    async def _tag(self, ctx, tag: str):
        # tag = tag.value
        found = False
        for item in os.listdir('cogs/embed'):
            if tag != item.replace(".json", ""):
                pass
            else:
                tagitem = item
                found = True
                break
        if not found:
            return await ctx.send("This tag does not exist!")
        f = json.load(open(f"cogs/embed/{tagitem}", 'rb'))['embed']

        embed = discord.Embed(title = f['title'], description = f['description'])
        if 'fields' in f:
            for field in f['fields']:
                embed.add_field(name = field['title'], value = field['value'], inline = True if ('inline' in f) and f['inline'] else False)
        if 'image' in f:
            embed.set_image(url = f['image'])
        await ctx.send(embed=embed)

    @app_commands.command(name = "tags", description = "List the tags")
    async def _tagsslash(self, ctx: discord.Interaction):
        embed = discord.Embed(title = "Tags", description = "View the tags!")
        for item in os.listdir('cogs/embed'):
            embed.add_field(name = f'{json.load(open(f'cogs/embed/{item}', 'rb'))['embed']['title']}', value = f"""
    ID: {item.replace('.json', '')}
    Run `/tag {item.replace('.json', '')}` or `!tag {item.replace('.json', '')}` to view this tag!

    """, inline=True)
        await ctx.response.send_message(embed=embed)

    @commands.command(name = "tags", description = "List the tags")
    async def _tags(self, ctx):
        embed = discord.Embed(title = "Tags", description = "View the tags!")
        cnt = 0
        for item in os.listdir('cogs/embed'):
            if cnt == 15:
                break
            embed.add_field(name = f'{json.load(open(f'cogs/embed/{item}', 'rb'))['embed']['title']}', value = f"""
    ID: {item.replace('.json', '')}
    Run `/tag {item.replace('.json', '')}` or `!tag {item.replace('.json', '')}` to view this tag!

    """, inline=True)
            cnt += 1
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Tag(bot))
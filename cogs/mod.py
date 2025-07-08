import discord
from discord.ext import commands
from discord.ext.commands import Cog
from discord import app_commands
class Moderation(Cog):
    def __init__(self, bot):
        self.client = bot
    
    @app_commands.command(name = "kick", description = "Boot a user from the Discord")
    @commands.has_permissions(kick_members = True)
    async def _kick(self, ctx: discord.Interaction, member: discord.Member, reason: str="No reason provided"):
        if member == self.client.user:
            return await ctx.response.send_message(embed=discord.Embed(title = "Error", description="You can't kick me!"))
        elif member.bot:
            return await ctx.response.send_message(embed=discord.Embed(title = "Error", description = "You can't kick bots! This is a API limitation."))
        else:
            await member.kick(reason = reason)
            try:
                await member.send(
                    embed = discord.Embed(
                        title = f"You have been kicked!",
                        description = f"You were kicked from {ctx.guild.name}.\n Reason: {reason}. \nResponsable moderator: {ctx.user.name}"
                    )
                )
            except discord.Forbidden:
                await ctx.response.send_message(embed = discord.Embed(
                    title = "Success!",
                    description = f"Successfully kicked {member.name} for the following reason: {reason}. I could not send a DM though."
                ), ephemeral=True)
                return
            await ctx.response.send_message(embed = discord.Embed(
                title = "Success!",
                description = f"Successfully kicked {member.name} for the following reason: {reason}"
            ), ephemeral=True)

    @app_commands.command(name = "ban", description = "USE THE ALMIGHTY BAN HAMMER")
    @commands.has_permissions(ban_members = True)
    async def _ban(self, ctx: discord.Interaction, member: discord.Member, reason: str="No reason provided"):
        if member == self.client.user:
            return await ctx.response.send_message(embed=discord.Embed(title = "Error", description="You can't ban me!"))
        elif member.bot:
            return await ctx.response.send_message(embed=discord.Embed(title = "Error", description = "You can't ban bots! This is a API limitation."))
        else:
            await member.ban(reason = reason)
            try:
                await member.send(
                    embed = discord.Embed(
                        title = f"You have been banned!",
                        description = f"You were banned from {ctx.guild.name}.\n Reason: {reason}. \nResponsable moderator: {ctx.user.name}"
                    )
                )
            except discord.Forbidden:
                await ctx.response.send_message(embed = discord.Embed(
                    title = "Success!",
                    description = f"Successfully banned {member.name} for the following reason: {reason}. I could not send a DM though."
                ), ephemeral=True)
                return
            await ctx.response.send_message(embed = discord.Embed(
                title = "Success!",
                description = f"Successfully banned {member.name} for the following reason: {reason}"
            ), ephemeral=True)
    
    @app_commands.command(name = "unban", description = "REVERT THE ALMIGHTY BAN HAMMER")
    @commands.has_permissions(ban_members = True)
    async def _unban(self, ctx: discord.Interaction, member: discord.User, reason: str="No reason provided"):
        if member == self.client.user:
            return await ctx.response.send_message(embed=discord.Embed(title = "Error", description="How would I be banned?"))
        bans = await ctx.guild.bans()
        if any(ban_entry.user.id == member.id for ban_entry in bans):
            return await ctx.response.send_message(embed=discord.Embed(title = "Error", description="Why unban a user who's already not banned??"))
        else:
            await ctx.guild.unban(member, reason=reason)
            await ctx.response.send_message(embed = discord.Embed(
                title = "Success!",
                description = f"Successfully unbanned {member.name} for the following reason: {reason}"
            ), ephemeral=True)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
import discord
from discord.ext import commands
from discord.ext.commands import Cog
from discord import app_commands
import utils.config

class Report(Cog):
    def __init__(self, bot):
        self.client = bot
    
    class ReportModal(discord.ui.Modal):
        def __init__(self, client, user: discord.User):
            
            self.user = user
            self.client = client
            self.offender = discord.ui.TextInput(label = "Please enter the ID of the offender.", required=True, max_length=999)
            self.body = discord.ui.TextInput(label = "Why are you reporting them?", required=True, max_length=999)
            self.image = discord.ui.TextInput(label = "Add a link of proof [split with ,]", required=True, max_length = 100)
            
            super().__init__(title = "Enter the suggestion details")
            self.add_item(self.offender)
            self.add_item(self.body)
            self.add_item(self.image)
        async def on_submit(self, ctx: discord.Interaction):
            embed = discord.Embed(title = f"Report from {self.user.name}: {self.offender.value}", description=self.body.value)
            embed.add_field(name = "Evidence", value = self.image.value)

            target_channel_id = utils.config.config['report']['channel']
            print(target_channel_id)
            # Fetch the channel using the bot instance
            channel = self.client.get_channel(target_channel_id)
            if channel is None:
                channel = await self.client.fetch_channel(target_channel_id)
            message = await channel.send(embed=embed)
            await message.create_thread(
                name=self.offender.value
            )
            await ctx.response.send_message("Successfully sent report.", ephemeral=True)
            
    @app_commands.command(name = "report", description = "Report a user")
    async def _report(self, ctx: discord.Interaction):
        await ctx.response.send_modal(self.ReportModal(self.client, ctx.user))
async def setup(bot):
    await bot.add_cog(Report(bot))
import discord
from discord.ext import commands
from discord.ext.commands import Cog
from discord import app_commands
import utils.config
class Suggest(Cog):
    def __init__(self, bot):
        self.client = bot
    # Step 1: Define your View (can be inside or outside the Cog)

    class VoteView(discord.ui.View):
        def __init__(self, author_id: int):
            super().__init__(timeout=None)
            self.author_id = author_id
            self.upvotes = 0
            self.downvotes = 0
            self.votes = {}  # user_id: "up" or "down"

        async def _check_author(self, interaction: discord.Interaction):
            if interaction.user.id == self.author_id:
                await interaction.response.send_message("You cannot vote on your own suggestion.", ephemeral=True)
                return False
            return True

        @discord.ui.button(label="👍 0", style=discord.ButtonStyle.green, custom_id="vote:up")
        async def upvote(self, interaction: discord.Interaction, button: discord.ui.Button):
            if not await self._check_author(interaction):
                return

            user_id = interaction.user.id
            previous_vote = self.votes.get(user_id)

            if previous_vote == "up":
                await interaction.response.send_message("You already upvoted!", ephemeral=True)
                return
            elif previous_vote == "down":
                self.downvotes -= 1
                self.upvotes += 1
                self.votes[user_id] = "up"
                await interaction.response.send_message("Changed your vote to Upvote!", ephemeral=True)
            else:
                self.upvotes += 1
                self.votes[user_id] = "up"
                await interaction.response.send_message("You upvoted!", ephemeral=True)

            button.label = f"👍 {self.upvotes}"
            downvote_button = self.children[1]
            downvote_button.label = f"👎 {self.downvotes}"

            await interaction.message.edit(view=self)

        @discord.ui.button(label="👎 0", style=discord.ButtonStyle.red, custom_id="vote:down")
        async def downvote(self, interaction: discord.Interaction, button: discord.ui.Button):
            if not await self._check_author(interaction):
                return

            user_id = interaction.user.id
            previous_vote = self.votes.get(user_id)

            if previous_vote == "down":
                await interaction.response.send_message("You already downvoted!", ephemeral=True)
                return
            elif previous_vote == "up":
                self.upvotes -= 1
                self.downvotes += 1
                self.votes[user_id] = "down"
                await interaction.response.send_message("Changed your vote to Downvote!", ephemeral=True)
            else:
                self.downvotes += 1
                self.votes[user_id] = "down"
                await interaction.response.send_message("You downvoted!", ephemeral=True)

            button.label = f"👎 {self.downvotes}"
            upvote_button = self.children[0]
            upvote_button.label = f"👍 {self.upvotes}"

            await interaction.message.edit(view=self)

    class SuggestModal(discord.ui.Modal):
        def __init__(self, client, user: discord.User):
            
            self.user = user
            self.client = client
            self.title_suggest = discord.ui.TextInput(label = "Please enter the title for your suggestion", max_length=60, required = True)
            self.body = discord.ui.TextInput(label = "Please describe your issue", required=True, max_length=999)
            self.image = discord.ui.TextInput(label = "OPTIONAL: Add a image of your suggestion", required=False, max_length = 100)
            
            super().__init__(title = "Enter the suggestion details")
            self.add_item(self.title_suggest)
            self.add_item(self.body)
            self.add_item(self.image)
        async def on_submit(self, ctx: discord.Interaction):
            embed = discord.Embed(title = f"Suggestion from {self.user.name}: {self.title_suggest.value}", description=self.body.value)
            embed.set_image(url=self.image)

            target_channel_id = utils.config.config['suggest']['channel']
            # Fetch the channel using the bot instance
            channel = self.client.get_channel(target_channel_id)
            if channel is None:
                channel = await self.client.fetch_channel(target_channel_id)
            message = await channel.send(embed=embed, view=Suggest.VoteView(self.user.id))
            await message.create_thread(
                name=self.title_suggest.value
            )
            await ctx.response.send_message("Successfully sent suggestion.", ephemeral=True)
            

    @app_commands.command(name = "suggest", description = "Make a suggestion")
    async def _suggest(self, ctx: discord.Interaction):
        await ctx.response.send_modal(self.SuggestModal(self.client, ctx.user))

async def setup(bot):
    bot.add_view(Suggest.VoteView(0))
    print("cogs.suggest: Loaded persistant view") 
    await bot.add_cog(Suggest(bot))
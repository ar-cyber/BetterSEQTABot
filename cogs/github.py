import discord
from discord.ext import commands, tasks
from discord.ext.commands import Cog
from discord import app_commands
import utils.config
from github import Github, InputGitAuthor
from github import Auth
import datetime
import io
import json
from aiohttp import web
import asyncio
auth = Auth.Token(utils.config.config['github']['token'])
global g
g = Github(auth=auth)



routes = web.RouteTableDef()
class GitHub_SEQTA(Cog):
    def __init__(self, bot):
        self.client = bot
        self.app = web.Application()
        self.app.router.add_post('/github', self.github_webhook)  # register handler
        self.runner = web.AppRunner(self.app)
        bot.loop.create_task(self.start_webhook_server())
    
    async def github_webhook(self, request):
        print("Got request")
        data = await request.json()
        j = json.load(open('cogs/forummemory.json', 'r'))
        event = request.headers.get('X-GitHub-Event')
        print(event)
        print(data)
        # Only handle comments on issues
        if event == 'issue_comment':
            gissue = data['issue']
            comment = data['comment']

            for issue in j['sessions']:
                        # Only if it's the target issue number
                if gissue['number'] == issue['issue_number']:
                    author = comment['user']['login']

                    body = comment['body']
                    
                    msg = f"**{author}**: {body}"
                    channel = self.client.get_channel(issue['channel_id'])
                    await channel.send(msg)
        elif event == 'issues':
            gissue = data['issue']['number']
            if data['action'] == 'closed':
                for issue in j['sessions']:
                    if gissue == issue['issue_number']:
                        print(issue)
                        author = data['issue']['user']['login']
                        msg = f":x: **{author}** closed the issue."
                        channel = self.client.get_channel(issue['channel_id'])
                        await channel.edit(archived=True)
                        await channel.send(msg)
            if data['action'] == 'reopened':
                for issue in j['sessions']:
                    if gissue == issue['issue_number']:
                        print(issue)
                        author = data['issue']['user']['login']
                        msg = f":arrows_counterclockwise: **{author}** reopened the issue."
                        channel = self.client.get_channel(issue['channel_id'])
                        await channel.edit(archived=False)
                        await channel.send(msg)
            if data['action'] == 'locked':
                for issue in j['sessions']:
                    if gissue == issue['issue_number']:
                        print(issue)
                        author = data['issue']['user']['login']
                        msg = f":lock: **{author}** locked this channel to people with write access/mods."
                        channel = self.client.get_channel(issue['channel_id'])
                        await channel.edit(locked=True, archived = False)
                        await channel.send(msg)
            if data['action'] == 'unlocked':
                for issue in j['sessions']:
                    if gissue == issue['issue_number']:
                        print(issue)
                        author = data['issue']['user']['login']
                        msg = f":white_check_mark: **{author}** unlocked this channel."
                        channel = self.client.get_channel(issue['channel_id'])
                        await channel.edit(locked=False, archived = False)
                        await channel.send(msg)

        return web.Response(text='OK')
    async def start_webhook_server(self):
        await self.runner.setup()
        site = web.TCPSite(self.runner, '0.0.0.0', 5000)
        await site.start()
        print("🌐 GitHub webhook listener started on http://localhost:5000/github")

    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        data = json.load(open('cogs/forummemory.json', 'r'))
        if thread.parent.type == discord.ChannelType.forum and thread.parent.id == int(utils.config.config['github']['forumid']):
            owner = await thread.fetch_member(thread.owner_id) 
            print(f"New forum post detected: {thread.name}") 
            content = await thread.fetch_message(thread.id)
            body = f'''Autocollected from Discord by BetterSEQTA-Bot
## Created by {thread.owner.name}
{content.content}
## Nerdy info
Thread ID (for comments): {thread.id}
'''
            repo = g.get_repo(utils.config.config['github']['issuerepo'])
            id = repo.create_issue(title=thread.name, body = body).number
            
            await thread.send(f"**You may find a GitHub issue in https://github.com/{utils.config.config['github']['issuerepo']}/issues/{id}**")
            jsons = {
                "channel_id": thread.id,
                "issue_number": id
            }
            data['sessions'].append(jsons)
            print(data)
            with open('cogs/forummemory.json', 'w') as fp:
                json.dump(data, fp)
            print("Done")
    @commands.Cog.listener()
    async def on_thread_update(self, before: discord.Thread, after: discord.Thread):
        print(after.archived)
        repo = g.get_repo(utils.config.config['github']['issuerepo'])
        if not before.archived and after.archived:
            print(f"📁 Thread '{after.name}' was archived.")

            # Load your GitHub mapping
            data = json.load(open('cogs/forummemory.json', 'r'))

            for item in data['sessions']:
                if item['channel_id'] == after.id:
                    # Get the GitHub issue and close it
                    
                    issue = repo.get_issue(number=item['issue_number'])
                    issue.edit(state='closed')
                    print(f"✅ Closed GitHub issue #{item['issue_number']} because thread was archived.")
                    channel = self.client.get_channel(item['channel_id'])
                    await channel.send("**MGMT**: We detected  that this channel was closed. PLEASE NOTE THAT YOU WILL NEED TO MANUALLY OPEN THE GITHUB ISSUE DUE TO DISCORD LIMITATIONS. ")
        if before.archived and not after.archived:
            print(f"📁 Thread '{after.name}' was unarchived.")

            # Load your GitHub mapping
            data = json.load(open('cogs/forummemory.json', 'r'))

            for item in data['sessions']:
                if item['channel_id'] == after.id:
                    # Get the GitHub issue and close it
                    
                    issue = repo.get_issue(number=item['issue_number'])
                    issue.edit(state='open')
                    
        if not before.locked and after.locked:
            print(f"📁 Thread '{after.name}' was locked.")

            # Load your GitHub mapping
            data = json.load(open('cogs/forummemory.json', 'r'))

            for item in data['sessions']:
                if item['channel_id'] == after.id:
                    # Get the GitHub issue and close it
                    
                    issue = repo.get_issue(number=item['issue_number'])
                    issue.lock("too heated")
        if before.locked and not after.locked:
            print(f"📁 Thread '{after.name}' was unlocked.")

            # Load your GitHub mapping
            data = json.load(open('cogs/forummemory.json', 'r'))

            for item in data['sessions']:
                if item['channel_id'] == after.id:
                    # Get the GitHub issue and close it
                    
                    issue = repo.get_issue(number=item['issue_number'])
                    issue.unlock()
                    


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return  # ignore bot messages
        repo = g.get_repo(utils.config.config['github']['issuerepo'])
        print(message.channel.id)
        data = json.load(open('cogs/forummemory.json', 'r'))
        for item in data['sessions']:
            if item['channel_id'] == message.channel.id:
                github_issue = repo.get_issue(number=item['issue_number'])
                github_issue.create_comment(f"**{str(message.author)} | {str(message.author.id)}:** " + message.content)
            else:
                pass

    @app_commands.command(name = "submit_theme", description = "Submit a theme to the themes repo")
    @commands.has_role(utils.config.config['github']['themerole'])
    async def _submit_theme(self, ctx: discord.Interaction, theme_name: str, file: discord.Attachment):
        await ctx.response.send_message("Started. Please wait for it to finish; it could take a long time. Please wait for a DM to indicate it's finished.", ephemeral=True)
        file_bytes = await file.read()
        file_name = file.filename
        repo = g.get_repo(utils.config.config['github']['repo'])
        base = repo.get_branch("main")
        # Unique branch name
        branch_name = f"bot-upload-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

        # Create branch from main
        repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=base.commit.sha)

        # Prepare file commit
        author = InputGitAuthor(f"{ctx.user}", f"{ctx.user.id}-BetterSEQTA@betterseqta.org")
        try:
            repo.create_file(
                path=f"uploads/{file_name}",
                message=f"Add Theme {file_name} via Discord bot",
                content=file_bytes,
                branch=branch_name,
                author=author
            )
        except Exception as e:
            return await ctx.response.send_message(f"Failed to create file: {e}", ephemeral=True)
            
        body = f'''Theme created by {ctx.user}.
# Theme information
Theme name: {theme_name}'''
        pr = repo.create_pull(
            title=f"Theme upload {file_name}",
            body=body,
            head=branch_name,
            base="main"
        ).number
        await ctx.user.send(f"The upload has finished. You may check your pull request out at https://github.com/{utils.config.config['github']['repo']}/pulls/{id}")
        await ctx.followup.send("Successfully created the pull request!", ephemeral=True)
        
async def setup(bot):
    await bot.add_cog(GitHub_SEQTA(bot))
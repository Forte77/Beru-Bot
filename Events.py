import discord
from discord.ext import commands
from discord.ext import tasks
from discord.member import Member
from datetime import datetime

class Events(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    @commands.Cog.listener() #Replace @bot.event
    async def on_message(self,msg):
        username = msg.author.display_name
        if msg.author == self.bot.user:
            return
        else:
            if msg.content == "hello":
                await msg.channel.send("hello " + username)
            elif msg.content == "Hello":
                await msg.channel.send("Hello " + username)
            elif msg.content == "p":
                await msg.channel.send("Shut up Blizzerd")
            elif msg.content == "timezone":
                await msg.channel.send("[Timezone helper](https://discordtools.io/timestamp)")
    #When a member joins the server the bot wll DM them.
    @commands.Cog.listener()
    async def on_member_join(self,member):
        guild = member.guild
        guildname = guild.name
        dmchannel = await member.create_dm()
        await dmchannel.send(f"Welcome to {guildname}!")
    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        emoji = payload.emoji.name
        member = payload.member #this implementation only works on reaction add
        message_id = payload.message_id
        guild_id = payload.guild_id
        guild = self.bot.get_guild(guild_id)
        # if statement to confirm emoji and message that is reacted to. google and copy exact emoji.
        if emoji == "🎮" and message_id == 1429934331115212841:
            role = discord.utils.get(guild.roles, name = "gamer")
            await member.add_roles(role)
        if emoji == "📓" and message_id == 1429934331115212841:
            role = discord.utils.get(guild.roles, name = "QA")
            await member.add_roles(role)
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,payload):
        user_id = payload.user_id #used for member
        print(user_id)
        emoji = payload.emoji.name
        message_id = payload.message_id
        guild_id = payload.guild_id
        print(guild_id)
        guild = self.bot.get_guild(guild_id)
        member = await guild.fetch_member(user_id) #how to get member for remove
        '''if member is None:
            # Member not found in cache, try fetching
            try:
                member = await guild.fetch_member(user_id)
            except discord.NotFound:
                # Member not found in the guild
                return'''
        if emoji == "🎮" and message_id == 1429934331115212841:
            role = discord.utils.get(guild.roles, name = "gamer")
            await member.remove_roles(role)
        if emoji == "📓" and message_id == 1429934331115212841:
            role = discord.utils.get(guild.roles, name = "QA")
            await member.remove_roles(role)

async def setup(bot):
    await bot.add_cog(Events(bot))
import nextcord
from nextcord.ext import commands
from nextcord.ext import tasks
from nextcord.member import Member
from datetime import datetime
with open("BotToken.txt",'r') as file:
    lines = file.readlines() #added my id to the bottoken text
    token = lines[0]
    own = lines[1]
    own = int(own)
#Coding commands not event. Command decorator calls a function. Event itself is a function
async def is_me(arg):
        if isinstance(arg,nextcord.Interaction): #adding in slash command functionality so I need to change the is_me check to use context and interactions
            intauth = arg.user.id
            return intauth == own
        else:
            auth = arg.author.id
            return auth == own
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
            elif msg.content == "p" or msg.content == "P":
                await msg.channel.send("Shut up Blizzerd")
            elif msg.content == "timezone":
                await msg.channel.send("[Timezone helper](https://nextcordtools.io/timestamp)")
    #When a member joins the server the bot wll DM them.
    @commands.Cog.listener()
    async def on_member_join(self,member):
        guild = member.guild
        guildname = guild.name
        dmchannel = await member.create_dm()
        await dmchannel.send(f"Welcome to {guildname}!")
    #Going to comment out this whole section. It was partially triggering with the poll and I don't really need it right now  but I wanna keep the stuff above active. Going to just leave it here as notes I guess
    '''@commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        emoji = payload.emoji.name
        member = payload.member #this implementation only works on reaction add
        message_id = payload.message_id
        guild_id = payload.guild_id
        guild = self.bot.get_guild(guild_id)
        # if statement to confirm emoji and message that is reacted to. google and copy exact emoji.
        if emoji == "🎮" and message_id == 1429934331115212841:
            role = nextcord.utils.get(guild.roles, name = "gamer")
            await member.add_roles(role)
        if emoji == "📓" and message_id == 1429934331115212841:
            role = nextcord.utils.get(guild.roles, name = "QA")
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
        if member is None: # Couldn't get this part working
            # Member not found in cache, try fetching
            try:
                member = await guild.fetch_member(user_id)
            except nextcord.NotFound:
                # Member not found in the guild
                return
        if emoji == "🎮" and message_id == 1429934331115212841:
            role = nextcord.utils.get(guild.roles, name = "gamer")
            await member.remove_roles(role)
        if emoji == "📓" and message_id == 1429934331115212841:
            role = nextcord.utils.get(guild.roles, name = "QA")
            await member.remove_roles(role)
    '''
async def setup(bot):
    bot.add_cog(Events(bot))
import nextcord
from nextcord.ext import commands
from nextcord.ext import tasks
from nextcord.member import Member

# To do. Nextcord(finish course) and then work on setting up chafe gaem.

#Cog Syntax:
class CogName(commands.Cog):
    #initialize MyCog class..Don't have to redo bot and intents stuff.
    def __init__(self,bot): #not async
        self.bot = bot
#setup done outside the class
async def setup(bot):
    bot.add_cog(CogName(bot))
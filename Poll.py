import discord
from discord.ext import commands
from discord.ext import tasks
from discord.member import Member

#Cog Syntax:
class Poll(commands.Cog):
    #initialize MyCog class..Don't have to redo bot and intents stuff.
    def __init__(self,bot): #not async
        self.bot = bot
        self.numbers = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]

#setup done outside the class
async def setup(bot):
    await bot.add_cog(Poll(bot))
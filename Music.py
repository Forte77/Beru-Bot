import discord
from discord.ext import commands
from discord.ext import tasks
from discord.member import Member
# Need a join, leave, play, pause, skip, queue, and maybe move command
class Music(commands.Cog):
    #initialize Cog class..Don't have to redo bot and intents stuff.
    def __init__(self,bot): #not async
        self.bot = bot
    queueList = [] # Set these lists up
    deleteLater = [] # delete the songs after
    @commands.command() # Join VC
    async def join(self,ctx):
        if ctx.author.voice is None: # Make sure the user is in a VC
            await ctx.send("Join a VC first")
        else:
            channel = ctx.author.voice.channel
        if ctx.voice_client is not None: #if it's somewhere else. move.
            await ctx.voice_client.move_to(channel)
            print("moved and joined")
        else:
            await channel.connect() # connects to the vc
            print("joined")
    @commands.command() # Leave VC
    async def leave(self,ctx, help = "leaves the Voice Channel"):
        await ctx.voice_client.disconnect()
        print("leaving")
    #@commands.command() # Play a song
    #async def play(ctx):
    #    print("playing")
#Setup
async def setup(bot):
    await bot.add_cog(Music(bot))
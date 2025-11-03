import discord
from discord.ext import commands
from discord.ext import tasks
from discord.member import Member
from datetime import datetime
#Cog made while learning. MAY change the name of later.
class MyCog(commands.Cog):
    #initialize MyCog class
    def __init__(self,bot):
        self.bot = bot
        self._last_member = None
    
    @commands.Cog.listener() #Cog equivalent of Bot.listen
    async def on_member_join(self,member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Welcome {member.mention}.')
    @commands.Cog.listener()
    async def on_message(self,msg):
        if msg.content == "hello":
            await msg.channel.send("Hi!")
    @commands.command()
    async def yellow(self,ctx):
        await ctx.send("White!")
    @tasks.loop(seconds = 5) #this will run every 5 seconds
    async def task(self,ctx):
        await ctx.send("task")
    @commands.command()
    async def hello(self,ctx,*,member : discord.Member = None):
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f'Hello {member.name}~')
        else:
            await ctx.send(f'Hello again {member.name}!')
        self._last_member = member
    @tasks.loop(seconds=1)
    async def alarms(self,ctx,hour,minute):
        now = datetime.now().time()
        if now.hour ==hour and now.minute == minute:
            await ctx.author.create_dm()
            await ctx.author.dm_channel.send("It's time now!")
            self.alarms.stop()
    @commands.command()
    async def alarm(self,ctx,date,r=None):
        hour,minute = date.split(":")
        hour = int(hour)
        minute = int(minute)
        self.alarms.start(ctx,hour,minute)
        if r != None:
            await ctx.send("Alarm set. I'll dm you to "+r)
        else:
            await ctx.send("Alarm set. I'll dm you.")
    @alarm.error
    async def errorhandler(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument): # Check for a Missing Required Argument
            await ctx.send("Input an appropriate time for the alarm")
        if isinstance(error,commands.CommandInvokeError):
            await ctx.send("Only one alarm can be set")
        if isinstance(error,RuntimeError):
            await ctx.send("Only one alarm can be set")

    @commands.command()
    async def start(self,ctx):
        self.task.start(ctx)
    @commands.command()
    async def stop(self,ctx):
        self.task.stop()
        
async def setup(bot):
    await bot.add_cog(MyCog(bot))
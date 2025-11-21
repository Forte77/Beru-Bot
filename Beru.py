#import discord library
import discord
import string
with open('BotToken.txt','r') as file:
    token = file.read()
from discord.ext import commands
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix = "?", intents = intents,help_command=None)
#Coding commands not event. Command decorator calls a function. Event itself is a function
def is_me(ctx):
    return ctx.author.id == 300868241100636160
@bot.command() #ping command
async def ping(ctx): #Commmands use context parameter. I shortened to ctx
    await ctx.send("Pong!")
#Help/About command
@bot.command(aliases = ["about"])
async def help(ctx):
    #Building the help command in an embed.
    MyEmbed = discord.Embed(title = "Commands", description = "These are the available commands",color = discord.Colour.from_str(value= "#FFD700"))
    #settting the thumbnail for the embed to Zani
    MyEmbed.set_thumbnail(url="https://s3.getstickerpack.com/storage/uploads/sticker-pack/zani-day-at-work-and-abby/sticker_4.png?76f28757eea310fa122b44bc3d924cb7&d=200x200")
    #You can add 'inline = False' to make them display Vertically
    MyEmbed.add_field(name = "?alarm", value = "This command sets an alarm for a given time(24h) for only one server member(at the moment). If the hour is after Noon then add 12. Ex: hh:mm",inline = False)
    MyEmbed.add_field(name = "?battleship", value = "Start a game of battleship with another member. You can also choose the vertical and horizontal dimensions of the board. Ex: \n?battleship @friendo 5 5",inline = False)
    MyEmbed.add_field(name = "?choose4me", value = "This command will randomly select from a list of things. Activate the command and then put in the options one by one",inline = False)
    MyEmbed.add_field(name = "?creator", value = "Just pulls up contact information",inline = False)
    MyEmbed.add_field(name = "?luck", value = "This command flips a coin 3 times",inline = False)
    MyEmbed.add_field(name = "?ping", value = "This command replies back with Pong when used",inline = False)
    MyEmbed.add_field(name = "?poll", value = "This command creates a poll for [x] amount of minutes with the tile and options given. EX: **?poll 5 \"Amber checks DMs\" yes no sometimes rarely** This will create a 5 min poll with the title of Amber checks DMs with 4 different options.",inline = False)
    MyEmbed.add_field(name = "?rps [choice]", value = "This command lets you play Rock Paper Scissors. It does not allow non-classical answers.",inline = False)
    #Send embed that was built.
    await ctx.send(embed=MyEmbed)
@bot.command(aliases = ["contact","master"]) #Wanted to make a command to give contact info for me if I open this up to the public
async def creator(ctx):
     MyEmbed = discord.Embed(title="Contact Info",description= "Here is all thw ways you can reach me if there is a problem or you have questions about Beru.",color = discord.Colour.from_str(value= "#FFD700"))
     MyEmbed.set_thumbnail(url="https://s3.getstickerpack.com/storage/uploads/sticker-pack/zani-day-at-work-and-abby/sticker_4.png?76f28757eea310fa122b44bc3d924cb7&d=200x200")
     MyEmbed.add_field(name = "Email", value = "quantumforte7@gmail.com",inline=False)
     MyEmbed.add_field(name = "Discord", value = "forte.exe_xx",inline = False)
     MyEmbed.add_field(name = "Shameless Plug", value = "[My Twitch](https://twitch.tv/QuantumForte)",inline = False)
     await ctx.send(embed=MyEmbed)
@bot.command() # to unload extension
@commands.check(is_me)
async def unload(ctx,cogname):
    await bot.unload_extension(cogname)
@unload.error
async def errorhandler(ctx,error):
        if isinstance(error,commands.CheckFailure):
            await ctx.send("You're not my Master!")
@bot.command() # to reload an extension. can be used when when bot is already running
@commands.check(is_me)
async def reload(ctx,cogname):
    await bot.reload_extension(cogname)
    await ctx.send("Cog has been __Tactically__ Reloaded")
@reload.error
async def errorhandler(ctx,error):
        if isinstance(error,commands.CheckFailure):
            await ctx.send("You're not my Master!")
@bot.event #bot.event IS a function. bot.command() CALLS a function
async def on_ready():
    await bot.load_extension("Admin")
    await bot.load_extension("Cogs")
    await bot.load_extension("Events")
    await bot.load_extension("Misc")
    await bot.load_extension("Music")
    await bot.load_extension("Battleship")
    await bot.load_extension("Poll")
    print("Beru has been summoned.") 
bot.run(token) 
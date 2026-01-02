#import nextcord library
import nextcord
import string
from nextcord import application_command
from nextcord.ext import commands
from nextcord.ext import application_checks
from nextcord import Interaction
intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix = "?", intents = intents,help_command=None)
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
@bot.command() #ping command
async def ping(ctx): #Commmands use context parameter. Shortened to ctx
    await ctx.send("Pong!")
#Help/About command
@bot.group(aliases = ["about"],invoke_without_command=True)
async def help(ctx:commands.Context):
        #Building the help command in an embed.
        MyEmbed = nextcord.Embed(title = "Commands", description = "These are the available commands. For extra help with most commands use **?help [command name]**",color = nextcord.Colour(0xFFD700))
        #settting the thumbnail for the embed to Zani
        MyEmbed.set_thumbnail(url="https://s3.getstickerpack.com/storage/uploads/sticker-pack/zani-day-at-work-and-abby/sticker_4.png?76f28757eea310fa122b44bc3d924cb7&d=200x200")
        #You can add 'inline = False' to make them display Vertically
        MyEmbed.add_field(name = "?alarm", value = "This command sets an alarm for a given time(24h) for only one server member at a time.",inline = False)
        MyEmbed.add_field(name = "?battleship", value = "Start a game of battleship with another member. You can also choose the vertical and horizontal dimensions of the board. Ex: \n?battleship @friendo 5 5",inline = False)
        MyEmbed.add_field(name = "?choose4me", value = "This command will randomly select from a list of things. Activate the command and then put in the options one by one",inline = False)
        MyEmbed.add_field(name = "?creator", value = "Just pulls up contact information",inline = False)
        MyEmbed.add_field(name = "?luck", value = "This command flips a coin 3 times",inline = False)
        MyEmbed.add_field(name = "?ping", value = "This command replies back with Pong when used",inline = False)
        MyEmbed.add_field(name = "?poll", value = "This command creates a poll for [x] amount of minutes with the tile and options given.",inline = False)
        MyEmbed.add_field(name = "?rps [choice]", value = "This command lets you play Rock Paper Scissors. It does not allow non-classical answers. You must type rock paper or scissors as a response.",inline = False)
        #Send embed that was built.
        await ctx.send(embed=MyEmbed)
@help.command(name="alarm",description="More help with the alarm command")
async def alarm(ctx:commands.Context):
    MyEmbed = nextcord.Embed(title = "In-depth help for ?alarm", description = "Here is more info about the command.",color = nextcord.Colour(0xFFD700))
    MyEmbed.add_field(name= "Syntax:",value="?alarm [time] [reason for the alarm]\n You do not have to give a reason. The time must be formatted in hh:mm format(Military time). If you don't know what that means, if it it after noon then add 12 to the hour.")
    await ctx.send(embed=MyEmbed)
@help.command(name="battleship",description="More help with the battleship command")
async def battleship(ctx:commands.Context):
    MyEmbed = nextcord.Embed(title = "In-depth help for ?battleship", description = "Here is more info about the command.",color = nextcord.Colour(0xFFD700))
    MyEmbed.add_field(name= "Syntax:",value="?battleship [ping person to play with] [size of the board]\n If no size is given it will default to a 5x5. After the game begins you can use ?shoot and the coordinate you want to shoot at Ex:\n?shoot b3\nThe letter must go before the number.")
    await ctx.send(embed=MyEmbed)
@help.command(name="choose4me",description="More help with the chooose4me command")
async def choose4me(ctx:commands.Context):
    MyEmbed = nextcord.Embed(title = "In-depth help for ?choose4me", description = "Here is more info about the command.",color = nextcord.Colour(0xFFD700))
    MyEmbed.add_field(name= "Syntax:",value="?choose4me\nThis command prompts you to input your options. __DO NOT__ put any of your options surrounded by more or less than one \" on each side. This breaks the poll command and just doesn't work. I have no idea why, I could not fix it. Fuck Zytos.")
    await ctx.send(embed=MyEmbed)
@help.command(name="poll",description="More help with the poll command")
async def poll(ctx:commands.Context):
    MyEmbed = nextcord.Embed(title = "In-depth help for ?alarm", description = "Here is more info about the command.",color = nextcord.Colour(0xFFD700))
    MyEmbed.add_field(name= "Syntax:",value="?poll 5 \"Amber checks DMs\" yes no sometimes rarely\n This will create a 5 min poll with the title of *Amber checks DMs* with 4 different options. If one of your options contains more than one word it must be in quotations.\n__DO NOT__ put any of your options surrounded by more or less than one \" on each side. This breaks the command and just doesn't work. I have no idea why, I could not fix it. Fuck Zytos.")
    await ctx.send(embed=MyEmbed)
#Help command for admin commands
@bot.group(invoke_without_command=True) #don't have to use a subcommand
@commands.check(is_me)
async def adminhelp(ctx): #Moved to Beru because the help subcommand edit was not working if it had the same name as the other edit group command in Admin. Moving it here lets them both have the same name
    #Building the help command in an embed.
    MyEmbed = nextcord.Embed(title = "Admin Commands", description = "These are the available admin commands",color = nextcord.Colour(0xFFD700))
    #settting the thumbnail for the embed to Zani
    MyEmbed.set_thumbnail(url="https://s3.getstickerpack.com/storage/uploads/sticker-pack/zani-day-at-work-and-abby/sticker_4.png?76f28757eea310fa122b44bc3d924cb7&d=200x200")
    #You can add 'inline = False' to make them display Vertically
    MyEmbed.add_field(name = "?edit [...]", value = "This command is used to edit server information, channels, and roles. For more in-depth help type __?adminhelp edit__",inline = False) 
    MyEmbed.add_field(name = "?kick", value = "This command kicks the user",inline = False)
    MyEmbed.add_field(name = "?ban", value = "This command bans the user",inline = False)
    MyEmbed.add_field(name = "?purge", value = "This command purge's message by either amount or after a certain date. [dd mm yyyy]. For more in-depth help type __?adminhelp purge__")
    #MyEmbed.add_field(name = "?", value = "This command ",inline = False) keeping for copy and paste lol
    #Send embed that was built.
    await ctx.send(embed=MyEmbed)
@adminhelp.command()
async def edit(ctx):
    MyEmbed = nextcord.Embed(title = "Sub Commands", description = "These are the available sub commands and syntax",color = nextcord.Colour(0xFFD700))
    MyEmbed.add_field(name= "Syntax:",value="?edit [subcommand]\nEdit has multiple subcommands and does nothing by itself.",inline=False)
    MyEmbed.add_field(name= "servername:",value="?edit servername [new name]\nThis command changes the server's name to the input.",inline=False)
    MyEmbed.add_field(name= "createtextchannel:",value="?edit createtextchannel [channel name]\n his command creates a text channel with the name as input.",inline=False)
    MyEmbed.add_field(name= "createvoicechannel:",value="?edit createvoicechannel [channel name]\nThis command creates a voice channel with the name as input.",inline=False)
    MyEmbed.add_field(name= "createrole:",value="?edit createrole [role name]\nThis command creates a role with the name as input.",inline=False)
    MyEmbed.add_field(name= "assignrole:",value="?edit assignrole [member] [role name]\nThis command assigns a role to a given member. If the role is not created in the server it will create the role and then assign it. If the member already has the role it will be removed.",inline=False)
    await ctx.send(embed=MyEmbed)
@adminhelp.command()
async def purge(ctx):
    MyEmbed = nextcord.Embed(title = "Purge command", description = "This is how to use the Purge command.",color = nextcord.Colour(0xFFD700))
    MyEmbed.add_field(name= "Syntax:",value="?purge [amount] [day] [month] [year]\nPurge command deletes a specified number of messages or all messages after a given date. If you purge by date input a / instead of the amount number. The date must be separated by spaces and in a dd mm yyyy format. Bot has limits so if everything is not deleted then use the command again.",inline=False)
    await ctx.send(embed=MyEmbed)
@bot.command(aliases = ["contact","master"]) #Wanted to make a command to give contact info for me if I open this up to the public
async def creator(ctx):
    MyEmbed = nextcord.Embed(title="Contact Info",description= "Here is all thw ways you can reach me if there is a problem or you have questions about Beru.",color = nextcord.Colour(0xFFD700))
    MyEmbed.set_thumbnail(url="https://s3.getstickerpack.com/storage/uploads/sticker-pack/zani-day-at-work-and-abby/sticker_4.png?76f28757eea310fa122b44bc3d924cb7&d=200x200")
    MyEmbed.add_field(name = "Email", value = "quantumforte7@gmail.com",inline=False)
    MyEmbed.add_field(name = "nextcord", value = "forte.exe_xx",inline = False)
    MyEmbed.add_field(name = "Shameless Plug", value = "[My Twitch](https://twitch.tv/QuantumForte)",inline = False)
    await ctx.send(embed=MyEmbed)
@bot.command() # to unload extension
@commands.check(is_me)
async def unload(ctx,cogname):
    await bot.unload_extension(cogname)
    await ctx.send("Cog has been __Tactically__ Unloaded")
@unload.error
async def errorhandler(ctx,error):
    if isinstance(error,commands.CheckFailure):
        await ctx.send("You're not my Master!")
@bot.command() # to reload an extension. can be used when when bot is already running
@commands.check(is_me)
async def reload(ctx,cogname):
    print("Reload?")
    bot.reload_extension(cogname)
    print("yes")
    await ctx.send("Cog has been __Tactically__ Reloaded")
@reload.error
async def errorhandler(ctx,error):
        if isinstance(error,commands.CheckFailure):
            await ctx.send("You're not my Master!")
@bot.command()
async def feedback(ctx:nextcord.Member,*,feedback:str):
    await ctx.message.delete()
    if feedback == None:
        await ctx.send("Please type some thing as feedback")
        return
    await ctx.send("Sending your feeback to my Master...\nThank you")
    print(feedback)
    me = bot.get_user(own) or await bot.fetch_user(own)
    await me.send(f"# Feedback Incoming:\n{feedback}")
    await ctx.author.send("__Your feedback has been sent.__")
@bot.command() # Reload slash commands
@commands.check(is_me)
async def refresh(ctx): #Doing this on_ready uses up rate limit for the API
    await ctx.message.delete()
    try: #Slash commands
        await bot.sync_all_application_commands() #have to create slash command and then sync to bot to update it. Going to sync on ready for now
        print(f"Command(s) have been synced")
    except Exception as e:
        print(e)
    finally:
        print("Beru has been refreshed.")
@bot.slash_command(name="hello",description="Have Beru say hellow to you.")
async def hello(interaction:nextcord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention}!",ephemeral=True)
@bot.slash_command(name="say",description="Tell Beru what to say.") #fun little thing for me to play around with
@application_checks.check(is_me)
async def say(interaction:nextcord.Interaction,thing_to_say:str):
    await interaction.response.send_message(f"{interaction.user.name} said: '{thing_to_say}'",ephemeral=False)
@say.error
async def errorhandler(ctx:nextcord.Interaction,error):
        if isinstance(error,nextcord.errors.ApplicationCheckFailure):
            await ctx.send("You're not my Master!")
@bot.slash_command(name="botcommands",description="Gives info about each of the commands")
async def botcommands(interaction:nextcord.Interaction):
    #Building the help command in an embed.
    MyEmbed = nextcord.Embed(title = "Commands", description = "These are the available commands. For extra help with most commands use **?help [command name]**",color = nextcord.Colour(0xFFD700))
    #Settting the thumbnail for the embed to Zani
    MyEmbed.set_thumbnail(url="https://s3.getstickerpack.com/storage/uploads/sticker-pack/zani-day-at-work-and-abby/sticker_4.png?76f28757eea310fa122b44bc3d924cb7&d=200x200")
    #You can add 'inline = False' to make them display Vertically
    MyEmbed.add_field(name = "?alarm", value = "This command sets an alarm for a given time(24h) for only one server member at a time.",inline = False)
    MyEmbed.add_field(name = "?battleship", value = "Start a game of battleship with another member. You can also choose the vertical and horizontal dimensions of the board. Ex: \n?battleship @friendo 5 5",inline = False)
    MyEmbed.add_field(name = "?choose4me", value = "This command will randomly select from a list of things. Activate the command and then put in the options one by one",inline = False)
    MyEmbed.add_field(name = "?creator", value = "Just pulls up contact information",inline = False)
    MyEmbed.add_field(name = "?luck", value = "This command flips a coin 3 times",inline = False)
    MyEmbed.add_field(name = "?ping", value = "This command replies back with Pong when used",inline = False)
    MyEmbed.add_field(name = "?poll", value = "This command creates a poll for [x] amount of minutes with the tile and options given.",inline = False)
    MyEmbed.add_field(name = "?rps [choice]", value = "This command lets you play Rock Paper Scissors. It does not allow non-classical answers. You must type rock paper or scissors as a response.",inline = False)
    #Send embed that was built.
    await interaction.response.send_message(embed=MyEmbed)
@bot.slash_command(name="help", description="Get more info on certain commands")
async def help(interaction: nextcord.Interaction):
    pass
@help.subcommand(description="More in-depth help on the alarm command")
async def alarm(interaction: nextcord.Interaction):
    MyEmbed = nextcord.Embed(title = "In-depth help for ?alarm", description = "Here is more info about the command.",color = nextcord.Colour(0xFFD700))
    MyEmbed.add_field(name= "Syntax:",value="?alarm [time] [reason for the alarm]\n You do not have to give a reason. The time must be formatted in hh:mm format(Military time). If you don't know what that means, if it it after noon then add 12 to the hour.")
    await interaction.response.send_message(embed=MyEmbed)
@help.subcommand(description="More in-depth help on the battleship command")
async def battleship(interaction: nextcord.Interaction):
    MyEmbed = nextcord.Embed(title = "In-depth help for ?battleship", description = "Here is more info about the command.",color = nextcord.Colour(0xFFD700))
    MyEmbed.add_field(name= "Syntax:",value="?battleship [ping person to play with] [size of the board]\n If no size is given it will default to a 5x5. After the game begins you can use ?shoot and the coordinate you want to shoot at Ex:\n?shoot b3\nThe letter must go before the number.")
    await interaction.response.send_message(embed=MyEmbed)
@help.subcommand(description="More in-depth help on the choose4me command")
async def choose4me(interaction: nextcord.Interaction):
    MyEmbed = nextcord.Embed(title = "In-depth help for ?choose4me", description = "Here is more info about the command.",color = nextcord.Colour(0xFFD700))
    MyEmbed.add_field(name= "Syntax:",value="?choose4me\nThis command prompts you to input your options. __DO NOT__ put any of your options surrounded by more or less than one \" on each side. This breaks the poll command and just doesn't work. I have no idea why, I could not fix it. Fuck Zytos.")
    await interaction.response.send_message(embed=MyEmbed)
@help.subcommand(description="More in-depth help on the poll command")
async def poll(interaction: nextcord.Interaction):
    MyEmbed = nextcord.Embed(title = "In-depth help for ?alarm", description = "Here is more info about the command.",color = nextcord.Colour(0xFFD700))
    MyEmbed.add_field(name= "Syntax:",value="?poll 5 \"Amber checks DMs\" yes no sometimes rarely\n This will create a 5 min poll with the title of *Amber checks DMs* with 4 different options. If one of your options contains more than one word it must be in quotations.\n__DO NOT__ put any of your options surrounded by more or less than one \" on each side. This breaks the command and just doesn't work. I have no idea why, I could not fix it. Fuck Zytos.")
    await interaction.response.send_message(embed=MyEmbed)
@bot.event #bot.event IS a function. bot.command() CALLS a function
async def on_ready():
    bot.load_extension("Admin")
    bot.load_extension("Cogs")
    bot.load_extension("Events")
    bot.load_extension("Misc")
    bot.load_extension("Battleship")
    bot.load_extension("Poll")
    bot.load_extension("Rogues")
    print("Beru has been summoned")
bot.run(token) 
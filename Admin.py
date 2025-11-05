import discord
from discord.ext import commands
from discord.ext import tasks
from discord.member import Member
from datetime import datetime
def is_me(ctx):
    return ctx.author.id == 300868241100636160
class Admin(commands.Cog):
    #initialize Admin class
    def __init__(self,bot): #not async
        self.bot = bot
    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def purge(self,ctx, amount, day : int = None, month : int = None, year : int = datetime.now().year): #options to input date for the purging
        if amount == "/":
            if day == None or month == None:
                return
            else:
                await ctx.channel.purge(after = datetime(year,month,day))
        else:
            await ctx.channel.purge(limit = int(amount)+1)
    @purge.error
    async def errorhandler(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("Enter how many messages to purge.")
        if isinstance(error,commands.CommandInvokeError):
            await ctx.send("You can only have a slash or a number as the first input")
    #Help command for admin commands
    #@commands.command()
    async def adminhelp(self,ctx):
        #Building the help command in an embed.
        MyEmbed = discord.Embed(title = "Commands", description = "These are the available commands",color = discord.Colour.from_str(value= "#FFD700"))
        #settting the thumbnail for the embed to Zani
        MyEmbed.set_thumbnail(url="https://s3.getstickerpack.com/storage/uploads/sticker-pack/zani-day-at-work-and-abby/sticker_4.png?76f28757eea310fa122b44bc3d924cb7&d=200x200")
        #You can add 'inline = False' to make them display Vertically
        MyEmbed.add_field(name = "?edit [...]", value = "This command is used to edit server information, channels, and roles.",inline = False) 
        MyEmbed.add_field(name = "?kick", value = "This command kicks the user",inline = False)
        MyEmbed.add_field(name = "?ban", value = "This command bans the user",inline = False)
        MyEmbed.add_field(name = "?purge", value = "This command purge's message by either amount or after a certain date. [dd/mm/yyyy]")
        #MyEmbed.add_field(name = "?", value = "This command ",inline = False)
        #Send embed that was built.
        await ctx.send(embed=MyEmbed)
    #Creating nested functions/sub commands
    @commands.group() #allows nested subcommands into main command
    @commands.check(is_me)
    async def edit(self,ctx): #does nothing but is the main command
        pass
    #sub command *,input == input+ in dyno
    @edit.command()
    async def servername(self,ctx,*,input): #change server name
        await ctx.guild.edit(name = input)
    @edit.command()
    async def createtextchannel(self,ctx,*,input):
        await ctx.guild.create_text_channel(name = input)
    @edit.command()#check api doc for more customization
    async def createvoicechannel(self,ctx,*,input):
        await ctx.guild.create_voice_channel(name = input)
    @edit.command() # I believe this one is obsolete but my course covered it so here it is.
    async def rtc_region(self,ctx,*,input): #change server region
        await ctx.VoiceChannel.edit(rtc_region = input)
    @edit.command()
    async def createrole(self,ctx,*,input):
        await ctx.guild.create_role(name = input)
        await ctx.send("The role has been created")
    @edit.command()
    async def assignrole(self,ctx,member : discord.Member,*,input):
        role = input
        print(role)
        guild = self.bot.get_guild(member.guild.id)
        trole = discord.utils.get(guild.roles, name = input) #checking each role in the server to see if the one we need to use has been made already
        if not trole == None:
            rolename = trole.name
            print(trole.name+".\n")
            if role == rolename:
                print(role + " == "+ rolename + " Role identified")
                ID = trole.id 
                if member.get_role(ID) == None:
                    await member.add_roles(trole)
                    await ctx.send("User has been given the " + rolename + " role.")
                    return
                else:
                    await ctx.send("User already has this role")
                    return
        else:
            self.bot.get_command('createrole')
            await self.createrole(ctx,input=input) #creates the role if not found
            role = discord.utils.get(guild.roles, name = input)
            await member.add_roles(role) #Then adds it to the user.
    @edit.error # Error handler. Syntax is @[command name].error
    async def errorhandler(self,ctx,error): # Error handlers need ctx and the error
        if isinstance(error,commands.CheckFailure): # Check for a specific error that is expected to pop up.
            await ctx.send("You're not my Master!") # Do something else instead of crashing

    @commands.command()
    @commands.has_role("gamer")
    async def kick(self,ctx,member : discord.Member,*,reason = None):#converts string member into the discord Member object
        await ctx.guild.kick(member, reason = reason)
    @kick.error
    async def errorhandler(self,ctx,error):
        if isinstance(error,commands.MissingRole):
            await ctx.send("You're not approved by my Master!")
    @commands.command()
    @commands.has_role("gamer")
    async def ban(self,ctx,member : discord.Member,*,reason = None):
        await ctx.guild.ban(member, reason = reason)
        await ctx.send(member.name + " has been banned")
    @ban.error
    async def errorhandler(self,ctx,error):
        if isinstance(error,commands.MissingRole):
            await ctx.send("You're not approved by my Master!")
    @commands.command() #Mute user
    @commands.has_role("gamer")
    async def mute(self,ctx,user : discord.Member):
        await user.edit(mute = True)
    @mute.error
    async def errorhandler(self,ctx,error):
        if isinstance(error,commands.MissingRole):
            await ctx.send("You're not approved by my Master!")
    @commands.command() #Unmute
    @commands.has_role("gamer")
    async def unmute(self,ctx,user : discord.Member):
        await user.edit(mute = False)
    @unmute.error
    async def errorhandler(self,ctx,error):
        if isinstance(error,commands.MissingRole):
            await ctx.send("You're not approved by my Master!")
    @commands.command() #Deafen
    @commands.has_role("gamer")
    async def deafen(self,ctx,user : discord.Member):
        await user.edit(mute = True)
    @deafen.error
    async def errorhandler(self,ctx,error):
        if isinstance(error,commands.MissingRole):
            await ctx.send("You're not approved by my Master!")
    @commands.command() #Undeafen command
    @commands.has_role("gamer")
    async def undeafen(self,ctx,user : discord.Member):
        await user.edit(mute = False)
    @undeafen.error
    async def errorhandler(self,ctx,error):
        if isinstance(error,commands.MissingRole):
            await ctx.send("You're not approved by my Master!")
    @commands.command() #Kick from a VC
    @commands.has_role("gamer")
    async def voicekick(self,ctx,user : discord.Member):
        await user.edit(voice_channel= None)
    @voicekick.error
    async def errorhandler(self,ctx,error):
        if isinstance(error,commands.MissingRole):
            await ctx.send("You're not approved by my Master!")
    @commands.command()
    @commands.check(is_me)
    async def unban(self,ctx,*,input):
        if "#" in input:
            name, discriminator = input.split("#") #in case anyone is using an older style discord username
        else:
            name = input
            discriminator = None
        async for entry in ctx.guild.bans(limit=150): #grabs and goes through list of banned people
            username = entry.user.name
            if not discriminator == None:
                disc = entry.user.discriminator
            else:
                disc = None
            if name == username and discriminator == disc:
                await ctx.guild.unban(entry.user)
                await ctx.send(input + " has been unbanned")
    @unban.error
    async def errorhandler(self,ctx,error):
        if isinstance(error,commands.CheckFailure):
            await ctx.send("You're not my Master!")
        
#setup done outside the class
async def setup(bot):
    await bot.add_cog(Admin(bot))
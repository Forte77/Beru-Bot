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
    @commands.command()
    async def poll(self, ctx, minutes : int,title,*options):
        if len(options) == 0: # checking if there are options given and if not then assume a yes or no type.
            pollEmbed = discord.Embed(title = title, description = f"You have **{minutes}** minutes remaining!") # Make embed
            msg = await ctx.send(embed = pollEmbed)
            await msg.add_reaction("👍")
            await msg.add_reaction("👎")
        else:
            pollEmbed = discord.Embed(title = title, description = f"You have **{minutes}** minutes remaining!") # Reminder that all embeds take a title & description
            for number,option in enumerate(options): # enumerate returns the numbered index and the item
                pollEmbed.add_field(name = f"{self.numbers[number]}", value = f"**{option}**", inline = False)
            msg = await ctx.send(embed = pollEmbed)
            for x in range(len(pollEmbed.fields)): # adding numbered reactions for each item
                await msg.add_reaction(self.numbers[x])
        self.poll_loop.start(ctx,minutes,title,options,msg)
    @tasks.loop(minutes = 1)
    async def poll_loop(self, ctx, minutes, title, options, msg):
        count = self.poll_loop.current_loop
        remaining_time = minutes - count
        newEmbed = discord.Embed(title = title, description = f"You have **{remaining_time}** minutes left!")
        for number,option in enumerate(options): # enumerate returns the numbered index and the item
            newEmbed.add_field(name = f"{self.numbers[number]}", value = f"**{option}**", inline = False)
        await msg.edit(embed = newEmbed)
        #before this point the message is not properly cached so we can not see the amount of emojis
        if remaining_time == 0:
            self.poll_loop.stop()
            counts = []
            msg = discord.utils.get(self.bot.cached_messages, id = msg.id)
            reactions = msg.reactions
            for reaction in reactions: #going through all reactions and getting how many
                counts.append(reaction.count)
            max_value = max(counts)
            print(self.poll_loop.is_running())
            i = 0 
            for count in counts:
                if count == max_value:
                    i = i+1
            if i>1:
                await ctx.send("It's a Draw")
            else:
                max_index = counts.index(max_value)
                if len(options) == 0:
                    winEmoji = reactions[max_index]
                    await ctx.send("Time's Up!")
                    if winEmoji.emoji == "👍":
                        await ctx.send("### The people have spoken\nThe people have agreed!")
                    if winEmoji.emoji == "👎":
                        await ctx.send("### The people have spoken\nThe people have disagreed!")
                else:
                    winner = options[max_index]
                    winEmoji = reactions[max_index]
                    await ctx.send("## Time's Up!")
                    await ctx.send(f"{winEmoji.emoji} **{winner}** has won the Poll!")
        
    @poll.error
    async def errorhandler(self,ctx,error):
        if isinstance(error,commands.errors.BadArgument):
            await ctx.send("The usage of this command was invalid. Reminder that the poll command goes like this:\n?poll [minutes] \"[Question in quotes]\" [options for the poll separated by spaces]\nIf your options are multiple words then put them in quotes and space them.")
#setup done outside the class
async def setup(bot):
    await bot.add_cog(Poll(bot))
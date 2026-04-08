import asyncio
import nextcord
import random
import string
from nextcord.ext import commands
from datetime import datetime
from nextcord.ext import tasks
from nextcord.member import Member
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
class Misc(commands.Cog):
    def __init__(self,bot): #not async
        self.bot = bot
    @commands.command()
    async def choose4me(self,ctx):
        i = 0
        done = False
        await ctx.channel.send("What do you need help chooseing between?\nType your first option:") # Prompt the user to enter options
        options = []
        while (done == False):
            done = await self.choose(ctx,done,options,i)
            i +=1 # Update i
            print (i)
            if done:
                continue
        await ctx.channel.purge(limit = i*2)
        opt = random.randint(1,i) # Randomize choices
        pick = options[opt-1] # Get the choice that was at that random selection.
        print(options)
        try:
            await ctx.channel.send(f"You should do:\n" + pick)
        except TypeError:
            await ctx.channel.send(f"Invalid input. Please run the command again... but better this time.")
    async def choose(self,ctx,done,options,i):
        def check(message): # Get the user
            return message.author == ctx.author and message.channel == ctx.channel # Check the message is a valid response from the right person in the right channel
        try:
            msg = await self.bot.wait_for('message',check=check,timeout=30.0) # Wait 30 seconds
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond! Finish thinking about the options and restart.")
            return True
        else:
            #print(msg.content)
            if (msg.content == "done"):
                #print("done test at ",i)
                return True
            options.append(msg.content) # Add to the list of options
            if (i < 1):
                await ctx.channel.send(f"Alright type your second option.") # Prompt option #2
                return False
            await ctx.channel.send(f"Ok type your next option or type \"done\" if you have no more.") # Response for all
            return False
    @commands.command()
    async def laugh(self,ctx):
        await ctx.channel.purge(limit = 1)
        funnies = ["https://cdn.nextcordapp.com/attachments/681684835513008280/1433133633245286521/cf2fb2ea0e790e25ff1e936fd9c1dd93.mp4?ex=69039534&is=690243b4&hm=870f12d87f2d0564b411fc0df5db30335595455bc1b6ff714e2e3193de659135&","https://www.instagram.com/reel/DQJQzTPDvEx/?igsh=Ym11OTA2OWg0aTRl"]
        link = random.randint(1,2)
        await ctx.channel.send(f"Here's something that might give you a laugh:\n"+funnies[link-1])
    @commands.command()
    async def shadow(self,ctx):# Stream redeem shadow did on 2.2.26
        cool = ["Shadowzero","Zytos"]
        coolest = random.choice(cool)
        await ctx.send(f"The coolest shadow is: {coolest}")
    @commands.command() # command for my own use lol
    @commands.check(is_me)
    async def justdoit(self,ctx):
        await ctx.channel.purge(limit = 1)
        task = ["Japanese","Coding","Sprites","Twitch stuff","Job stuff"]
        japanese = ["Short quiz","Long quiz","Umi Lesson","Umi review"]
        review = ["review","speak","listen","blitz"]
        coding = ["Lua","nextcord Bot","Hackerrank"]
        work = random.choice(task)
        match(work):
            case "Sprites":
                await ctx.send("Your chosen task is: " + work +"\nGet back on that grind and start the BN4 pack.")
            case "Coding":
                await ctx.send("Your chosen task is: " + work)
                work1 = random.choice(coding)
                #await ctx.send("https://www.udemy.com/home/my-courses/learning/")
                match (work1):
                    case "Lua":
                        await ctx.send("Pick the Lua course back up. Almost done")
                    case "nextcord Bot":
                        await ctx.send("Work on the game.")
                    case "Hackerrank":
                        await ctx.send("Do hackerrank things")
                    case _:
                        await ctx.send("Do "+ work1)
            case "Japanese":
                work2 = random.choice(japanese)
                await ctx.send("Your chosen task is: " + work +" today!\n"+"Specifically doing a: "+work2)
                match (work2):
                    case "Short quiz":
                        await ctx.send("Do some short quizzes\nhttps://kana-quiz.tofugu.com/ \nInvite Zach or Rizen. Alternate doing quizzes for Hiragana and Katakana.\nDo at LEAST 4 Quizzes total; so 2 Hiragana and 2 Katakana.")
                    case "Long quiz":
                        await ctx.send("Do a couple long quizzes. 1 Hiragana and 1 Katakana\nhttps://realkana.com/hiragana \nCheck off all single,double(and extended for katakana) character boxes for each language and all fonts. Don't do any word packs unless you have a lot of free time.\n**Uncheck** __\"Continuous Play\"__ and __\"Repeat Problem Kana\"__")
                    case "Umi Lesson":
                        await ctx.send("Do your next lesson in Umi.")
                    case "Umi review":
                        work3 = random.choice(review)
                        match(work3):
                            case "review":
                               await ctx.send("Go do the "+work3+" part of your Umi reviews")
                            case "speak":
                                await ctx.send("Go do the "+work3+" part of your Umi reviews")
                            case "listen":
                                await ctx.send("Go do the "+work3+" part of your Umi reviews")
                            case "blitz":
                                await ctx.send("Go do the "+work3+" part of your Umi reviews")
                            case _:
                                await ctx.send("Do "+work3)
                    case _:
                        await ctx.send("Do "+work2)
            case _:
                await ctx.send("Do "+work)
    @justdoit.error
    async def errorhandler(self,ctx,error):
        if isinstance(error,commands.CheckFailure):
            await ctx.send("You're not my Master!")
    #Flip a coin Command
    @commands.command()
    async def luck(self,ctx): 
        for i in range(3):
            num = random.randint(1,2)
            if num == 1:
                await ctx.send("Heads!")
            if num == 2:
                await ctx.send("Tails!")
    #Rock Paper Scissors Command
    @commands.command()
    async def rps(self,ctx, hand = None): #second parameter is what else is in the message.
        hands =["🪨","📜","✂️"]
        bothand = random.choice(hands)
        if hand == None:
            await ctx.send("At least throw something out.")
        else:
            player = hand.lower()
        await ctx.send(bothand)
        if bothand == "🪨":
            bothand = "rock"
        if bothand == "📜":
            bothand = "paper"
        if bothand == "✂️":
            bothand = "scissors"
        if player == bothand:
            await ctx.send("It's a draw! Try again?")
        elif player == "scissors" :
            if bothand == "rock":
                await ctx.send("You lose. Better luck next time!")
            if bothand == "paper":
                await ctx.send("You Win!")
        elif player == "paper":
            if bothand == "rock":
                await ctx.send("You Win!")
            if bothand == "scissors":
                await ctx.send("You lose. Better luck next time!")
        elif player == "rock":
            if bothand == "scissors":
                await ctx.send("You Win!")
            if bothand == "paper":
                await ctx.send("You lose. Better luck next time!")
        else:
            await ctx.send("Come on use the real choices. No Volcanoes, Guns, etc. please.")
    @rps.error
    async def errorhandler(self,ctx,error):
        if isinstance(error,UnboundLocalError):
            await ctx.send("Invalid. Be better")
async def setup(bot):
    bot.add_cog(Misc(bot))
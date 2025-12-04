import nextcord
from nextcord.ext import commands
from nextcord.ext import tasks
from nextcord.member import Member
from nextcord import Interaction
from nextcord import application_command
from nextcord.ext import application_checks
free = True
# Need a function to check if there is a game running already
def ongoing(free):
    return free == True
#Cog Syntax:
class Rogues(commands.Cog):
    #initialize MyCog class..Don't have to redo bot and intents stuff.
    def __init__(self,bot): #not async
        self.bot = bot
    @nextcord.slash_command()
    @application_checks.check(ongoing)
    async def RogueGame(self,interaction:nextcord.Interaction): #function to start the game
        free = False # set the free check to false since the game has started
    def Deck(self): #create the "deck" of spells for the dungeon
        #gotta finish spell class first
        print("Creating Deck")
        #I'm thinking use deck command to make each spell and the spell class takes the variables to initialize them

class Player:
    name="player"
    uid=1
    health = 3
    shield = 0
    prevRoom = None
    nextRoom = None
    hand = [None,None,None,None,None] # Players can hold a max of 5 spells
    Rogue = False
    def __init__(self,interaction:nextcord.Interaction):
        name = interaction.user.name

class Spell: #This will all be internal. No player interaction to create spells for the game.
    spellName = ""
    spellType = "" # Off Def Anc
    counter = True # Whether it can be countered
    block = True # Whether it can be blocked
    avoid = True # Whether it can be avoided
    copy = 1 # will increment with each spell that is created under the same name
    count = 3 # How many are in the deck total. This variable will be different for the different named spells but not change beyond that.
    aim = False # Need to make a use command and prompt user for a target if this is ever true
    def __init__(self,name,stype,counter,block,avoid,copy,count):
        self.spellName = name
        self.spellType = stype
        self.counter = counter
        self.block = block
        self.avoid = avoid
        self.copy = copy
        self.count = count

#setup done outside the class
async def setup(bot):
    bot.add_cog(Rogues(bot))

# Notes:
# Need to make a tear down command at the end of all of this to wipe everything
# Player commands to check their stats
# Implement bot creating a text channel for dungeon and VCs for each room. Thinking to create a category for the game that the bot can then delete afterwards.
# Current idea is to have deck command make all the spells and for the ones with multiple counts to be done in a loop, that way I can pass the appropriate copy number.
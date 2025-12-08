import nextcord
from nextcord.ext import commands
from nextcord.ext import tasks
from nextcord.member import Member
from nextcord import Interaction
from nextcord import application_command
from nextcord.ext import application_checks
from nextcord import ApplicationCommandOptionType
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
ready = True
deck = []
evil = False
# Need a function to check if there is a game running already
def ongoing(ready):
    return ready == False
class Rogues(commands.Cog):
    #initialize MyCog class..Don't have to redo bot and intents stuff.
    def __init__(self,bot): #not async
        self.bot = bot
    def Deck(self): #create the "deck" of scrolls for the dungeon
        #gotta finish scroll class first
        print("Creating Deck")
        self.createScroll("Wish","Ancillary",False,False,False,1,"") # TBD
        self.createScroll("Za Warudo","Ancillary",False,False,False,1,"") # when prompting defensive scrolls need to also check for this.
        self.createScroll("Soul Knot","Ancillary",False,False,False,1,"") # Link to another player when one dies the other dies but if they are both the only two to get out then they both win.
        self.createScroll("Holy Shield","Defensive",False,False,False,1,"") # Super Strong long lasting shield. numbers will be worked out later
        self.createScroll("Teleport","Defensive",False,False,False,6,"") # 6 teleport scrolls it can not be countered blocked or avoided (it's an attack or aimed at anyone)
        self.createScroll("Fireball","Offensive",True,True,True,7,"") # 7 Fireball can be countered blocked and avoided
        self.createScroll("Counter","Defensive",False,True,True,7,"") # Counter spell can be blocked and avoided but not countered
        self.createScroll("Mold Earth","Defensive",False,False,False,3,"") # Covers two players
        self.createScroll("Eldritch Blast","Offensive",True,True,False,5,"") # Can't be avoided
        self.createScroll("Call Lightning","Offensive",False,True,True,5,"") # Can't be countered
        self.createScroll("Dragon Breath","Offensive",True,False,True,5,"") # Can't be blocked
        self.createScroll("Scrying","Ancillary",False,False,False,4,"") # The target chooses which scroll to show
        self.createScroll("Divine Wisdom","Ancillary",False,False,False,3,"") # Reveal all scrolls of one chosen player to the user
        self.createScroll("Barbarian Rage","Defensive",False,False,False,3,"") # Blocks TWO instances of damage
        self.createScroll("Polymorph","Ancillary",True,False,False,2,"") # Prevent another player from taking action twice CAN only be countered.
        self.createScroll("Invisibility","Defensive",False,False,False,3,"") # When used as a reaction can not be used to avoid single target scroll but can be used to dodge multi target. Rogues have extra perks with invis
        self.createScroll("Magic Shield","Defensive",False,False,False,6,"") # Blocks a spell
        self.createScroll("Cure Wounds","Defensive",False,False,False,4,"") # heal
        if evil == True:
            self.createScroll("Steal","Offensive",False,False,True,4,"") # TBD
            self.createScroll("Blood Altar","Offensive",False,False,False,3,"") # Sap Health if uninterupted. Won't heal if it is CBA
        sn = 0 
        for i in deck:
            self.serialize(i,sn) # Add serial number to the Scrolls to further help keep track of.
            sn +=1
        print("Deck created")
    def createScroll(self,name,type,counter,block,avoid,count,flavor="If you see this I fucked up"): # Function to create scrolls for the game
        i = 0
        global deck
        while (i < count):
            deck.append(Scroll(name,type,counter,block,avoid,i+1,count,flavor)) # Create Scroll and add it to the deck
            i+=1
    def serialize(self,scroll,sn):
        scroll.serial = sn
    @commands.command()
    @commands.check(is_me)
    async def printDeck(self,ctx):
        if ready == True:
            ctx.send("No deck to print")
            return
        for i in deck:
            i.toPrint()
        #I'm thinking use deck command to make each scroll and the scroll class takes the variables to initialize them

    @nextcord.slash_command(name="rogues",description="Start the game")
    async def RogueGame(self,interaction:nextcord.Interaction): #function to start the game
        global ready
        if ready==False:
            interaction.response.send_message("A game has already started")
            return
        ready = False # set the ready check to false since the game has started
        await interaction.response.send_message("Setting up Game...")
        self.Deck()
    @nextcord.slash_command(name="cleared",description="End the game")
    @application_checks.check(ongoing)
    async def cleared(self,interaction:nextcord.Interaction):
        global ready
        ready = True # set the ready check to false since the game has started
        await interaction.response.send_message("Shutting down Game...")
        
class Player:
    name="player"
    uid=1
    hp = 3
    shield = 0
    pRoom = None
    nRoom = None
    hand = [None,None,None,None,None] # Players can hold a max of 5 scrolls
    Rogue = False
    done = False
    mem = nextcord.Member
    reacting = False
    def __init__(self,interaction:nextcord.Interaction):
        name = interaction.user.name
    @application_checks.check(ongoing)
    @nextcord.slash_command(name="player",description="Player commands during the game")
    async def player(self,interaction:nextcord.Interaction):
        pass
    @player.subcommand(description="Use one of your scrolls")
    async def use(self,interaction:nextcord.Interaction,scroll,target:None,target2:None):
        if target != None and target2 == None:
            scroll.action(target)
        elif target2 != None:
            scroll.action(target,target2)
        else:
            scroll.action()
        await interaction.response.send_message("done")
    @player.subcommand(description="Show another player one of your scrolls")
    async def show(self,interaction:nextcord.Interaction,scroll,target:None):
        print("Player is showing their scroll.")
        await interaction.response.send_message("done")
    @player.subcommand(description="Duel another player")
    async def duel(self,interaction:nextcord.Interaction,target):
        print("Player wants to duel")
        await interaction.response.send_message("done")

class Scroll: #This will all be internal. No player interaction to create scrolls for the game.
    scrollName = ""
    scrollType = "" # Off Def Anc
    counter = True # Whether it can be countered
    block = True # Whether it can be blocked
    avoid = True # Whether it can be avoided
    copy = 1 # will increment with each scroll that is created under the same name
    count = 3 # How many are in the deck total. This variable will be different for the different named scrolls but not change beyond that.
    aim = False # Need to make a use command and prompt user for a target if this is ever true
    serial = 0
    flavor = ""
    def __init__(self,name,stype,counter,block,avoid,copy,count,flavor):
        self.scrollName = name
        self.scrollType = stype
        self.counter = counter
        self.block = block
        self.avoid = avoid
        self.copy = copy
        self.count = count
        self.flavor = flavor
    def toPrint(self):
        print(f"{self.scrollName}. Type: {self.scrollType}. Serial Number: {self.copy}. There are {self.count} total in the dungeon.")
    async def action(self,interaction:nextcord.Interaction,target:None,target2:None):
        match self.scrollName:
            case "Teleport":
                print("Player casted Teleport")
            case "Fireball":
                print("Player casted ")
            case "Counter":
                print("Player casted ")
            case "Mold Earth":
                print("Player casted ")
            case "Eldritch Blast":
                print("Player casted ")
            case "Call Lightning":
                print("Player casted ")
            case "Dragon Breath":
                print("Player casted ")
            case "Scrying":
                print("Player casted ")
            case "Divine Wisdom":
                print("Player casted ")
            case "Barbarian Rage":
                print("Player casted ")
            case "Polymorph":
                print("Player casted ")
            case "Invisibility":
                print("Player casted ")
            case "Magic Shield":
                print("Player casted ")
            case "Steal":
                print("Player casted ")
            case "Blood Altar":
                print("Player casted ")
            case "Cure Wounds":
                print("Player casted ")
            case "Holy Shield":
                print("Player casted ")
            case "Soul Knot":
                print("Player casted ")
            case "Wish":
                print("Player casted ")
            case "Za Warudo":
                print("Player casted ")
            case _: #Default
                interaction.response.send_message("That was not a valid name for a scroll.",ephemeral=True)

#setup done outside the class
async def setup(bot):
    bot.add_cog(Rogues(bot))
# Notes:
# Need to make a tear down command at the end of all of this to wipe everything
# Player commands to check their stats
# Implement bot creating a text channel for dungeon and VCs for each room. Thinking to create a category for the game that the bot can then delete afterwards.
# Current idea is to have deck command make all the scrolls and for the ones with multiple counts to be done in a loop, that way I can pass the appropriate copy number.
# Each scroll will just be a function in the scroll class
# When dealing with Rooms make an exit check that will happen each time a room has been entered by a player
# Need to make A LOT OF CHECKS primarily to see if a player has a spell(and which copy) in their hand
# Make a removeShields function for when the floor advances.
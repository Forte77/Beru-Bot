import nextcord
import asyncio
import random
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
players = []
# Need a function to check if there is a game running already
def ongoing(ready):
    return ready == False
class Rogues(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    async def make(self,interaction:nextcord.Interaction):
        try:
            global category
            category = await guild.create_category("Rogues Category")
            await interaction.send("Creating the category and channels. Please remember to have a moderator use the ?teardown command when the game is done.")
            print(f"Category {category.name} created successfully!")
            global safeRoom
            safeRoom = await guild.create_text_channel(name="safe-room",category=category,position=0,topic="Room for the party to discuss and make decisions",overwrites={everyone:nextcord.PermissionOverwrite(view_channel=False,read_messages=False,send_messages=False),playerRole:nextcord.PermissionOverwrite(view_channel=True,read_messages=True,send_messages=True)})
            await safeRoom.send("This looks like a safe spot.")
            global safeVC
            safeVC = await guild.create_voice_channel(name="Safe VC",category=category,overwrites={everyone:nextcord.PermissionOverwrite(view_channel=False,connect=False,read_messages=False,send_messages=False),playerRole:nextcord.PermissionOverwrite(view_channel=True,connect=True,read_messages=False,send_messages=False)})
        except Exception as e:
            print(f"An error occured: {e}")
    async def addPlayer(self,player:nextcord.Member,uid):
        match uid:
            case 1:
                await player.add_roles(playerRole)
                player1 = Player(player,uid)
                players.append(player1)
            case 2:
                await player.add_roles(playerRole)
                player2 = Player(player,uid)
                players.append(player2)
            case 3:
                await player.add_roles(playerRole)
                player3 = Player(player,uid)
                players.append(player3)
            case 4:
                await player.add_roles(playerRole)
                player4 = Player(player,uid)
                players.append(player4)
            case 5:
                await player.add_roles(playerRole)
                player5 = Player(player,uid)
                players.append(player5)
            case 6:
                await player.add_roles(playerRole)
                player6 = Player(player,uid)
                players.append(player6)
            case 7:
                await player.add_roles(playerRole)
                player7 = Player(player,uid)
                players.append(player7)
            case 8:
                await player.add_roles(playerRole)
                player8 = Player(player,uid)
                players.append(player8)
            case _:
                print("too many players")
    def Deck(self): #create the "deck" of scrolls for the dungeon
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
    def deal(self, player):
        print(f"Dealing to {player.name}:\n")
        for i in range(0,3): # Deal 3 scrolls at the start of the game
            dealt = random.choice(deck) # randomly pick a scroll
            deck.remove(dealt) # remove the scroll from the deck
            player.addScroll(dealt) # add the scroll to the player's hand
    @commands.command()
    @commands.check(is_me)
    async def printDeck(self,ctx):
        if ready == True:
            ctx.send("No deck to print")
            return
        for i in deck:
            i.toPrint()
        #I'm thinking use deck command to make each scroll and the scroll class takes the variables to initialize them
    
    @nextcord.slash_command(name="rogues",description="Start the game and select the players")
    async def RogueGame(self,interaction:nextcord.Interaction, #function to start the game
                        member1:nextcord.Member, # Members to be added to the game by the person who used the command.
                        member2:nextcord.Member = None, # Will make this required later
                        member3:nextcord.Member = None,
                        member4:nextcord.Member = None,
                        member5:nextcord.Member = None,
                        member6:nextcord.Member = None,
                        member7:nextcord.Member = None): 
        global ready
        if ready==False:
            await interaction.response.send_message("A game has already started")
            return
        ready = False # set the ready check to false since the game has started
        people = [interaction.user,member1]
        # I feel like there's a better way to do this but for the life of me rn I can't think of it
        if member2 != None: people.append(member2)
        if member3 != None: people.append(member3)
        if member4 != None: people.append(member4)
        if member5 != None: people.append(member5)
        if member6 != None: people.append(member6)
        if member7 != None: people.append(member7)
        if member2 ==None or member3==None: #change to 4 when ready
            await interaction.response.send_message("Not enough players for a fair game. Please get more acquaintances. At least 4 people total(including yourself) but a max of 8")
        else:
            global guild
            guild = interaction.guild
            global playerRole
            playerRole = await guild.create_role(name="player")
            global everyone
            everyone = guild.default_role
            j=1
            for i in people:
                print(f"people? {people[j-1].name} {i}")
                await self.addPlayer(i,j)
                j+=1
        await interaction.send("Setting up Game...")
        # Need to get the bot to create the channels.
        self.Deck()
        await interaction.send("Please have all party members join the SafeVC")
        await self.make(interaction)
        # Need to add Map related stuff
        await interaction.send("The dungeon has supplied magic scrolls to help the party.")
        for i in players:
            self.deal(i)

    @nextcord.slash_command(name="cleared",description="End the game")
    @application_checks.check(is_me)
    async def teardown(self,interaction:nextcord.Interaction):
        global ready
        ready = True # set the ready check to false since the game has started
        await interaction.response.send_message("Shutting down Game...")
        await playerRole.delete()
        await safeRoom.delete()
        await safeVC.delete()
        await category.delete()
    #@application_checks.check(ongoing)
    '''@nextcord.slash_command(name="player",description="Player commands during the game")
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
        await interaction.response.send_message("done")'''
    '''@player.subcommand(description="Display your stats")
    async def stats(self,interaction:nextcord.Interaction):
        i=0
        while i < self.hp:
            self.hpDis = self.hpDis + ":heart:"
            i+=1
        i=0
        if self.shield ==0: self.shieldDis = "None" 
        else: self.shieldDis = ""
        while i < self.shield:
            self.shieldDis = self.shieldDis + ":blue_heart:"
            i+=1
        i=0
        if len(self.hand)==0: self.handDis = "You have no scrolls. I'm suprised you're even still alive."
        while i < len(self.hand):
            self.handDis = f"{self.handDis} {self.hand[i].scrollName} a(n) {self.hand[i].scrollType} type of spell"
            i+=1
            if i == len(self.hand):
                self.handDis = self.handDis + "."
            else:
                self.handDis = self.handDis + ","
        MyEmbed = nextcord.Embed(title = self.name, description = "These your stats",color = nextcord.Colour(0xFFD700))
        MyEmbed.add_field(name="HP", value = self.hpDis,inline=True)
        MyEmbed.add_field(name="Shields", value=self.shieldDis,inline=True)
        MyEmbed.add_field(name="PlayerID",value=self.uid,inline=True)
        if self.Rogue:
            MyEmbed.add_field(name="Evil?",value="Yes",inline=True)
        MyEmbed.add_field(name="Owned Scrolls",value=self.handDis,inline=False)
        await interaction.response.send_message(embed=MyEmbed,ephemeral=True)'''
    @nextcord.slash_command(name="stats",description="your stats")
    async def stats(self,interaction:nextcord.Interaction):
        current=None
        for i in players:
            if interaction.user == i.mem:
                current = i
        i=0
        while i < current.hp:
            current.hpDis = current.hpDis + ":heart:"
            i+=1
        i=0
        if current.shield ==0: current.shieldDis = "None" 
        else: current.shieldDis = ""
        while i < current.shield:
            current.shieldDis = current.shieldDis + ":blue_heart:"
            i+=1
        i=0
        if len(current.hand)==0: current.handDis = "You have no scrolls. I'm suprised you're even still alive."
        while i < len(current.hand):
            current.handDis = f"{current.handDis} {current.hand[i].scrollName} a(n) {current.hand[i].scrollType} type of spell"
            i+=1
            if i == len(current.hand):
                current.handDis = current.handDis + "."
            else:
                current.handDis = current.handDis + ","
        MyEmbed = nextcord.Embed(title = current.name, description = "These your stats",color = nextcord.Colour(0xFFD700))
        MyEmbed.add_field(name="HP", value=current.hpDis,inline=True)
        MyEmbed.add_field(name="Shields", value=current.shieldDis,inline=True)
        MyEmbed.add_field(name="PlayerID",value=current.uid,inline=True)
        if current.Rogue:
            MyEmbed.add_field(name="Evil?",value="Yes",inline=True)
        MyEmbed.add_field(name="Owned Scrolls",value=current.handDis,inline=False)
        await interaction.response.send_message(embed=MyEmbed,ephemeral=True)
        
class Player:
    name="player"
    uid=0
    hp = 5
    hpDis = ""
    shield = 0
    shieldDis = "None"
    pRoom = None
    nRoom = None
    hand = [] # Players can hold a max of 5 scrolls
    handDis = "Scrolls: "
    Rogue = False
    turnDone = False
    mem = nextcord.Member # incase I need anything specific from discords member class
    reacting = False
    def __init__(self,player:nextcord.Member,uid):
        self.name = player.name
        self.mem = player
        self.uid = uid
        self.hand = []
        self.hp = 5
        self.shield = 0
        self.pRoom = None
        self.nRoom = None
        self.Rogue = False
        self.turnDone = False
        self.handDis = ""
        self.hpDis = ""
        self.shieldDis=""
        self.reacting = False
    def addScroll(self, scroll):
        print(f"Modifying {self.name}'s hand")
        if len(self.hand)!=5:
            self.hand.append(scroll)
            print(f"{scroll.scrollName} added to {self.name}'s hand")
        elif len(self.hand)==5:
            # Need to make a function for prompting the player if they're full to choose to swap and discard a scroll or give to another player
            print("Hand full...add later")
        else:
            print("something went wrong")
    
class Scroll: #This will all be internal. No player interaction to create scrolls for the game.
    scrollName = ""
    scrollType = "" # Off Def Anc
    counter = True # Whether it can be countered
    block = True # Whether it can be blocked
    avoid = True # Whether it can be avoided
    copy = 1 # will increment with each scroll that is created under the same name
    count = 3 # How many are in the deck total. This variable will be different for the different named scrolls but not change beyond that.
    aim = False # Need to make a use command and prompt user for a target if this is ever true
    serial = 0 # Serial number throughout the whole deck.
    flavor = "" # Flavor text of the scroll
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
                await interaction.response.send_message("That was not a valid name for a scroll.",ephemeral=True)
class Enemy:
    hp = 5

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
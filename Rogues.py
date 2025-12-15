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
bads = 0
start = False
# Need a function to check if there is a game running already
async def ongoing(interaction:nextcord.Interaction):
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
            await interaction.send(f"You may now assemble in the {safeRoom.mention}")
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
            case 9:
                await player.add_roles(playerRole)
                player9 = Player(player,uid)
                players.append(player9)
            case _:
                print("Not a discord member or Too many players")
        match len(players)/2:#how many rogues there will be
            case 2:
                bads = 1
            case 3:
                bads = 2
            case 4:
                if len(players)>8: bads=3
                else:
                    bads = 2
    def identify(self,player:nextcord.Member): #function to identify discord Member to Player class counterpart
        for i in players:
            if player == i.mem:
                return i
    def Deck(self): #create the "deck" of scrolls for the dungeon
        print("Creating Deck")
        self.createScroll("Wish","Ancillary",False,False,False,1,"") # TBD
        self.createScroll("Za Warudo","Ancillary",False,False,False,1,"") # when prompting defensive scrolls need to also check for this.
        self.createScroll("Soul Knot","Ancillary",False,False,False,1,"") # Link to another player when one dies the other dies but if they are both the only two to get out then they both win.
        self.createScroll("Holy Shield","Defensive",False,False,False,1,"") # Super Strong long lasting shield. numbers will be worked out later
        self.createScroll("Teleport","Defensive",False,False,False,6,"") # 6 teleport scrolls it can not be countered blocked or avoided (it's not an attack or aimed at anyone)
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
        print(f"Dealing to {player.name}:")
        for i in range(0,3): # Deal 3 scrolls at the start of the game
            dealt = random.choice(deck) # randomly pick a scroll
            deck.remove(dealt) # remove the scroll from the deck
            player.addScroll(dealt) # add the scroll to the player's hand
    @commands.command()
    @commands.check(is_me)
    async def loot(self,ctx,test:str=None,player2:nextcord.Member=None):
        player = self.identify(ctx.author)
        if player2 != None:
            player2 = self.identify(player2)
            #player2.hp = 3
            #print(f"{player2.name}'s health has been set to 3")
        if test !=None:
            for i in deck:
                if i.scrollName == "Fireball":
                    dealt = i
                    deck.remove(dealt)
                    player.addScroll(dealt)
                    break
            for i in deck:
                if i.scrollName == "Magic Shield":
                    dealt = i
                    deck.remove(dealt)
                    player.addScroll(dealt)
                    break
        else:
            dealt = random.choice(deck)
            deck.remove(dealt)
            player.addScroll(dealt)
    @commands.command()
    @commands.check(is_me)
    async def printDeck(self,ctx):
        if ready == True:
            ctx.send("No deck to print")
            return
        for i in deck:
            i.toPrint()
    @printDeck.error
    async def errorhandler(ctx:nextcord.Interaction,error):
        if isinstance(error,nextcord.errors.ApplicationCheckFailure):
            await ctx.send("You're not my Master!")
        #I'm thinking use deck command to make each scroll and the scroll class takes the variables to initialize them

    @nextcord.slash_command(name="rogues",description="Start the game and select the other players")
    async def RogueGame(self,interaction:nextcord.Interaction, #function to start the game
                        member1:nextcord.Member = nextcord.SlashOption(description="Another human to add to the game",required=True), # Members to be added to the game by the person who used the command.
                        member2:nextcord.Member = nextcord.SlashOption(description="Another human to add to the game",required=True), # Will make this required later
                        member3:nextcord.Member = nextcord.SlashOption(description="Another human to add to the game",required=True),
                        member4:nextcord.Member = nextcord.SlashOption(description="Another human to add to the game",required=False),
                        member5:nextcord.Member = nextcord.SlashOption(description="Another human to add to the game",required=False),
                        member6:nextcord.Member = nextcord.SlashOption(description="Another human to add to the game",required=False),
                        member7:nextcord.Member = nextcord.SlashOption(description="Another human to add to the game",required=False),
                        member8:nextcord.Member = nextcord.SlashOption(description="Another human to add to the game",required=False)):
        global ready
        if ready==False:
            await interaction.response.send_message("A game has already started")
            return
        ready = False # set the ready check to false since the game has started
        people = [interaction.user,member1,member2,member3]
        # I feel like there's a better way to do this but for the life of me rn I can't think of it
        if member4 != None: people.append(member4)
        if member5 != None: people.append(member5)
        if member6 != None: people.append(member6)
        if member7 != None: people.append(member7)
        if member8 != None: people.append(member8)
        global guild
        guild = interaction.guild
        global playerRole
        playerRole = await guild.create_role(name="player")
        global everyone
        everyone = guild.default_role
        j=1
        for i in people:
            #print(i)
            await self.addPlayer(i,j)
            j+=1
        await interaction.send("Setting up Game...")
        # Need to get the bot to create the channels.
        self.Deck()
        await interaction.send("Please have all party members join the SafeVC")
        await self.make(interaction)
        # Need to add Map related stuff
        await safeRoom.send("The dungeon has supplied magic scrolls to help the party.")
        for i in players:
            self.deal(i)
    @RogueGame.error
    async def errorhandler(ctx:nextcord.Interaction,error):
        if isinstance(error,nextcord.errors.ApplicationCommandOptionMissing):
            await ctx.send("Not enough players.")

    @nextcord.slash_command(name="teardown",description="End the game")
    @application_checks.check(is_me or ongoing)    
    async def teardown(self,interaction:nextcord.Interaction):
        global ready
        ready = True # set the ready check to false since the game has started
        await interaction.response.send_message("Shutting down Game...")
        await playerRole.delete()
        await safeRoom.delete()
        await safeVC.delete()
        await category.delete()
        deck.clear()
        for i in players:
            i.hand.clear()
        players.clear()
        print("GAME OVER")
    @teardown.error
    async def errorhandler(ctx:nextcord.Interaction,error):
        if isinstance(error,nextcord.errors.ApplicationCheckFailure):
            await ctx.send("You're not my Master!")
    @application_checks.check(ongoing)
    @nextcord.slash_command(name="player",description="Player commands during the game")
    async def player(self,interaction:nextcord.Interaction):
        pass
    @player.subcommand(description="Use one of your scrolls")
    #@nextcord.slash_command(name="cast",description="Use one of your scrolls")
    async def cast(self,interaction:nextcord.Interaction,scroll:str,target:nextcord.Member = None,target2:nextcord.Member = None):
        player = self.identify(interaction.user)
        scroll = str(scroll)
        await interaction.response.send_message(f"You are attempting to cast {scroll}",ephemeral=True)
        if target != None and target2 == None:
            await player.use(interaction,scroll,target)
        elif target2 != None:
            await player.use(interaction,scroll,target,target2)
        else:
            await player.use(interaction,scroll)
        return
    @player.subcommand(description="Show another player one of your scrolls")
    async def show(self,interaction:nextcord.Interaction,scroll:str,target:nextcord.Member=None):
        print("Player is showing their scroll.")
        player = self.identify(interaction.user)
        for i in player.hand:
            if i.scrollName == scroll and target==None:
                await interaction.response.send_message(f"{player.name} has a {scroll} scroll")
                return
            elif i.scrollName == scroll and target!=None:
                await target.send(f"{player.name} shows you that they own a {scroll} scroll")
                return
        await interaction.response.send_message(f"You do not have a {scroll} scroll")
    '''@player.subcommand(description="Duel another player")
    async def duel(self,interaction:nextcord.Interaction,target:nextcord.Member=None):
        print("Player wants to duel")
        await interaction.response.send_message("done")'''
    @player.subcommand(description="Display your stats")
    #@nextcord.slash_command(name="stats",description="your stats")
    async def stats(self,interaction:nextcord.Interaction):
        current=None
        current = self.identify(interaction.user)
        current.hpDis = ""
        current.shieldDis = "None"
        current.handDis = ""
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
        if len(current.hand)==0: current.handDis = "You have no scrolls. I'm surprised that you're even still alive."
        while i < len(current.hand):
            if i ==0:
                current.handDis = f"{i+1}. {current.handDis} **{current.hand[i].scrollName}** a(n) __{current.hand[i].scrollType}__ type of spell"
            else:
                current.handDis = f"{current.handDis} **{current.hand[i].scrollName}** a(n) __{current.hand[i].scrollType}__ type of spell"
            i+=1
            if i == len(current.hand):
                current.handDis = current.handDis + "."
            else:
                current.handDis = current.handDis + f",\n{i+1}. "
        MyEmbed = nextcord.Embed(title = current.name, description = "These are your stats",color = nextcord.Colour(0xFFD700))
        MyEmbed.add_field(name="HP", value=current.hpDis,inline=True)
        MyEmbed.add_field(name="Shields", value=current.shieldDis,inline=True)
        MyEmbed.add_field(name="PlayerID",value=current.uid,inline=True)
        if current.Rogue:
            MyEmbed.add_field(name="Evil?",value="Yes",inline=True)
        MyEmbed.add_field(name="Owned Scrolls",value=current.handDis,inline=False)
        await interaction.response.send_message(embed=MyEmbed,ephemeral=True)
    @stats.error
    async def errorhandler(ctx:nextcord.Interaction,error):
        if isinstance(error,nextcord.errors.ApplicationCheckFailure):
            await ctx.send("There isn't a game happening right now.")
    async def damage(self,victim,avoided=False):
        if victim.shield>0:
            if avoided: 
                await victim.mem.send(f"You have avoided damage.")
                return
            else:
                victim.shield-=1
                await victim.mem.send(f"You have taken damage that was blocked by one of your shields.")
                return
        else:
            if avoided: 
                await victim.mem.send(f"You have avoided damage.")
                return
            else:
                victim.hp-=1
                await victim.mem.send(f"You have taken damage.")
                return
    @tasks.loop(seconds=1)
    async def reactTime(self,interaction:nextcord.Interaction,victim):
        count = self.reactTime.current_loop
        remaining = 45 - count
        if remaining==0:
            self.reactTime.stop()
            await victim.mem.send(f"RIP")
            await victim.mem.send(f"You failed to react in time.")
            await Rogues.damage(Rogues,victim)
            victim.reacting = False
    class Reacts(nextcord.ui.View):
        def __init__(self,timeout = 45):
            super().__init__(timeout=timeout) 
    class butt(nextcord.ui.Button):
            def __init__(self,scroll=None,victim=None,caster=None,final=False):
                super().__init__()
                self.label = scroll.scrollName
                self.scroll = scroll
                self.victim = victim
                self.caster = caster
                if final:
                    self.label = "Take the hit"
                    self.custom_id = str(6)
                else:
                    self.custom_id = str(scroll.serial)

            async def callback(self,interaction:nextcord.Interaction):
                Rogues.reactTime.stop()
                print("react timer stopped")
                match str.lower(self.label):
                    case "invisibility":
                        await self.victim.use(interaction,self.label)
                        await Rogues.damage(Rogues,self.victim,True)
                        self.victim.reacting = False
                    case "teleport":
                        await self.victim.use(interaction,self.label,self.caster)
                        await Rogues.damage(Rogues,self.victim,True)
                        self.victim.reacting = False
                    case "counter":
                        await self.victim.use(interaction,self.label,self.caster)
                        await Rogues.damage(Rogues,self.victim,self.caster,True)
                        self.victim.reacting = False
                    case "za warudo":
                        await self.victim.use(interaction,self.label,self.caster)
                        await Rogues.damage(Rogues,self.victim,self.caster,True)
                        self.victim.reacting = False
                    case "take the hit":
                        await Rogues.damage(Rogues,self.victim)
                    case _:
                        await self.victim.use(interaction,self.label)
                        await Rogues.damage(Rogues,self.victim)
                        self.victim.reacting = False
    async def react(self,interaction,victim,caster,reaction):
        victim.handDis = ""
        MyEmbed = nextcord.Embed(title = "Reaction Spells", description = "These are the spells you own that can be used to save you from this attack",color = nextcord.Colour(0xFFD700))
        i=0
        while i < len(reaction):
            if i==0:
                victim.handDis = f"{i+1}. {victim.handDis} **{reaction[i].scrollName}**"
            else:
                victim.handDis = f"{victim.handDis} **{reaction[i].scrollName}**"
            i+=1
            if i == len(reaction):
                break
            elif i == len(reaction)-1:
                victim.handDis = victim.handDis + "."
            else:
                victim.handDis = victim.handDis + f",\n{i+1}. "
        MyEmbed.add_field(name="Owned Scrolls",value=victim.handDis,inline=False)
        view = self.Reacts()
        for j in reaction:
            view.add_item(self.butt(j,victim,caster))
        view.add_item(self.butt(j,victim,caster,True))
        await victim.mem.send(embed=MyEmbed,view=view)
        self.reactTime.start(self,interaction,victim)
        return
        
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
    handDis = ""
    Rogue = False
    turnDone = False
    mem = nextcord.Member # incase I need anything specific from discords member class
    reacting = False
    soul = ""
    def __init__(self,player:nextcord.Member,uid):
        if player.nick!=None:self.name = player.nick
        else: self.name = player.name
        self.mem = player
        self.uid = uid
        self.hand = []
        self.hp = 5
        self.shield = 0
        self.pRoom = None
        self.nRoom = None
        self.turnDone = False
        self.handDis = ""
        self.hpDis = ""
        self.shieldDis="None"
        self.reacting = False
        self.soul = ""
    def addScroll(self, scroll):
        if len(self.hand)!=5:
            self.hand.append(scroll)
            print(f"{scroll.scrollName} added to {self.name}'s hand")
        elif len(self.hand)==5:
            # Need to make a function for prompting the player if they're full to choose to swap and discard a scroll or give to another player
            print("Hand full...add code later")
        else:
            print(f"Something went wrong when dealing scrolls to {self.name}")
    async def use(self,interaction:nextcord.Interaction,scroll,target:nextcord.Member=None,target2:nextcord.Member=None):
        for i in self.hand:
            if str.lower(scroll) == str.lower(i.scrollName):
                if target == None:
                    await i.action(interaction)
                    return
                elif target2 != None:
                    await i.action(interaction,target,target2)
                    return
                else:
                    await i.action(interaction,target)
                    return
        await interaction.send("That was not a valid name for a scroll that you own.")

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
    async def action(self,interaction:nextcord.Interaction,target=None,target2=None):
        caster = Rogues.identify(Rogues,interaction.user)
        match str.lower(self.scrollName):
            case "teleport": # just used to avoid an attack for right now so not a lot needs to be here.
                print(f"{interaction.user} casted {self.scrollName}")
                if caster.reacting == True:
                    await safeRoom.send(f"{caster.name} teleported away from {target.name}'s attack")
                else:
                    pass
            case "fireball": # attacking a player so gotta check for a lot
                print(f"{interaction.user} casted {self.scrollName}")
                if target != None: # making sure there even is a target
                    victim = Rogues.identify(Rogues,target) # identify target player
                    hit = True # check to see if it automatically hits.
                    reaction = [] # array of the options the victim has.
                    await target.send(f"You are being targetted by {caster.name} who casted {self.scrollName}.\nYou have 45 seconds to react if you have any scrolls that can save you.")
                    for i in victim.hand:
                        if i.scrollType == "Defensive" or i.scrollName == "Za Warudo": # check if they have a defensive spell or Za Warudo cuz it's special.
                            reaction.append(i)
                            if len(reaction)==1:
                                await target.send(f"You have at least one scroll in your hand that can be used to save you from this spell. Which scroll will you use?")
                            hit = False # pause the hit
                    if hit:
                        await target.send(f"You have no scrolls that can save you from this spell. Big rip")
                        await Rogues.damage(Rogues,victim)
                    elif victim.reacting==True: # Players will need to react to spells one at a time.
                        await caster.send(f"{victim.name} is already being attacked and is currently reacting to another spell. Give them a moment to think they are safe(max 45 sec). Then you can try again.")
                    else:
                        await safeRoom.send(f"{caster.name} casted {self.scrollName} at {victim.name}")
                        victim.reacting = True
                        await Rogues.react(Rogues,interaction,victim,caster,reaction)
                else: # if there's no target
                    print(self.scrollName)
                    await interaction.send("You need to target ONE person with this scroll. Either yourself or another player in the same room.")
            case "counter": # avoid and counter attack
                print(f"{interaction.user} COUNTERED")
                if caster.reacting == True:
                    print("COUNTER")

            case "mold earth":
                print(f"{interaction.user} casted {self.scrollName}")
                if target != None and target2==None: # if there's only one target
                    healed = Rogues.identify(Rogues,target)
                    same = caster==healed
                    if same: # if the person ONLY targets themself.
                        await interaction.send(f"{caster.name} shielded themselves")
                        healed.shield+=2
                        print(f"{healed.name} was shielded to {healed.shield} shields")
                    else:
                        await interaction.send(f"{caster.name} casted Mold Earth on {healed.name}!")
                        healed.shield+=2
                        print(f"{healed.name} was shielded to {healed.shield} shields")
                    if caster.reacting==True:
                        await caster.mem.send("This is a reaction and will not use up your turn.")
                    else:
                        caster.turnDone = True
                        await caster.mem.send("You have ended your turn")
                elif target!=None and target==target2: # covering if the player puts in the same @ twice
                    caster = Rogues.identify(Rogues,interaction.user)
                    healed = Rogues.identify(Rogues,target)
                    same = caster==healed
                    if same: # if the person ONLY targets themself.
                        await interaction.send(f"{caster.name} shielded themselves")
                        healed.shield+=2
                        print(f"{healed.name} was shielded to {healed.shield} shields")
                    else:
                        await interaction.send(f"{caster.name} casted Mold Earth on {healed.name}!")
                        healed.shield+=2
                        print(f"{healed.name} was shielded to {healed.shield} shields")
                    if caster.reacting==True:
                        await caster.mem.send("This is a reaction and will not use up your turn.")
                    else:
                        caster.turnDone = True
                        await caster.mem.send("You have ended your turn")
                elif target2!=None and target!=target2: # two targets are not the same
                    caster = Rogues.identify(Rogues,interaction.user)
                    healed = Rogues.identify(Rogues,target)
                    healed2 = Rogues.identify(Rogues,target2)
                    healed.shield+=1
                    healed2.shield+=1
                    if caster == healed:
                        await interaction.send(f"{caster.name} shielded themself and {healed2.name}")
                        print(f"{caster.name} and {healed2.name} were shielded to {caster.shield} and {healed2.shield} shields")
                    elif caster == healed2:
                        await interaction.send(f"{caster.name} shielded themself and {healed.name}")
                        print(f"{caster.name} and {healed.name} were shielded to {caster.shield} and {healed.shield} shields")        
                    else:
                        await interaction.send(f"{caster.name} casted Magic Shield on {healed.name} and {healed2.name}!")
                        print(f"{healed.name} and {healed2.name} were shielded to {healed.shield} and {healed2.shield} shields")
                    if caster.reacting==True:
                        await caster.mem.send("This is a reaction and will not use up your turn.")
                    else:
                        caster.turnDone = True
                        await caster.mem.send("You have ended your turn")
                else: # if there's no target
                    print(self.scrollName)
                    await interaction.send("You need to target ONE person with this scroll. Either yourself or another player in the same room.")
            case "eldritch blast": # can't be avoided
                print(f"{interaction.user} casted {self.scrollName}")
            case "call lightning": # target two entities or one entity twice
                print(f"{interaction.user} casted {self.scrollName}")
            case "dragon breath": # can't be blocked
                print(f"{interaction.user} casted {self.scrollName}")
            case "scrying": #Ask chafe if this is random or if the victim chooses which one to reveal
                print(f"{interaction.user} casted {self.scrollName}")
            case "divine wisdom":
                print(f"{interaction.user} casted {self.scrollName}")
            case "barbarian rage": # +2 shields
                print(f"{interaction.user} casted {self.scrollName}")
            case "polymorph":
                print(f"{interaction.user} casted {self.scrollName}")
            case "invisibility": # need to more clearly define how this works but for the time being it will be an avoid spell only
                print(f"{interaction.user} casted {self.scrollName}")
            case "magic shield": # +1 shield
                print(f"{interaction.user} casted {self.scrollName}")
                if target != None and target2==None:
                    caster
                    healed = Rogues.identify(Rogues,target)
                    healed.shield+=1
                    same = interaction.user==target
                    if same:
                        await interaction.send(f"{caster.name} shielded themselves")
                        print(f"{healed.name} was shielded to {healed.shield} shields")
                    else:
                        await interaction.send(f"{interaction.user} casted Magic Shield on {healed.name}!")
                        print(f"{healed.name} was shielded to {healed.shield} shields")
                    if caster.reacting==True:
                        await caster.mem.send("This is a reaction and will not use up your turn.")
                    else:
                        caster.turnDone = True
                        await caster.mem.send("You have ended your turn")
                elif caster.reacting == True:
                    caster.shield+=1
                    await caster.mem.send(f"You shielded yourself.")
                else:
                    print("no target. not reacting")
                    await interaction.send("You need to target ONE person with this scroll. Either yourself or another player in the same room.")
            case "steal":
                print(f"{interaction.user} casted {self.scrollName}")
            case "blood altar":
                print(f"{interaction.user} casted {self.scrollName}")
            case "cure wounds":
                print(f"{interaction.user} casted {self.scrollName}")
                if target != None and target2==None:
                    healed = Rogues.identify(Rogues,target)
                    healed.hp+=1
                    same = caster==healed
                    if same:
                        await interaction.send(f"{caster.name} healed themselves")
                    else:
                        await interaction.send(f"{caster.name} casted Cure Wounds on {healed.name}!")
                    print(f"{healed.name} was healed to {healed.hp}")
                    if healed.hp >5:
                        healed.hp = 5
                        if same: await interaction.send(f"Well that was kind of dumb. You were full health...")   
                        else: await interaction.send(f"Well that was kind of dumb. {healed.name} was full health...")
                    caster.turnDone = True
                    await caster.mem.send("You have ended your turn")
                else:
                    print(self.scrollName)
                    await interaction.send("You need to target ONE person with this scroll. Either yourself or another player in the same room.")
            case "holy shield":
                print(f"{interaction.user} casted {self.scrollName}")
            case "soul knot": # add implementation for this at LITERALLY the end of the game lol
                print(f"{interaction.user} casted {self.scrollName}")
                caster.soul = target.name
                target.soul = caster.name
            case "wish":
                print(f"{interaction.user} casted {self.scrollName}")
            case "za warudo":
                print(f"{interaction.user} casted {self.scrollName}")
            case _: #Default
                await interaction.send("That was not a valid name for a scroll. Orrrrrr something went wrong...tell my Master",ephemeral=True)
        caster.hand.remove(self)
        deck.append(self)
        await interaction.send(f"*Your {self.scrollName} has returned to the Dungeon*")
class Enemy:
    hp = 3
class Room:
    id = None
    name = None

#setup done outside the class
async def setup(bot):
    bot.add_cog(Rogues(bot))
# Notes:
# Need to make a tear down command at the end of all of this to wipe everything ADD MORE TO IT
''' Player commands to check their stats DONE'''
'''Implement bot creating a text channel for dungeon and VCs for each room. Thinking to create a category for the game that the bot can then delete afterwards. DONE'''
'''Current idea is to have deck command make all the scrolls and for the ones with multiple counts to be done in a loop, that way I can pass the appropriate copy number. DONE'''
'''Each scroll will just be a function in the scroll class DONE'''
# When dealing with Rooms make an exit check that will happen each time a room has been entered by a player
# Need to make A LOT OF CHECKS primarily to see if a player has a spell(and which copy) in their hand
# Make a removeShields function for when the floor advances.
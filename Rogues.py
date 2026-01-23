# TLDR of how this came to be. My friend had an idea for a game that we worked on in the past. Making it into a card game.
# I realized on the playtest for the card game that it kind of needed a DM. I figured I could make a discrod bot to manage the stuff I had to manage for the playtest and here we are. 
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
RC = 0
# Need a function to check if there is a game running already
async def ongoing(interaction:nextcord.Interaction):
    return ready == False
class Rogues(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    async def make(self,interaction:nextcord.Interaction):
        await interaction.response.send_message("Setting up Game...")
        print("here")
        try:
            msg = await interaction.original_message()
            print("?")
            global category
            category = await guild.create_category("Rogues Category")
            await msg.edit(content="Creating the category and channels. Please remember to have a moderator use the ?teardown command when the game is done.")
            print(f"Category {category.name} created successfully!")
            global safeRoom
            safeRoom = await guild.create_text_channel(name="safe-room",category=category,position=0,topic="Room for the party to discuss and make decisions",overwrites={everyone:nextcord.PermissionOverwrite(view_channel=False,read_messages=False,send_messages=False),playerRole:nextcord.PermissionOverwrite(view_channel=True,read_messages=True,send_messages=True)})
            Room(name="Safe Room",id=0,exit=False,roomType="safe")
            global safeVC
            safeVC = await guild.create_voice_channel(name="Safe VC",category=category,overwrites={everyone:nextcord.PermissionOverwrite(view_channel=False,connect=False,read_messages=False,send_messages=False),playerRole:nextcord.PermissionOverwrite(view_channel=True,connect=True,read_messages=False,send_messages=False)})
            #await safeRoom.send("Please have all party members join the SafeVC")
            await safeRoom.send("This looks like a safe spot.")
            await msg.edit(content=f"You may now assemble in the {safeRoom.mention} OR VC")
        except Exception as e:
            print(f"53 An error occured: {e}")
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
    def identify(self,player:nextcord.Member=None,name:str=None): #function to identify discord Member to Player class counterpart
        if player!=None:
            for i in players:
                if player == i.mem:
                    return i
        else:
            for i in players:
                if name == i.name:
                    return i
    def Deck(self): #create the "deck" of scrolls for the dungeon
        print("Creating Deck") # counter block avoid
        self.createScroll("Wish","Ancillary",False,False,False,1,"","","https://github.com/Forte77/Beru-Bot/blob/initialBeru/wish.png?raw=true") # TBD
        self.createScroll("Za Warudo","Ancillary",False,False,False,1,"","","https://github.com/Forte77/Beru-Bot/blob/initialBeru/zawarudo.png?raw=true") # when prompting defensive scrolls need to also check for this.
        self.createScroll("Soul Knot","Ancillary",False,False,False,1,"Anything for my Senpai","Tie your soul and destiny to another player.","https://github.com/Forte77/Beru-Bot/blob/initialBeru/soulknot.png?raw=true",True) # Link to another player when one dies the other dies but if they are both the only two to get out then they both win.
        self.createScroll("Holy Shield","Defensive",False,False,False,1,"Nothing can pierce my Holy Pope Box","A shield of Divinity.\n*Grants +5 shields*","https://github.com/Forte77/Beru-Bot/blob/initialBeru/holyshield.png?raw=true") # Super Strong long lasting shield. numbers will be worked out later
        self.createScroll("Teleport","Defensive",False,False,False,6,"What the hell is all this black stuff on me?","A spell that can be used to return to a previous room or avoid an attack.","https://github.com/Forte77/Beru-Bot/blob/initialBeru/teleport.png?raw=true") # 6 teleport scrolls it can not be countered blocked or avoided (it's not an attack or aimed at anyone)
        self.createScroll("Fireball","Offensive",True,True,True,7,"So anyway I started blasting.","A basic attack spell.","https://github.com/Forte77/Beru-Bot/blob/initialBeru/fireball.png?raw=true",True) # 7 Fireball can be countered blocked and avoided
        self.createScroll("Counter","Defensive",False,True,True,7,"*FULL Counter*","A spell that can be used to counter attack someone that tried to cast a spell at you.","https://github.com/Forte77/Beru-Bot/blob/initialBeru/counter.png?raw=true") # Counter spell can be blocked and avoided but not countered
        self.createScroll("Mold Earth","Defensive",False,False,False,3,"THE BOULDER is conflicted","A defensive type of spell that can grant a shield to two different people or you can double up on one person or yourself","https://github.com/Forte77/Beru-Bot/blob/initialBeru/moldearth.png?raw=true",True,True) # Covers two players #
        self.createScroll("Eldritch Blast","Offensive",True,True,False,5,"Almost as good as that Ghost Boy","A cryptic attack that always finds it's target.","https://github.com/Forte77/Beru-Bot/blob/initialBeru/eldritch.png?raw=true",True) # Can't be avoided
        self.createScroll("Call Lightning","Offensive",False,True,True,5,"Talk about a STATIC SHOCK","Summon magical lightning bolts from above that can not be countered.","https://github.com/Forte77/Beru-Bot/blob/initialBeru/callliightning.png?raw=true",True,True) # Can't be countered
        self.createScroll("Dragon Breath","Offensive",True,False,True,5,"Girl dragons are just Reeking of feminine beauty","A flame so hot it bypasses through shields of any kind.","https://github.com/Forte77/Beru-Bot/blob/initialBeru/dragonsbreath.png?raw=true",True) # Can't be blocked
        self.createScroll("Scrying","Ancillary",False,False,False,4,"I CAN SEE THE FUTURE","Casting this spell will allow you to see one of the scrolls of your target. But they get to choose.","https://github.com/Forte77/Beru-Bot/blob/initialBeru/scrying.png?raw=true",True) # The target chooses which scroll to show
        self.createScroll("Divine Wisdom","Ancillary",False,False,False,3,"Filthy Ningen","Learn which scrolls your target owns currently.","https://github.com/Forte77/Beru-Bot/blob/initialBeru/divinewisdom.png?raw=true",True) # Reveal all scrolls of one chosen player to the user
        self.createScroll("Barbarian Rage","Defensive",False,False,False,3,"IMPOTENT RAGE!!!\n-# does not actually make you impotent","A spell that activates the dormant barbarian rage that sleeps in anyone. Allowing them to shield through attacks out of sheer anger.\n*Gives 2 shields*","https://github.com/Forte77/Beru-Bot/blob/initialBeru/barbarianrage.png?raw=true") # Blocks TWO instances of damage
        self.createScroll("Polymorph","Ancillary",True,False,False,2,"Now that I don't have a brain I don't even know what that means.","Turn your opponent into a useless wad of meat. They will be unable to complete actions for a limited time.","https://github.com/Forte77/Beru-Bot/blob/initialBeru/polymorph.png?raw=true",True) # Prevent another player from taking action twice CAN only be countered.
        self.createScroll("Invisibility","Defensive",False,False,False,3,"If I can't see them, then they can't see me.","You can go invisible to avoid attacks or cast it preemptively to be invisible for a limited time.","https://github.com/Forte77/Beru-Bot/blob/initialBeru/invisibility.png?raw=true") # Rogues have extra perks with invis
        self.createScroll("Magic Shield","Defensive",False,False,False,6,"No you are not the Shield Hero","Project a magical shield that will protect you from a single attack.\n*Gives 1 shield*","https://github.com/Forte77/Beru-Bot/blob/initialBeru/magicshield.png?raw=true",True) # Blocks a spell
        self.createScroll("Cure Wounds","Ancillary",False,False,False,4,"Just don't seek revenge...","Heal yourself or others.\n*Gives 1 HP*","https://github.com/Forte77/Beru-Bot/blob/initialBeru/curewounds.png?raw=true",True) # heal #
        self.createScroll("Explosion","Offensive",False,True,False,1,"Bakuretsu Bakurestu la la la","Summon an extremely powerful explosion that hurts everyone in the room. This spell can only be avoided by Teleport.","https://github.com/Forte77/Beru-Bot/blob/initialBeru/explosion.png?raw=true")
        print("check")
        if evil == True:
            self.createScroll("Steal","Offensive",False,False,True,4,"Please don't steal someone's panties.","Steal a random scroll from your target","https://github.com/Forte77/Beru-Bot/blob/initialBeru/steal.png?raw=true",True) # TBD
            self.createScroll("Blood Altar","Offensive",False,False,False,3,"A fine tribute to the Gore Queen Garuda","Sap health from your enemy if damage is dealt to enemy health.","https://github.com/Forte77/Beru-Bot/blob/initialBeru/bloodaltar.png?raw=true",True) # Sap Health if uninterupted. Won't heal if it is CBA
        sn = 0 
        for i in deck:
            self.serialize(i,sn) # Add serial number to the Scrolls to further help keep track of.
            sn +=1
        print("Deck created")
    def createScroll(self,name,type,counter,block,avoid,count,flavor="If you see this I fucked up",effect="This spell does...something",image="image url here",aim=False,aim2=False): # Function to create scrolls for the game
        i = 0
        global deck
        while (i < count):
            deck.append(Scroll(name,type,counter,block,avoid,i+1,count,flavor,effect,image,aim,aim2)) # Create Scroll and add it to the deck
            i+=1
    def serialize(self,scroll,sn):
        scroll.serial = sn
    def deal(self, player):
        print(f"Dealing to {player.name}:")
        for i in range(0,3): # Deal 3 scrolls at the start of the game
            dealt = random.choice(deck) # randomly pick a scroll
            deck.remove(dealt) # remove the scroll from the deck
            player.addScroll(dealt) # add the scroll to the player's hand
    async def createRoom(self,exit=False):
        RC+=1
        if exit:
            if difficulty==0:
                room = Room(name=f"Magic{RC}",id=RC,exit=True,roomType="Loot")
            else:
                room = Room(name=f"Exit{RC}",id=RC,exit=True,roomType="Exit")
        else:
            match (difficulty): #unsure how I want to tackle the exit situation.
                case 0:
                    types = ["monster","loot","trap"]
                    weight = [0.15,0.80,0.05]
                    room = random.choices(types,weight,k=1)
                    room = Room(name=f"Room{RC}",id=RC,exit=False,roomType=room)
                case 1:
                    types = ["monster","loot","trap"]
                    weight = [0.4,0.4,0.2]
                    room = random.choices(types,weight,k=1)
                    room = Room(name=f"Room{RC}",id=RC,exit=False,roomType=room) 
                case 2:
                    types = ["monster","loot","trap"]
                    weight = [0.33,0.34,0.33,]
                    room = random.choices(types,weight,k=1)
                    room = Room(name=f"Room{RC}",id=RC,exit=False,roomType=room) 
                case 3:
                    types = ["monster","loot","trap"]
                    weight = [0.4,0.20,0.4]
                    room = random.choices(types,weight,k=1)
                    room = Room(name=f"Room{RC}",id=RC,exit=False,roomType=room)
                case _:
                    await safeRoom.send("Something went wrong creating a room")
        await guild.create_text_channel(name=room.name,category=category,position=1,topic="A random room in the dungeon.",overwrites={everyone:nextcord.PermissionOverwrite(view_channel=False,read_messages=False,send_messages=False)})
        return room
    @commands.command()
    @commands.check(is_me)
    async def reset(self,ctx,member:nextcord.Member):
        print(member)
        redo = self.identify(name=member.name)
        print(isinstance(redo,Player))
        redo.turnDone = False
    @commands.command()
    #@commands.check(is_me)
    async def loot(self,ctx,test:str=None,player2:nextcord.Member=None): #for now this is a test command for me
        player = self.identify(ctx.author)
        if player2 != None:
            player2 = self.identify(player2)
            #player2.hp = 3
            #print(f"{player2.name}'s health has been set to 3")
        if test !=None:
            for i in deck:
                if i.scrollName == "Call Lightning":
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
            for i in deck:
                if i.scrollName == "Fireball":
                    dealt = i
                    deck.remove(dealt)
                    player.addScroll(dealt)
                    break
            #dealt = random.choice(deck)
            #deck.remove(dealt)
            #player.addScroll(dealt)
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
        people = set()
        people.add(interaction.user)
        people.add(member1)
        people.add(member2)
        people.add(member3)
        # I feel like there's a better way to do this but for the life of me rn I can't think of it
        if member4 != None: people.add(member4)
        if member5 != None: people.add(member5)
        if member6 != None: people.add(member6)
        if member7 != None: people.add(member7)
        if member8 != None: people.add(member8)
        if len(people) < 4:
            await interaction.response.send_message("Not enough players to start the game. Please find more friends.")
        print("made")
        global guild
        guild = interaction.guild
        global playerRole
        playerRole = await guild.create_role(name="player")
        global everyone
        everyone = guild.default_role
        print("it")
        j=1
        for i in people:
            #print(i)
            await self.addPlayer(i,j)
            j+=1
        print("to")
        # Need to get the bot to create the channels.
        print("right")
        self.Deck()
        print("over")
        await self.make(interaction)
        # Need to add Map related stuff
        print(".")
        await safeRoom.send("The dungeon has supplied magic scrolls to help the party.")
        global difficulty
        difficulty = 0
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
        ready = True 
        await interaction.response.send_message("Shutting down Game...")
        await playerRole.delete()
        await safeRoom.delete()
        await safeVC.delete()
        await category.delete()
        print("g")
        global deck
        del deck
        print("o")
        global players
        del players
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
    async def cast(self,interaction:nextcord.Interaction):
        caster = self.identify(interaction.user)
        if caster.turnDone==False:
            await self.chooseScroll(interaction,caster=caster,scrolls=caster.hand,cast=True)
        else:
            await interaction.response.send_message("You have already ended your turn. You can not use another scroll.",ephemeral=True)
        return
    @player.subcommand(description="Show another player one of your scrolls.")
    async def show(self,interaction:nextcord.Interaction,target:nextcord.Member=nextcord.SlashOption(description="If you don't select a player you will show everyone in the room.",required=False)):
        caster = self.identify(interaction.user)
        if caster.hand != []:
            if target!=None:
                victim = self.identify(target)
                await self.chooseScroll(interaction,victim=victim,caster=caster,scrolls=caster.hand,show=True)
            else:
                await self.chooseScroll(interaction,victim=caster,caster=caster,scrolls=caster.hand,show=True)
        else:
            await interaction.response.send_message("You have no scrolls to show",ephemeral=True)
    @player.subcommand(description="Give another player one of your scrolls.")
    async def give(self,interaction:nextcord.Interaction,target:nextcord.Member = nextcord.SlashOption(description="Choose who to give your scroll to.",required=True)):
        caster = self.identify(interaction.user)
        victim = self.identify(target)
        if caster == victim: 
            await interaction.response.send_message("You can't give yourself stuff",ephemeral=True)
        else:
            await self.chooseScroll(interaction,victim=victim,caster=caster,scrolls=caster.hand,give=True)
    @player.subcommand(description="End your turn manually")
    async def end(self,interaction:nextcord.Interaction):
        caster = self.identify(interaction.user)
        await interaction.response.send_message(f"{caster.name} has ended their turn")
        caster.turnDone = True
        if caster.dCount>0: caster.dCount-=1
    @player.subcommand(description="Display your stats")
    #@nextcord.slash_command(name="stats",description="your stats")
    async def stats(self,interaction:nextcord.Interaction):
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
            current.shieldDis = current.shieldDis + ":shield:"
            i+=1
        current.handDis = ""
        if len(current.hand)==0: 
            current.handDis = "You have no scrolls. I'm surprised that you're even still alive."
        i=0
        while i < len(current.hand):
            if len(current.hand)==1:
                current.handDis = f"{i+1}. **{current.hand[i].scrollName}** a(n) __{current.hand[i].scrollType}__ type of spell\n"
            elif i == len(current.hand):
                break
            elif i == len(current.hand)-1:
                current.handDis = current.handDis + f"{i+1}. **{current.hand[i].scrollName}** a(n) __{current.hand[i].scrollType}__ type of spell\n-# You can use the view command to inspect your scrolls"
            else:
                current.handDis = current.handDis + f"{i+1}. **{current.hand[i].scrollName}** a(n) __{current.hand[i].scrollType}__ type of spell\n"
            i+=1
        MyEmbed = nextcord.Embed(title = current.name, description = "These are your stats",color = nextcord.Colour(0xFFD700))
        MyEmbed.set_thumbnail(url=current.mem.display_avatar.url)
        MyEmbed.add_field(name="HP:heart:", value=current.hpDis,inline=True)
        MyEmbed.add_field(name="Shields:shield:", value=current.shieldDis,inline=True)
        MyEmbed.add_field(name="PlayerID",value=current.uid,inline=True)
        if current.Rogue:
            MyEmbed.add_field(name="Evil?",value="Yes",inline=True)
        if current.dCount>0:
            MyEmbed.add_field(name="Invis?",value=f"{current.dCount} turn(s)",inline=True)
        if current.soul != "":
            MyEmbed.add_field(name="Soulmate?", value=current.soul,inline=True)
        MyEmbed.add_field(name="Owned Scrolls",value=current.handDis,inline=False)
        await interaction.send(embed=MyEmbed,ephemeral=True)
    @player.subcommand(description="Duel another player")
    async def duel(self,interaction:nextcord.Interaction,target:nextcord.Member):
        caster = self.identify(interaction.user)
        victim = self.identify(target)
        await interaction.response.send_message(f"I have sanctioned a duel between {caster.name} and {victim.name}\nAll attacks made on these two will no longer work until the duel is over.\nI can not allow you to hear them but I will commentate if you would like to stay and await the thrilling conclusion.")
        #Need to add duel checks to EVERYTHING and a timer for the loser. I'm thinking they can duel over loot they find or freely duel to get scrolls from each other.
    @player.subcommand(name="view",description="Inspect one of your scrolls.")
    async def info(self,interaction:nextcord.Interaction):
        caster = self.identify(interaction.user)
        await self.chooseScroll(interaction,caster=caster,scrolls=caster.hand,info=True)
    @player.subcommand(name="move",description="Move to a new room.")
    async def move(self,interaction:nextcord.Interaction):
        #Make view and buttons for the possible next rooms
        #change movement to false and set up system so that when all players end their turn they all reset turn(dungeon does it's turn first but so far no enemies yet.)
        #cannot be used if in a monster room and cleared is false
        #establish prev next and new current room for player
        #edit create room to follow blueprint?
        caster = self.identify(interaction.user)

        if caster.nRoom!=None:
            caster.movement = False
            #move
        else:
            await interaction.response.send_message("There are no further rooms that extended beyond the current room. If this is an exit room please use the delve command to vote to go to the next floor.")
    @player.subcommand(name="delve",description="Delve to the next floor of the dungeon")
    async def delve(self,interaction:nextcord.Interaction):
        #Vote amongst all players(majority pass)
        #Mini teardown to delete rooms that were created. reset RC
        #Remove shields from all players
    @player.error
    async def errorhandler(ctx:nextcord.Interaction,error):
        if isinstance(error,nextcord.errors.ApplicationCheckFailure):
            await ctx.send("There isn't a game happening right now.")
    async def damage(self,victim,avoided=False):
        if victim.shield>0:
            if avoided: 
                await victim.mem.send(f"You have avoided damage.")
            else:
                victim.shield-=1
                await victim.mem.send(f"You have taken damage that was blocked by one of your shields.")
        else:
            if avoided or victim.dCount>0:
                await victim.mem.send(f"You have avoided damage.")
                if victim.dCount>0:
                    victim.dCount -=1
                    if victim.dCount == 0:
                        await victim.mem.send(f"You have used up your invisibility.")
            else:
                victim.hp-=1
                await victim.mem.send(f"You have taken damage.")
        if victim.hp == 0:
            if victim.soul != "":
                # kill both
                print("death for both")
            else:
                # make a death function
                await safeRoom.send(f"{victim.name} has perished.")
                players.pop(victim.uid)
                victim.mem.remove_roles(playerRole)
    class Butt(nextcord.ui.Button):
        def __init__(self,scrolls,victim=None,caster=None,react=False,give=False,show=False,cast=False,info=False,label="",style=nextcord.ui.Button.style,custom_id=None):
            super().__init__(label=label,style=style,custom_id=custom_id)
            self.scrolls = scrolls
            if victim != None:
                self.victim = victim
            if caster!=None:
                self.caster = caster
            self.react=react
            self.give=give
            self.show=show
            self.cast=cast
            self.info=info
        async def callback(self,interaction:nextcord.Interaction):
            try:
                check = self.view.getS()
                await interaction.response.defer()
                for i in self.scrolls:
                    if self.label == i.scrollName:
                        spell = i
                        print(f"Breaking loop. Spell is: {spell.scrollName}")
                        print(f"{spell.scrollName} aim values are {spell.aim} and {spell.aim2}")
                        break
                if self.react:
                    print("react")
                    match str.lower(self.label):
                        case "invisibility":
                            await self.victim.use(interaction,spell)
                            await Rogues.damage(Rogues,self.victim,True)
                            if check==False:
                                self.victim.reacting = False                        
                            else:
                                check = False
                        case "teleport":
                            await self.victim.use(interaction,spell,self.caster)
                            await Rogues.damage(Rogues,self.victim,True)
                            if check==False:
                                self.victim.reacting = False
                            else:
                                check = False 
                        case "counter":
                            await self.victim.use(interaction,spell,self.caster)
                            await Rogues.damage(Rogues,self.victim,True)
                            #self.victim.reacting = False for my implementation I think I should NOT do this yet
                        case "za warudo":
                            await self.victim.use(interaction,spell,self.caster)
                            await Rogues.damage(Rogues,self.victim,True)
                            if check==False:
                                self.victim.reacting = False
                            else:
                                check = False
                        case "take the hit":
                            await Rogues.damage(Rogues,self.victim)
                            self.victim.reacting = False
                        case _:
                            print("label check "+ self.label)
                            await self.victim.use(interaction,spell)
                            await Rogues.damage(Rogues,self.victim)
                            self.victim.reacting = False
                    if check:
                        self.view.setS(check=False)
                        inter = self.view.getI()
                        await Rogues.chooseScroll(self=Rogues,interaction=inter,victim=self.victim,caster=self.caster,scrolls=self.scrolls,react=True,same=False)
                elif self.show:
                    print("show")
                    if self.victim != None:
                        await self.victim.mem.send(f"{self.caster.name} has shown you that they own a {self.label} scroll")
                        await self.caster.mem.send(f"You showed {self.victim.name} your {self.label} scroll")
                    else:
                        await safeRoom.send(f"{self.caster.name} has shown you all that they own a {self.label} scroll")
                        await self.caster.mem.send(f"You showed everyone in {safeRoom} your {self.label} scroll")
                elif self.give:
                    print("give")
                    for i in self.caster.hand:
                        if i.scrollName == self.label:
                            await self.victim.mem.send(f"{self.caster.name} is giving you their {self.label} scroll")
                            self.caster.hand.remove(i)
                            self.victim.addScroll(i)
                            await self.caster.mem.send(f"You are giving {self.victim.name} your {self.label} scroll")
                            self.disabled = True
                            inter = self.view.getI()
                            await inter.edit_original_message(view=self.view)
                            break
                elif self.info:
                    for i in self.caster.hand:
                        if i.scrollName == self.label:
                            await Rogues.inspect(Rogues,interaction,i)
                            break
                elif self.cast:
                    print("cast")
                    MyEmbed = nextcord.Embed(title = "Who will be your victim(s)?", description = "These are the other Players in the room",color = nextcord.Colour(0xFFD700))
                    for i in players:
                        if spell.scrollType == "Offensive" and i.name == self.caster.name:
                            print("Same same")
                        else:
                            MyEmbed.add_field(name=f"Player {i.uid}",value=i.name,inline=True)
                    print(f"Spell: {spell.scrollName}")
                    if spell.aim:
                        aim = Rogues.Aiming(interaction,scroll=spell,caster=self.caster,embed=MyEmbed)
                        await interaction.send(embed=MyEmbed,view=aim,ephemeral=True)
                    else:
                        print("i'm dumb")
                        await self.caster.use(interaction,spell)
                if self.cast==False:
                    for i in self.view.children:
                        i.disabled = True
                        print(f"{i.label} disabled. RCallback")
                    await interaction.edit_original_message(view=self.view)
                    self.view.stop()
            except Exception as e:
                print(f"503 An error occured: {e}")
    class Reacts(nextcord.ui.View):
        def __init__(self,oginter:nextcord.Interaction,scrolls,victim=None,caster=None,react=False,give=False,show=False,cast=False,info=False,same=False):
            super().__init__(timeout=45)
            self.oginter = oginter
            self.Scheck = same
            self.victim = victim
            self.caster = caster
            self.scrolls = scrolls
            self.info = info
            self.react = react
            for i in scrolls:
                self.add_item(Rogues.Butt(scrolls=scrolls,victim=victim,caster=caster,react=react,give=give,show=show,cast=cast,info=info,label=i.scrollName,style=nextcord.ButtonStyle.green,custom_id=str(i.serial)))
            if react:
                self.add_item(Rogues.Butt(scrolls=scrolls,react=react,give=give,show=show,cast=cast,info=info,label="Take the hit",style=nextcord.ButtonStyle.red,custom_id=str(77)))
        def getS(self): # getter to track Same check
            print(self.Scheck)
            return self.Scheck
        def setS(self,check:bool): # setter to track Same check
            self.Scheck = check
            print(self.Scheck)
        def getI(self): # grabbing the original view interaction
            print("Interaction")
            return self.oginter
        async def on_timeout(self): # Disable all items in the view when it times out
            for i in self.children:
                i.disabled = True
                print(f"{i.label} disabled. Reacts")
            await self.oginter.edit_original_message(view=self)
            if self.Scheck and self.react:
                await Rogues.chooseScroll(self=Rogues,interaction=self.oginter,victim=self.victim,caster=self.caster,scrolls=self.scrolls,react=True,same=False)
            self.stop()
    class AimButt(nextcord.ui.Button):
        def __init__(self,scroll=None,caster=None,label="",style:nextcord.ui.Button.style=None,custom_id=None,embed=None):
            super().__init__(label=label,style=style,custom_id=custom_id)
            self = Rogues.AimButt
            self.scroll = scroll
            self.caster = caster
            self.t1 = None
            self.t2 = None
            self.embed= embed
        async def callback(self,interaction:nextcord.Interaction):
            try:
                await interaction.response.defer()
                print("40")
                if self.scroll.aim2 and not self.view.aimCheck():
                    self.t1 = Rogues.identify(Rogues,name=self.label)
                    self.disabled = True
                    self.view.add_item(Rogues.AimButt(scroll=self.scroll,caster=self.caster,label="Same person",style=nextcord.ButtonStyle.blurple,custom_id=str(78),embed=self.embed))
                    print("did the embed work?")
                    await interaction.edit_original_message(embed=self.embed,view=self.view)
                    self.view.setT(target=self.label)
                    print("saving target 1?")
                    return
                elif self.scroll.aim2 and self.view.aimCheck:
                    print("hi2")
                    self.t1 = self.view.getT()
                    print(self.t1.name)
                    if self.label == "Same person":
                        print("yep same")
                        await self.caster.use(interaction,self.scroll,target=self.t1.mem,same=True)
                    else:
                        print("yep")
                        self.t2 = Rogues.identify(Rogues,name=self.label)
                        print(f"{self.t1.name} and {self.t2.name}")
                        await self.caster.use(interaction,self.scroll,target=self.t1.mem,target2=self.t2.mem)
                    for i in self.view.children:
                        i.disabled = True
                    await interaction.edit_original_message(embed=self.embed,view=self.view)
                    self.view.stop()
                else:
                    self.t1 = Rogues.identify(Rogues,name=self.label)
                    await self.caster.use(interaction,self.scroll,target=self.t1.mem)
                    for i in self.view.children:
                        i.disabled = True
                    await interaction.edit_original_message(embed=self.embed,view=self.view)
                    self.view.stop()
            except Exception as e:
                print(f"577 An error occured: {e}")
    class Aiming(nextcord.ui.View):
        def __init__(self,oginter:nextcord.Interaction,scroll=None,caster=None,embed=None):
            super().__init__(timeout=60)
            self.scroll = scroll
            self.caster = caster
            self.oginter = oginter
            self.skip = False
            self.embed = embed
            self.test = None
            for i in players:
                if self.scroll.scrollType == "Offensive" and i.name == self.caster.name:
                    print("same same")
                else:
                    self.add_item(Rogues.AimButt(scroll=self.scroll,caster=self.caster,label=i.name,style=nextcord.ButtonStyle.green,custom_id=str(i.uid),embed=self.embed))
        def getT(self): # getter to track 1st Target
            print(self.test.name)
            return self.test
        def setT(self,target:str): # setter to track 1st Target
            self.test = Rogues.identify(Rogues,name=target)
            print(self.test.name)
        def aimCheck(self):
            if self.test!=None:
                return True
            else:
                return False
        async def on_timeout(self): # Disable all items in the view when it times out
            for i in self.children:
                i.disabled = True
                print(f"{i.label} disabled. Aiming")
            self.embed.title = "Failed to choose a target in time."
            self.embed.description = "You did not select a target in time. Please try again."
            await self.oginter.edit_original_message(embed=self.embed,view=self)
    async def reactCheck(self,interaction:nextcord.Interaction,victim,caster,scroll,same=False,counter=True,block=True,avoid=True,used=False,tried=False): # Figured I should just turn this into a function rather than pasting under every offensive spell.
        if victim.reacting==True: # Players will need to react to spells one at a time.  
            await caster.mem.send(f"{victim.name} is already being attacked and is currently reacting to another spell. Give them a moment to think they are safe(max 15 sec). Then you can try again.")
            if same:
                await caster.mem.send(f"The {scroll.scrollName} scroll will not be used since you only targetted {victim.name}")
                return False
            else:
                if used:
                    await caster.mem.send(f"Your second target, {victim.name}, is already being attacked and will not be targetted by this spell.")
                else:
                    if tried:
                        await caster.mem.send(f"The {scroll.scrollName} scroll will not be used.")
                    else:
                        await caster.mem.send(f"The {scroll.scrollName} scroll will still be used up if your second target is able to be hit by the attack.")
                return False
        else:
            await caster.mem.send("You have used your scroll and ended your turn")
            hit = True # check to see if it automatically hits.
            reaction = [] # array of the options the victim has.
            if victim.hand != []:
                await victim.mem.send(f"You are being targetted by {caster.name} who casted {scroll.scrollName}.\nYou have 15 seconds to react if you have any scrolls that can save you.")
                for i in victim.hand:
                    if i.scrollType == "Defensive" or i.scrollName == "Za Warudo": # check if they have a defensive spell or Za Warudo cuz it's special.
                        if i.scrollName == "Counter" and scroll.counter == False:
                            continue
                        if "shield"in i.effect and scroll.block==False:
                            continue
                        if "avoid" in i.effect and scroll.avoid==False:
                            continue
                        reaction.append(i)
                        if len(reaction)==1:
                            await victim.mem.send(f"You have at least one scroll in your hand that can be used to save you from this spell. Which scroll will you use?")
                            hit = False # pause the hit
            else:
                await victim.mem.send("You have no scrolls to defend with. git gud")
                hit = True
            if hit:
                await victim.mem.send(f"You have no scrolls that can save you from this spell. Big rip")
                if same:
                    await Rogues.damage(Rogues,victim)
                await Rogues.damage(Rogues,victim)
                caster.turnDone = True
            else:
                victim.reacting = True
                if same==False:
                    await self.chooseScroll(self=self,interaction=interaction,victim=victim,caster=caster,scrolls=reaction,react=True)
                    await safeRoom.send(f"{caster.name} casted {scroll.scrollName} at {victim.name}")
                elif same:
                    if tried:
                        await self.chooseScroll(self=self,interaction=interaction,victim=victim,caster=caster,scrolls=reaction,react=True,same=same)
                    else:
                        await self.chooseScroll(self=self,interaction=interaction,victim=victim,caster=caster,scrolls=reaction,react=True,same=same)
                        victim.reacting = False
                        await Rogues.reactCheck(Rogues,interaction,victim,caster,self,same=True,counter=counter,block=block,avoid=avoid,used=used,tried=True)
                        return True
                caster.turnDone = True
            return True
    async def chooseScroll(self,interaction:nextcord.Interaction,caster,scrolls,victim=None,react=False,show=False,give=False,cast=False,same=False,info=False):
        if react:
            MyEmbed = nextcord.Embed(title = "Reaction Spells", description = "These are the scrolls you own that can be used to save you from this attack",color = nextcord.Colour(0xFFD700))
        else:
            MyEmbed = nextcord.Embed(title = "Scrolls",description="These are the scrolls to choose from.")
        i=0
        if victim==None:
            victim=caster
        victim.handDis = ""
        while i < len(scrolls):
            if len(scrolls)==1:
                victim.handDis = f"{i+1}. **{scrolls[i].scrollName}**\n"
            elif i == len(scrolls):
                break
            elif i == len(scrolls)-1:
                victim.handDis = victim.handDis + f"{i+1}. **{scrolls[i].scrollName}**"
            else:
                victim.handDis = victim.handDis + f"{i+1}. **{scrolls[i].scrollName}**\n"
            i+=1
        MyEmbed.add_field(name="Owned Scrolls",value=victim.handDis,inline=False)
        MyEmbed.set_thumbnail(url=caster.mem.display_avatar.url)
        if react:
            await interaction.send(f"Your target: {victim.name} is reacting to your spell.")
            view = self.Reacts(oginter=interaction,scrolls=scrolls,victim=victim,caster=caster,react=react,same=same)
            await victim.mem.send(embed=MyEmbed,view=view)
        elif cast:
            view = self.Reacts(oginter=interaction,scrolls=scrolls,caster=caster,react=react,show=show,give=give,cast=cast)
            await interaction.response.send_message(embed=MyEmbed,view=view,ephemeral=True)
        elif info:
            view = self.Reacts(oginter=interaction,scrolls=scrolls,caster=caster,info=info)
            await interaction.response.send_message(embed=MyEmbed,view=view,ephemeral=True)
        else:
            view = self.Reacts(oginter=interaction,scrolls=scrolls,victim=victim,caster=caster,react=react,show=show,give=give,cast=cast)
            await interaction.response.send_message(embed=MyEmbed,view=view,ephemeral=True)
        return
    async def inspect(self,interaction:nextcord.Interaction,scroll):
        MyEmbed = nextcord.Embed(title = scroll.scrollName,description=f"**{scroll.scrollType}** type spell")
        MyEmbed.set_image(url=scroll.image)
        MyEmbed.add_field(name="Counterable?",value=scroll.counter,inline=True)
        MyEmbed.add_field(name="Blockable?",value=scroll.block,inline=True)
        MyEmbed.add_field(name="Avoidable?",value=scroll.avoid,inline=True)
        MyEmbed.add_field(name="Effect:",value=scroll.effect,inline=False)
        MyEmbed.add_field(name="",value=f"*{scroll.flavor}*")
        await interaction.send(embed=MyEmbed,ephemeral=True)
    
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
    dodge = False
    dCount = 0
    nRoom = []
    pRoom = None
    cRoom = "Safe Room"
    movement = True
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
        self.nRoom = []
        self.pRoom = None
        self.cRoom = "Safe Room"
        self.movement = True
    def addScroll(self, scroll):
        if len(self.hand)<5:
            self.hand.append(scroll)
            print(f"{scroll.scrollName} added to {self.name}'s hand")
        elif len(self.hand)==5:
            # Need to make a function for prompting the player if they're full to choose to swap and discard a scroll or give to another player
            print("Hand full...add code later")
        else:
            print(f"Something went wrong when dealing scrolls to {self.name}")
    async def use(self,interaction:nextcord.Interaction,spell,target:nextcord.Member=None,target2:nextcord.Member=None,same=False):
        print("use scroll?")
        if spell.aim2 and target2!=None: #leaving a note here. add in an aim and aim2 bool to relevant spells. check them here and then do the action. then go back to the cast part of the new view.
            await spell.action(interaction,target,target2)
            return
        elif spell.aim and target!=None:
            if same:
                await spell.action(interaction,target,same=same)
                return
            await spell.action(interaction,target)
            return
        else:
            if target!=None:
                await spell.action(interaction,target)
            else:
                await spell.action(interaction)
            return

class Scroll: #This will all be internal. No player interaction to create scrolls for the game.
    scrollName = ""
    scrollType = "" # Off Def Anc
    counter = True # Whether it can be countered
    block = True # Whether it can be blocked
    avoid = True # Whether it can be avoided
    copy = 1 # will increment with each scroll that is created under the same name
    count = 3 # How many are in the deck total. This variable will be different for the different named scrolls but not change beyond that.
    aim = False 
    aim2 = False
    serial = 0 # Serial number throughout the whole deck.
    flavor = "" # Flavor text of the scroll
    effect = ""
    image = ""
    def __init__(self,name,stype,counter,block,avoid,copy,count,flavor,effect,image,aim=False,aim2=False):
        self.scrollName = name
        self.scrollType = stype
        self.counter = counter
        self.block = block
        self.avoid = avoid
        self.copy = copy
        self.count = count
        self.flavor = flavor
        self.aim = aim
        self.aim2 = aim2
        self.effect = effect
        self.image = image
    def toPrint(self):
        print(f"{self.scrollName}. Type: {self.scrollType}. Serial Number: {self.copy}. There are {self.count} total in the dungeon.")
    async def action(self,interaction:nextcord.Interaction,target=None,target2=None,same:bool=False):
        caster = Rogues.identify(Rogues,interaction.user)# Can set all these up outside each individual action.
        if target!=None:
            victim = Rogues.identify(Rogues,target)
        if target2!=None:
            v2 = Rogues.identify(Rogues,target2)
        used = False
        match str.lower(self.scrollName):
            case "teleport": # just used to avoid an attack for right now so not a lot needs to be here.
                print(f"{interaction.user} casted {self.scrollName}")
                if caster.reacting == True:
                    await safeRoom.send(f"{caster.name} teleported away from {target.name}'s attack")
                    caster.reacting = False
                    used = True
                else:
                    print(self.scrollName)
                    pass # implement later
                    return
            case "fireball": # attacking a player so gotta check for a lot
                print(f"{interaction.user} casted {self.scrollName}")
                used = await Rogues.reactCheck(Rogues,interaction,victim,caster,self)
                caster.turnDone = True
                await caster.mem.send("You have used your scroll and ended your turn")
            case "counter": # avoid and counter attack
                print(f"{interaction.user} COUNTERED")
                if caster.reacting == True:
                    used = await Rogues.reactCheck(Rogues,interaction,target,caster,self,counter=self.counter)
                    caster.reacting = False
                else:
                    print(self.scrollName)
                    await interaction.send(f"The {self.scrollName} scroll can only be used in reaction to another spell.")
                    return
            case "mold earth":
                print(f"{interaction.user} casted {self.scrollName}")
                if v2==None:
                    victim.shield+=2
                    if victim == caster:
                        await interaction.send(f"{caster.name} casted Mold Earth and shielded themselves")
                    else:
                        await interaction.send(f"{caster.name} casted Mold Earth on {victim.name}!")
                    caster.turnDone = True
                    await caster.mem.send("You have used your scroll and ended your turn")
                elif victim!=None:
                    victim.shield+=1
                    v2.shield+=1
                    if victim == caster:
                        await caster.mem.send(f"You casted Mold Earth and shielded yourself")
                    else:
                        await victim.mem.send(f"{caster.name} casted Mold Earth on you!")
                    if v2 == caster:
                        await caster.mem.send(f"You casted Mold Earth and shielded yourself")
                    else:
                        await v2.mem.send(f"{caster.name} casted Mold Earth on you!")
                    caster.turnDone = True
                    await caster.mem.send("You have used your scroll and ended your turn")
                elif caster.reacting==True:
                    caster.shield+=2
                    await caster.mem.send(f"You casted Mold Earth and shielded yourself")
                    caster.reacting = False
                used = True
            case "eldritch blast": # can't be avoided
                print(f"{interaction.user} casted {self.scrollName}")
                used = await Rogues.reactCheck(Rogues,interaction,victim,caster,self,avoid=self.avoid)
                caster.turnDone = True
                await caster.mem.send("You have used your scroll and ended your turn")
            case "call lightning": # target two entities or one entity twice
                print(f"{interaction.user} casted {self.scrollName}")
                tried = False
                if target2!=None:
                    used = await Rogues.reactCheck(Rogues,interaction,victim,caster,self,counter=self.counter,block=self.block,avoid=self.avoid,used=used,tried=tried)
                    tried = True
                    used = await Rogues.reactCheck(Rogues,interaction,v2,caster,self,counter=self.counter,block=self.block,avoid=self.avoid,used=used,tried=tried)
                elif target2 == None or same: # if the target is double fucked
                    used = await Rogues.reactCheck(Rogues,interaction,victim,caster,self,same=same,counter=self.counter,block=self.block,avoid=self.avoid,used=used)
                caster.turnDone = True
                await caster.mem.send("You have used your scroll and ended your turn")
            case "dragon breath": # can't be blocked
                print(f"{interaction.user} casted {self.scrollName}")
                victim = Rogues.identify(Rogues,target) # identify target player
                used = await Rogues.reactCheck(Rogues,interaction,victim,caster,self,block=self.block)
                caster.turnDone = True
                await caster.mem.send("You have used your scroll and ended your turn")
            case "scrying":
                print(f"{interaction.user} casted {self.scrollName}")
            case "divine wisdom":
                print(f"{interaction.user} casted {self.scrollName}")
            case "barbarian rage": # +2 shields to yourself
                print(f"{interaction.user} casted {self.scrollName}")
                if caster.reacting == True:
                    caster.shield +=2
                    await caster.mem.send("Your rage shields you allowing you to ignore damage twice.")
                    caster.reacting = False
                else:
                    caster.shield +=2
                    await caster.mem.send("Your rage shields you allowing you to ignore damage twice.")
                    caster.turnDone = True
                    await caster.mem.send("You have used your scroll and ended your turn")
            case "polymorph":
                print(f"{interaction.user} casted {self.scrollName}")
            case "invisibility": # need to more clearly define how this works but for the time being it will be an avoid spell only
                print(f"{interaction.user} casted {self.scrollName}")
                if caster.reacting == True:
                    caster.dCount = 2
                else:
                    caster.dCount = 2
                    caster.turnDone = True
                    await caster.mem.send("You have used your scroll and ended your turn")
            case "magic shield": # +1 shield
                print(f"{interaction.user} casted {self.scrollName}")
                if target != None:
                    victim.shield+=1
                    same = caster==victim
                    if same:
                        await interaction.send(f"{caster.name} shielded themselves")
                        print(f"{victim.name} was shielded to {victim.shield} shields")
                    else:
                        await interaction.send(f"{caster.name} casted Magic Shield on {victim.name}!")
                        print(f"{victim.name} was shielded to {victim.shield} shields")
                    caster.turnDone = True
                    await caster.mem.send("You have ended your turn")
                elif caster.reacting == True:
                    caster.shield+=1
                    await caster.mem.send(f"You reacted and shielded yourself.")
                    caster.reacting = False
                else:
                    caster.shield+=1
                    await caster.mem.send(f"You shielded yourself.")
                    caster.turnDone = True
            case "steal": # will work on these when we get there.
                print(f"{interaction.user} casted {self.scrollName}")
            case "blood altar": # ^
                print(f"{interaction.user} casted {self.scrollName}")
            case "cure wounds":
                print(f"{interaction.user} casted {self.scrollName}")
                victim.hp+=1
                same = caster==victim
                if same:
                    await interaction.send(f"{caster.name} healed themselves")
                else:
                    await interaction.send(f"{caster.name} casted Cure Wounds on {victim.name}!")
                print(f"{victim.name} was healed to {victim.hp}")
                if victim.hp >5:
                    victim.hp = 5
                    if same: await interaction.send(f"Well that was kind of dumb. You were full health...")   
                    else: await interaction.send(f"Well that was kind of dumb. {victim.name} was full health...")
                caster.turnDone = True
                await caster.mem.send("You have used your scroll and ended your turn")
            case "holy shield":
                print(f"{interaction.user} casted {self.scrollName}")
                await caster.mem.send("You *truly* have the power of **God** on your side.")
                caster.shield +=5
                if caster.reacting==True:
                    await caster.mem.send("This is a reaction and will not use up your turn.")
                else:
                    caster.turnDone = True
                    await caster.mem.send("You have used your scroll and ended your turn")
                used = True
            case "soul knot": # add implementation for this at LITERALLY the end of the game lol
                print(f"{interaction.user} casted {self.scrollName}") # Not limited to room and will expose death if target is dead.
                if target == None or caster == victim:
                    await caster.mem.send("You can **not** *knot* your soul with itself.")
                    return
                used = True
                caster.soul = victim.mem
                victim.soul = caster.mem
                await caster.mem.send(f"Your soul is now linked with {victim.name}.\n**Regardless of any other factors** if you both are the only ones to make it out of the dungeon __alive__ you both will be considered the winners of this excursion.\n**However if one of you dies. You both perish.**")
                await victim.mem.send(f"Your soul is now linked with {caster.name}.\n**Regardless of any other factors** if you both are the only ones to make it out of the dungeon __alive__ you both will be considered the winners of this excursion.\n**However if one of you dies. You both perish.**")
            case "wish":
                print(f"{interaction.user} casted {self.scrollName}")
            case "za warudo":
                print(f"{interaction.user} casted {self.scrollName}")
            case _: #Default
                await interaction.send("That was not a valid name for a scroll. Orrrrrr something went wrong...tell my Master",ephemeral=True)
        if used:
            caster.hand.remove(self)
            if str.lower(self.scrollName) == "soul knot":
                safeRoom.send("# Soul Knot has been used and will not be returned to the dungeon.")
            else:
                deck.append(self)
            await interaction.send(f"*Your {self.scrollName} has returned to the Dungeon*",ephemeral=True)
        if caster.dCount>0: caster.dCount-=1
class Enemy:
    hp = 3
class Room:
    id = None
    name = None
    next = []
    prev = []
    exit = False
    guests = []
    roomType = "" # monster loot trap exit
    def __init__(self,name,id,exit,roomType):
        self.id = id
        self.name = name
        self.exit = exit
        self.roomType = roomType
    def guestList(self):
        return self.guests
    def getNext(self):
        return self.next
    def setNext(self,rooms):
        self.next=rooms
    def setPrev(self,rooms):
        self.prev=rooms
    
# list of rooms I can randomize and then in second half I add the exit room to the list

#setup done outside the class
async def setup(bot):
    bot.add_cog(Rogues(bot))

''' I want to:
verify all buttons disable properly when casting,reacting,etc
'''
# Notes:
# idea: difficulty (int counter that goes up whenever the party advances rooms or floors[undecided]) will be used to influence enemy stats.
# wish idea: second life. when you die you are reborn(full health, 3 random scrolls from deck) into a previous room if applicable.
# Reminder to keep teardown up to date
# Need to make a death function to handle soul knot and other stuff
# When dealing with Rooms make an exit check that will happen each time a room has been entered by a player
# Make a removeShields function for when the floor advances.
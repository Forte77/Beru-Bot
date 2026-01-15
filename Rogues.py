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
# Need a function to check if there is a game running already
async def ongoing(interaction:nextcord.Interaction):
    return ready == False
class Rogues(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    async def make(self,interaction:nextcord.Interaction):
        try:
            msg = await interaction.original_message()
            global category
            category = await guild.create_category("Rogues Category")
            await msg.edit(content="Creating the category and channels. Please remember to have a moderator use the ?teardown command when the game is done.")
            print(f"Category {category.name} created successfully!")
            global safeRoom
            safeRoom = await guild.create_text_channel(name="safe-room",category=category,position=0,topic="Room for the party to discuss and make decisions",overwrites={everyone:nextcord.PermissionOverwrite(view_channel=False,read_messages=False,send_messages=False),playerRole:nextcord.PermissionOverwrite(view_channel=True,read_messages=True,send_messages=True)})
            await msg.edit(content=f"You may now assemble in the {safeRoom.mention} OR VC")
            global safeVC
            safeVC = await guild.create_voice_channel(name="Safe VC",category=category,overwrites={everyone:nextcord.PermissionOverwrite(view_channel=False,connect=False,read_messages=False,send_messages=False),playerRole:nextcord.PermissionOverwrite(view_channel=True,connect=True,read_messages=False,send_messages=False)})
            #await safeRoom.send("Please have all party members join the SafeVC")
            await safeRoom.send("This looks like a safe spot.")
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
        self.createScroll("Wish","Ancillary",False,False,False,1,"") # TBD
        self.createScroll("Za Warudo","Ancillary",False,False,False,1,"") # when prompting defensive scrolls need to also check for this.
        self.createScroll("Soul Knot","Ancillary",False,False,False,1,"Tie your soul and destiny to another player.",True) # Link to another player when one dies the other dies but if they are both the only two to get out then they both win.
        self.createScroll("Holy Shield","Defensive",False,False,False,1,"A shield of Divinity.\n*Grants +5 shields*") # Super Strong long lasting shield. numbers will be worked out later
        self.createScroll("Teleport","Defensive",False,False,False,6,"A spell that can be used to return to a previous room or avoid an attack.") # 6 teleport scrolls it can not be countered blocked or avoided (it's not an attack or aimed at anyone)
        self.createScroll("Fireball","Offensive",True,True,True,7,"So anyway I started blasting.",True) # 7 Fireball can be countered blocked and avoided
        self.createScroll("Counter","Defensive",False,True,True,7,"A spell that can be used to counter attack someone that tried to cast a spell at you.") # Counter spell can be blocked and avoided but not countered
        self.createScroll("Mold Earth","Defensive",False,False,False,3,"A defensive type of spell that can grant a shield to two different people or you can double up on one person or yourself",True,True) # Covers two players #
        self.createScroll("Eldritch Blast","Offensive",True,True,False,5,"A cryptic attack that always finds it's target.",True) # Can't be avoided
        self.createScroll("Call Lightning","Offensive",False,True,True,5,"Summon magical lightning bolts from above that can not be countered.",True,True) # Can't be countered
        self.createScroll("Dragon Breath","Offensive",True,False,True,5,"A flame so hot it bypasses through shields of any kind.",True) # Can't be blocked
        self.createScroll("Scrying","Ancillary",False,False,False,4,"Casting this spell will allow you to see one of the scrolls of your target. But they get to choose.",True) # The target chooses which scroll to show
        self.createScroll("Divine Wisdom","Ancillary",False,False,False,3,"",True) # Reveal all scrolls of one chosen player to the user
        self.createScroll("Barbarian Rage","Defensive",False,False,False,3,"A spell that activates the dormant barbarian rage that sleeps in anyone. Allowing them to shield through attacks out of sheer anger.\n*Gives 2 shields*") # Blocks TWO instances of damage
        self.createScroll("Polymorph","Ancillary",True,False,False,2,"",True) # Prevent another player from taking action twice CAN only be countered.
        self.createScroll("Invisibility","Defensive",False,False,False,3,"You can go invisible to avoid attacks or cast it preemptively to be invisible for a limited time.") # Rogues have extra perks with invis
        self.createScroll("Magic Shield","Defensive",False,False,False,6,"Project a magical shield that will protect you from a single attack.\n*Gives 1 shield*") # Blocks a spell
        self.createScroll("Cure Wounds","Ancillary",False,False,False,4,"Heal yourself or others.\n*Gives 1 HP*",True) # heal #
        #Need to add in explosion
        print("check")
        if evil == True:
            self.createScroll("Steal","Offensive",False,False,True,4,"") # TBD
            self.createScroll("Blood Altar","Offensive",False,False,False,3,"") # Sap Health if uninterupted. Won't heal if it is CBA
        sn = 0 
        for i in deck:
            self.serialize(i,sn) # Add serial number to the Scrolls to further help keep track of.
            sn +=1
        print("Deck created")
    def createScroll(self,name,type,counter,block,avoid,count,flavor="If you see this I fucked up",aim=False,aim2=False): # Function to create scrolls for the game
        i = 0
        global deck
        while (i < count):
            deck.append(Scroll(name,type,counter,block,avoid,i+1,count,flavor,aim,aim2)) # Create Scroll and add it to the deck
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
        await interaction.response.send_message("Setting up Game...")
        # Need to get the bot to create the channels.
        self.Deck()
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
        ready = True 
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
    async def cast(self,interaction:nextcord.Interaction):
        caster = self.identify(interaction.user)
        if caster.turnDone==False:
            await self.chooseScroll(interaction,caster=caster,scrolls=caster.hand,cast=True)
        else:
            await interaction.response.send_message("You have already ended your turn. You can not use another scroll.")
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
                current.handDis = current.handDis + f"{i+1}. **{current.hand[i].scrollName}** a(n) __{current.hand[i].scrollType}__ type of spell"
            else:
                current.handDis = current.handDis + f"{i+1}. **{current.hand[i].scrollName}** a(n) __{current.hand[i].scrollType}__ type of spell\n"
            i+=1
        MyEmbed = nextcord.Embed(title = current.name, description = "These are your stats",color = nextcord.Colour(0xFFD700))
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
    @stats.error
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
        def __init__(self,scrolls,victim=None,caster=None,react=False,give=False,show=False,cast=False,label="",style=nextcord.ui.Button.style,custom_id=None):
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
        async def callback(self,interaction:nextcord.Interaction):
            try:
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
                            self.victim.reacting = False
                        case "teleport":
                            await self.victim.use(interaction,spell,self.caster)
                            await Rogues.damage(Rogues,self.victim,True)
                            self.victim.reacting = False
                        case "counter":
                            await self.victim.use(interaction,spell,self.caster)
                            await Rogues.damage(Rogues,self.victim,True)
                            #self.victim.reacting = False for my implementation I think I should NOT do this yet
                        case "za warudo":
                            await self.victim.use(interaction,spell,self.caster)
                            await Rogues.damage(Rogues,self.victim,True)
                            self.victim.reacting = False
                        case "take the hit":
                            await Rogues.damage(Rogues,self.victim)
                            self.victim.reacting = False
                        case _:
                            print("label check "+ self.label)
                            await self.victim.use(interaction,spell)
                            await Rogues.damage(Rogues,self.victim)
                            self.victim.reacting = False
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
                            await interaction.response.edit_message(view=self.view)
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
                print(f"481 An error occured: {e}")
    class Reacts(nextcord.ui.View):
        def __init__(self,oginter:nextcord.Interaction,scrolls,victim=None,caster=None,react=False,give=False,show=False,cast=False):
            super().__init__(timeout=15)
            self.oginter = oginter
            for i in scrolls:
                self.add_item(Rogues.Butt(scrolls=scrolls,victim=victim,caster=caster,react=react,give=give,show=show,cast=cast,label=i.scrollName,style=nextcord.ButtonStyle.green,custom_id=str(i.serial)))
            if react:
                self.add_item(Rogues.Butt(scrolls=scrolls,react=react,give=give,show=show,cast=cast,label="Take the hit",style=nextcord.ButtonStyle.red,custom_id=str(77)))
        async def on_timeout(self): # Disable all items in the view when it times out
            for i in self.children:
                i.disabled = True
                print(f"{i.label} disabled. Reacts")
            await self.oginter.edit_original_message(view=self)
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
                        await self.caster.use(interaction,self.scroll,target=self.t1.mem)
                    else:
                        print("yep")
                        self.t2 = Rogues.identify(Rogues,name=self.label)
                        print(f"{self.t1.name} and {self.t2.name}")
                        await self.caster.use(interaction,self.scroll,target=self.t1.mem,target2=self.t2.mem)
                    self.view.stop()
                else:
                    self.t1 = Rogues.identify(Rogues,name=self.label)
                    await self.caster.use(interaction,self.scroll,target=self.t1.mem)
                    for i in self.view.children:
                        i.disabled = True
                    await interaction.edit_original_message(embed=self.embed,view=self.view)
                    self.view.stop()
            except Exception as e:
                print(f"538 An error occured: {e}")
    #@staticmethod
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
        def getT(self):
            print(self.test.name)
            return self.test
        def setT(self,target:str):
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
    async def reactCheck(self,interaction:nextcord.Interaction,victim,caster,scroll,victim2=None,same=False,counter=True,block=True,avoid=True): # Figured I should just turn this into a function rather than pasting under every offensive spell.
        if victim.reacting==True: # Players will need to react to spells one at a time.
            await caster.mem.send(f"{victim.name} is already being attacked and is currently reacting to another spell. Give them a moment to think they are safe(max 15 sec). Then you can try again.")
            if victim2!=None:
                if same == False:
                    await caster.mem.send("This scroll will still be used up if your second target is able to be hit by the attack.")
                else:
                    return
                if victim2.reacting == True and same==False:
                    await caster.mem.send(f"Both {victim.name} and {victim2.name} are currently being attacked by others. Please wait at most 15 seconds and try again.")
                    return
                elif victim2.reacting ==False and same ==False:
                    await self.reactCheck(self=Rogues,interaction=interaction,victim=victim2,caster=caster,scroll=scroll,counter=counter,block=block,avoid=avoid)
            return
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
                        if "shield"in i.flavor and scroll.block==False:
                            continue
                        if "avoid" in i.flavor and scroll.avoid==False:
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
                if same ==True:
                    await Rogues.damage(Rogues,victim)
                await Rogues.damage(Rogues,victim)
                caster.turnDone = True
            else:
                if victim2 != None and same ==False:
                    victim.reacting = True
                    victim2.reacting = True
                    await self.chooseScroll(self=self,interaction=interaction,victim=victim,v2=victim2,caster=caster,scrolls=reaction,react=True)
                elif same == False:
                    victim.reacting = True
                    await self.chooseScroll(self=self,interaction=interaction,victim=victim,caster=caster,scrolls=reaction,react=True)
                    await safeRoom.send(f"{caster.name} casted {scroll.scrollName} at {victim.name}")
                if same == True and len(reaction) == 1:
                    victim.reacting = True
                    await self.chooseScroll(self=self,interaction=interaction,victim=victim,caster=caster,scrolls=reaction,react=True)
                    await asyncio.sleep(21)
                    await Rogues.damage(Rogues,victim)
                elif same == True and len(reaction)>1:
                    victim.reacting = True
                    await self.chooseScroll(self=self,interaction=interaction,victim=victim,caster=caster,scrolls=reaction,react=True)
                    await asyncio.sleep(21)
                    victim.reacting = False
                    await self.reactCheck(self=Rogues,interaction=interaction,victim=victim,caster=caster,scroll=scroll,counter=counter,block=block,avoid=avoid)
                caster.turnDone = True
        if victim2!=None:
            caster.turnDone = True
            await self.reactCheck(self,Rogues,interaction=interaction,victim=victim2,caster=caster,scroll=scroll,counter=counter,block=block,avoid=avoid)
    async def chooseScroll(self,interaction:nextcord.Interaction,caster,scrolls,victim=None,v2=None,react=False,show=False,give=False,cast=False):
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
        if react:
            await interaction.response.send_message(f"Your target: {victim.name} is reacting to your spell.")
            view = self.Reacts(oginter=interaction,scrolls=scrolls,victim=victim,caster=caster,react=react)
            await victim.mem.send(embed=MyEmbed,view=view)
        elif cast:
            view = self.Reacts(oginter=interaction,scrolls=scrolls,caster=caster,react=react,show=show,give=give,cast=cast)
            await interaction.response.send_message(embed=MyEmbed,view=view)
        else:
            view = self.Reacts(oginter=interaction,scrolls=scrolls,victim=victim,caster=caster,react=react,show=show,give=give,cast=cast)
            await interaction.response.send_message(embed=MyEmbed,view=view,ephemeral=True)
        if v2!=None:
            await self.chooseScroll(interaction,caster,scrolls,v2,react=react)
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
    dodge = False
    dCount = 0
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
        if len(self.hand)<5:
            self.hand.append(scroll)
            print(f"{scroll.scrollName} added to {self.name}'s hand")
        elif len(self.hand)==5:
            # Need to make a function for prompting the player if they're full to choose to swap and discard a scroll or give to another player
            print("Hand full...add code later")
        else:
            print(f"Something went wrong when dealing scrolls to {self.name}")
    async def use(self,interaction:nextcord.Interaction,spell,target:nextcord.Member=None,target2:nextcord.Member=None):
        print("use scroll?")
        if spell.aim2 and target2!=None: #leaving a note here. add in an aim and aim2 bool to relevant spells. check them here and then do the action. then go back to the cast part of the new view.
            await spell.action(interaction,target,target2)
            return
        elif spell.aim and target!=None:
            await spell.action(interaction,target)
            return
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
    def __init__(self,name,stype,counter,block,avoid,copy,count,flavor,aim=False,aim2=False):
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
    def toPrint(self):
        print(f"{self.scrollName}. Type: {self.scrollType}. Serial Number: {self.copy}. There are {self.count} total in the dungeon.")
    async def action(self,interaction:nextcord.Interaction,target=None,target2=None):
        caster = Rogues.identify(Rogues,interaction.user)# Can set all these up outside each individual action.
        if target!=None:
            victim = Rogues.identify(Rogues,target)
        if target2!=None:
            v2 = Rogues.identify(Rogues,target2)
        match str.lower(self.scrollName):
            case "teleport": # just used to avoid an attack for right now so not a lot needs to be here.
                print(f"{interaction.user} casted {self.scrollName}")
                if caster.reacting == True:
                    await safeRoom.send(f"{caster.name} teleported away from {target.name}'s attack")
                    caster.reacting = False
                else:
                    print(self.scrollName)
                    pass # implement later
                    return
            case "fireball": # attacking a player so gotta check for a lot
                print(f"{interaction.user} casted {self.scrollName}")
                if target != None: # making sure there even is a target
                    await Rogues.reactCheck(Rogues,interaction,victim,caster,self)
                else: # if there's no target
                    print(self.scrollName)
                    await interaction.send("You need to target ONE person with this scroll. Either yourself or another player in the same room.")
                    return
            case "counter": # avoid and counter attack
                print(f"{interaction.user} COUNTERED")
                if caster.reacting == True:
                    await Rogues.reactCheck(Rogues,interaction,target,caster,self,counter=self.counter)
                    caster.reacting = False
                else:
                    print(self.scrollName)
                    await interaction.send("This scroll can only be used in reaction to another spell.")
                    return
            case "mold earth":
                print(f"{interaction.user} casted {self.scrollName}")
                if target != None and target2==None: # if there's only one target
                    healed = Rogues.identify(Rogues,target) # I'll leave the healing ones 
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
                        caster.reacting = False
                    else:
                        caster.turnDone = True
                        await caster.mem.send("You have ended your turn")
                elif target!=None and target==target2: # covering if the player puts in the same @ twice
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
                        caster.reacting = False
                    else:
                        caster.turnDone = True
                        await caster.mem.send("You have ended your turn")
                elif target2!=None and target!=target2: # two targets are not the same
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
                        caster.reacting = False
                    else:
                        caster.turnDone = True
                        await caster.mem.send("You have ended your turn")
                else: # if there's no target
                    await interaction.send(f"{caster.name} shielded themselves")
                    caster.shield+=2
                    print(f"{caster.name} was shielded to {caster.shield} shields")
            case "eldritch blast": # can't be avoided
                print(f"{interaction.user} casted {self.scrollName}")
                if target != None: # making sure there even is a target
                    await Rogues.reactCheck(Rogues,interaction,victim,caster,self,avoid=self.avoid)
                else: # if there's no target
                    print(self.scrollName)
                    await interaction.send("You need to target ONE person with this scroll. Either yourself or another player in the same room.")
                    return
            case "call lightning": # target two entities or one entity twice
                print(f"{interaction.user} casted {self.scrollName}")
                if target2 == None:
                    same = True
                else:
                    same = False
                if same:
                    await Rogues.reactCheck(Rogues,interaction,)
                if target2!=None:
                    if victim == v2:
                        same = True
                        await Rogues.reactCheck(Rogues,interaction,victim,caster,self,same=same,counter=self.counter)
                    else:
                        await Rogues.reactCheck(Rogues,interaction,victim,caster,self,v2,counter=self.counter)
                elif target != None: # making sure there even is a target
                    await Rogues.reactCheck(Rogues,interaction,victim,caster,self,same=True,counter=self.counter)
                else: # if there's no target
                    print(self.scrollName)
                    await interaction.send("You need to target ONE person with this scroll. Either yourself or another player in the same room.")
                    return
            case "dragon breath": # can't be blocked
                print(f"{interaction.user} casted {self.scrollName}")
                if target != None: # making sure there even is a target
                    victim = Rogues.identify(Rogues,target) # identify target player
                    await Rogues.reactCheck(Rogues,interaction,victim,caster,self,block=self.block)
                else: # if there's no target
                    print(self.scrollName)
                    await interaction.send("You need to target ONE person with this scroll. Either yourself or another player in the same room.")
                    return
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
                if target != None and target2==None:
                    healed = Rogues.identify(Rogues,target)
                    healed.shield+=1
                    same = caster.mem==target
                    if same:
                        await interaction.send(f"{caster.name} shielded themselves")
                        print(f"{healed.name} was shielded to {healed.shield} shields")
                    else:
                        await interaction.send(f"{caster.name} casted Magic Shield on {healed.name}!")
                        print(f"{healed.name} was shielded to {healed.shield} shields")
                    if caster.reacting==True:
                        await caster.mem.send("This is a reaction and will not use up your turn.")
                        caster.reacting = False
                    else:
                        caster.turnDone = True
                        await caster.mem.send("You have ended your turn")
                elif caster.reacting == True:
                    caster.shield+=1
                    await caster.mem.send(f"You shielded yourself.")
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
                    await caster.mem.send("You have used your scroll and ended your turn")
                else:
                    caster.hp+=1
                    if caster.hp >5:
                        caster.hp = 5
                        await interaction.send(f"Was there a purpose to that? You were full health...")
                    caster.turnDone = True
                    await caster.mem.send("You have used your scroll and ended your turn")
            case "holy shield":
                print(f"{interaction.user} casted {self.scrollName}")
                await caster.mem.send("You *truly* have the power of **God** on your side.")
                caster.shield +=5
                caster.turnDone = True
                await caster.mem.send("You have used your scroll and ended your turn")
            case "soul knot": # add implementation for this at LITERALLY the end of the game lol
                print(f"{interaction.user} casted {self.scrollName}") # Not limited to room and will expose death if target is dead.
                if target == None or caster == victim:
                    await caster.mem.send("You can **not** *knot* your soul with itself.")
                    return
                caster.soul = victim.name
                victim.soul = caster.name
                await caster.mem.send(f"Your soul is now linked with {victim.name}.\n**Regardless of any other factors** if you both are the only ones to make it out of the dungeon alive you both will be considered the winners of this excursion.\n**However if one of you dies. So to does the other.**")
                await victim.mem.send(f"Your soul is now linked with {caster.name}.\n**Regardless of any other factors** if you both are the only ones to make it out of the dungeon alive you both will be considered the winners of this excursion.\n**However if one of you dies. So to does the other.**")
            case "wish":
                print(f"{interaction.user} casted {self.scrollName}")
            case "za warudo":
                print(f"{interaction.user} casted {self.scrollName}")
            case _: #Default
                await interaction.send("That was not a valid name for a scroll. Orrrrrr something went wrong...tell my Master",ephemeral=True)
        caster.hand.remove(self)
        if str.lower(self.scrollName) == "soul knot":
            safeRoom.send("# Soul Knot has been used and will not be returned to the dungeon.")
        else:
            deck.append(self)
        await interaction.send(f"*Your {self.scrollName} has returned to the Dungeon*",ephemeral=True)
class Enemy:
    hp = 3
class Room:
    id = None
    name = None
# list of rooms I can randomize and then in second half I add the exit room to the list

#setup done outside the class
async def setup(bot):
    bot.add_cog(Rogues(bot))
# Notes:
# Need to make a tear down command at the end of all of this to wipe everything ADD MORE TO IT
# Need to make a death function to handle soul knot and other stuff
''' Player commands to check their stats DONE'''
'''Implement bot creating a text channel for dungeon and VCs for each room. Thinking to create a category for the game that the bot can then delete afterwards. DONE'''
'''Current idea is to have deck command make all the scrolls and for the ones with multiple counts to be done in a loop, that way I can pass the appropriate copy number. DONE'''
'''Each scroll will just be a function in the scroll class DONE'''
# find out how to update View and buttons for when scrolls are selected.
# When dealing with Rooms make an exit check that will happen each time a room has been entered by a player
# Need to make A LOT OF CHECKS primarily to see if a player has a spell(and which copy) in their hand ... after thinking on this one MAYBE
# Make a removeShields function for when the floor advances.

# raise RuntimeError("Task is already launched and is not completed.")
# RuntimeError: Task is already launched and is not completed.
# Idea: to catch run time error and make a temp timer
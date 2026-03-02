# TLDR of how this came to be. My friend had an idea for a game that we worked on in the past. For a game design course I was taking I was making it into a card game.
# I realized on the playtest for the card game that it kind of needed a DM. I figured I could make a discrod bot to manage the stuff I had to manage for the playtest.
# I thought this would be a good way to learn/get back into coding and here we are. 
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
deads = []
bads = 0
start = False
vote = 0
floor = []
floornum = 1
# Need a function to check if there is a game running already
async def ongoing(interaction:nextcord.Interaction):
    return ready == False
class Player:
    name="player"
    uid=0
    hp = 5
    hpDis = ""
    shield = 0
    shieldDis = "None"
    hand = [] # Players can hold a max of 5 scrolls
    handDis = ""
    Rogue = False
    turnDone = False
    mem = nextcord.Member # incase I need anything specific from discords member class
    reacting = False
    soul = ""
    dodge = False
    dCount = 0
    pRoom = None
    cRoom = None
    nRoom = None
    movement = True
    delve = False
    map = []
    greed = 0
    reborn = False
    pCount = 0
    bID = 0
    #potentially just add a player variable that is initially their discord uid and then increment that to use as custom ID for their buttons
    def __init__(self,player:nextcord.Member,uid):
        if player.nick!=None:self.name = player.nick
        else: self.name = player.name
        self.mem = player
        self.uid = uid
        self.hand = []
        self.hp = 5
        self.shield = 0
        self.turnDone = False
        self.handDis = ""
        self.hpDis = ""
        self.shieldDis="None"
        self.reacting = False
        self.soul = ""
        self.pRoom = None
        self.movement = True
        self.delve = False
        self.map = []
        self.greed = 0
        self.reborn = False
        self.pCount = 0
        self.bID = player.id
        print(self.bID)
        print("player created")
    def setRooms(self):
        self.nRoom = self.cRoom.next
    async def addScroll(self,scroll,interaction:nextcord.Interaction=None,gifter=None):
        if len(self.hand)<5:
            self.hand.append(scroll)
            scroll.owner = self.name
            print(f"{scroll.name} added to {self.name}'s hand")
        elif len(self.hand)==5:
            msg = await self.mem.send("You have the full amount of scrolls. You will need to decide what to do with the extra you have just received.")
            if gifter!=None:
                await Rogues.chooseScroll(Rogues,interaction,self,self.hand,victim=gifter,full=True,extra=scroll,msg=msg)
            else:
                await Rogues.chooseScroll(Rogues,interaction,self,self.hand,full=True,extra=scroll,msg=msg)
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
class Room:
    id = None
    name = None
    channel = nextcord.TextChannel
    next = []
    prev = []
    exit = False
    guests = []
    roomType = "" # monster loot trap exit
    cleared = False
    first = False # Bool for when the room was first entered
    def __init__(self,name,id,exit,roomType):
        self.id = id
        self.name = name
        self.exit = exit
        self.roomType = roomType
        self.cleared = False
        self.next = []
        self.prev = []
        self.guests = []
        self.channel = nextcord.TextChannel
        self.first = True
    def guestList(self):
        guestlist = ""
        for i in self.guests:
            guestlist += f"{i.name}----"
        return guestlist
    def getNext(self):
        return self.next
    def setNext(self,rooms):
        self.next=rooms
    def setPrev(self,rooms):
        self.prev=rooms
    async def event(self,user:Player=None):
        match (self.roomType):
            case "Safe":
                if self.first:
                    print(f"{self.roomType} event")# Event for Safe room will only be triggered as a result from delve moving to a new floor
                    match difficulty:
                        case 0:
                            msg = "I've created a safe spot in the dungeon for this floor. Please discuss with your party members and head out to find the exit to the next floor."
                        case 1:
                            msg = "We should regroup here. Something about that chest felt cursed."
                        case 2:
                            msg = f"My suspicions have been confirmed. That chest a while ago was indeed cursed. {bads} of your party members have been cursed to let out their inner greed. I fear they are planning to eliminate the rest of you. As we reach saferooms like this one I will allow the party to discuss for a few minutes and hold a vote. I will trap whoever is voted into a *Magic Jail* where they will remain until we make it out of this dungeon. They will not die but they will not be a participant in this expedition any longer."
                        case 3:
                            msg = "I have created another safe room. Please decide whether someone should be *Magic Jailed*"
                    await Rogues.talk(Rogues,msg,self)
                else:
                    await self.channel.send("Welcome back to The Saferoom")
            case "Loot":
                print(f"{self.roomType} event")# Event for rooms with a chest in them
                await self.channel.send(f"{user.name} has chosen to open the treasure chest. Everyone in the room will now be rewarded.")
                for i in self.guests:
                    await Rogues.deal(Rogues,i,True)
                    if len(self.guests)==1:
                        i.greed +=1
                    await self.channel.send(f"{i.name} has been gifted a scroll by the dungeon and grabbed some treasure for themselves.")
            case "Monster":
                print(f"{self.roomType} event")# Event for rooms with an enemy in them
                await self.channel.send("There is a monster in this room.\n*But I haven't implemented that yet soooooo uhhhh You're allowed to just move on.*\n*You can move again now*")
                for i in self.guests:
                    i.movement = True
                # Plan to make a whole battle view with buttons that will essentially mirror casting/reacting this will also manage the enemy turn.
            case "Exit":
                print(f"{self.roomType} event")# Event for the Exit Rooms
                #idea: Once the exit room is found the other rooms in the dungeon that are dead ends now lead to the exit room.
                await self.channel.send("You have found the exit room!!\n*You can feel the dungeon shifting*\nYou can explore other areas of the dungeon to try to inform your party of where the exit is or you can wait for them to catch up.")
                for i in floor:
                    if i.nRoom == None:
                        i.nRoom = self
            case "Magic":
                print(f"{self.roomType} event")# Event for the Exit Rooms in the beginning
                await self.channel.send("You have reached the end of the floor. Please wait for the other")
            case "Evil": #I was originally thinking of having opening the chest be optional but I think I'll keep track of who has gotten the most "loot" and they will be the greediest player and I will frame it as them opening the chest.
                print(f"{self.roomType} event")# Event for THE room. Implement later
                await self.channel.send("The party arrives at an empty room with nothing but a singular chest inside. ")
            case _:
                print("Something went wrong running the events for a room.")
                await self.channel.send("This is not a special room? something went wrong.")
class Rogues(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    async def make(self,interaction:nextcord.Interaction):
        await interaction.send("Setting up Game...")
        try:
            msg = await interaction.original_message()
            global category
            category = await guild.create_category("Rogues Category")
            await msg.edit(content="Creating the category and channels. Please remember to have a moderator use the ?teardown command when the game is done.")
            msg.content="Creating the category and channels. Please remember to have a moderator use the ?teardown command when the game is done."
            print(f"Category {category.name} created successfully!")
            global safeRoom
            safeRoom = await guild.create_text_channel(name="safe-room",category=category,position=0,topic="Room for the party to discuss and make decisions",overwrites={everyone:nextcord.PermissionOverwrite(view_channel=False,read_messages=False,send_messages=False),playerRole:nextcord.PermissionOverwrite(view_channel=True,read_messages=True,send_messages=True)})
            global safe
            safe = Room(name="The Saferoom",id=0,exit=False,roomType="Safe")
            safe.channel = safeRoom
            global safeVC
            safeVC = await guild.create_voice_channel(name="Safe VC",category=category,overwrites={everyone:nextcord.PermissionOverwrite(view_channel=False,connect=False,read_messages=False,send_messages=False),playerRole:nextcord.PermissionOverwrite(view_channel=True,connect=True,read_messages=True,send_messages=True)})
            roomA = await self.createRoom()
            roomB = await self.createRoom()
            roomC = await self.createRoom(exit=True)
            safe.next = [roomA,roomB]
            roomA.next = [roomC]
            roomA.prev = [safe]
            roomB.prev = [safe]
            roomB.next = [roomC]
            roomC.prev = [roomA,roomB]
            for i in players:
                i.cRoom = safe
                i.nRoom = safe.next
                i.map.append(safe)
                safe.guests.append(i)
            story = "Welcome party members! I am Beru and I will be guiding you through this magical dungeon. I understand many of you did not want to leave your equipment outside but thank you for following my instructions. Many do not believe me when I saw this but this dungeon IS alive. As such thank you all for leaving your equipment with my clone. __This dungeon is special. Your brand of traditional magic and conventional weaponry will not work in this dungeon. **You can ONLY use the scrolls the dungeon provides.**__ The dungeon may offer rewards but it also is wrought with monsters and traps. Do your best to survive as you all explore the dungeon. Rest assured I am more than enough to protect your belongings while we are gone. As we go through the dungeon I will split myself into smaller clones to travel with each of you individually. If one of you perishes in the dungeon the clone will return to me and I will notify everyone that someone in the party has died.\nI wish you all luck as you explore the dungeon."
            await Rogues.talk(self,story,safe)
            await msg.edit(content=f"{msg.content}\nYou may now assemble in the {safeRoom.mention} OR VC")
        except Exception as e:
            print(f"220 Before Make finished. An error occured: {e}")
    async def addPlayer(self,player:nextcord.Member,uid):
        match uid:
            case 1:
                await player.add_roles(playerRole)
                player1 = Player(player,uid)
                players.append(player1)
                print(f"player {uid} {player1.name}")
            case 2:
                await player.add_roles(playerRole)
                player2 = Player(player,uid)
                players.append(player2)
                print(f"player {uid} {player2.name}")
            case 3:
                await player.add_roles(playerRole)
                player3 = Player(player,uid)
                players.append(player3)
                print(f"player {uid} {player3.name}")
            case 4:
                await player.add_roles(playerRole)
                player4 = Player(player,uid)
                players.append(player4)
                print(f"player {uid} {player4.name}")
            case 5:
                await player.add_roles(playerRole)
                player5 = Player(player,uid)
                players.append(player5)
                print(f"player {uid} {player5.name}")
            case 6:
                await player.add_roles(playerRole)
                player6 = Player(player,uid)
                players.append(player6)
                print(f"player {uid} {player6.name}")
            case 7:
                await player.add_roles(playerRole)
                player7 = Player(player,uid)
                players.append(player7)
                print(f"player {uid} {player7.name}")
            case 8:
                await player.add_roles(playerRole)
                player8 = Player(player,uid)
                players.append(player8)
                print(f"player {uid} {player8.name}")
            case 9:
                await player.add_roles(playerRole)
                player9 = Player(player,uid)
                players.append(player9)
                print(f"player {uid} {player9.name}")
            case _:
                print("Not a discord member or Too many players")
        return uid+1
    def identify(self,player:nextcord.Member=None,name:str=None): #function to identify discord Member to Player class counterpart
        if player!=None:
            for i in players:
                if player == i.mem:
                    return i
        else:
            for i in players:
                if name == i.name:
                    return i
    async def talk(self,speech:str,room:Room=None,msg:nextcord.message=None,done=False): #command I'm going to use for exposition from the bot
        MyEmbed = nextcord.Embed(title ="Beru the Guide",description = "The Guide has something to say.",color = nextcord.Colour(0xFFD700))
        MyEmbed.set_thumbnail(url=self.bot.user.avatar.url)
        MyEmbed.add_field(name="Beru says:", value=speech,inline=False)
        if done:
            return MyEmbed
        else:
            if msg != None:
                await msg.edit(embed=MyEmbed)
            else:
                await room.channel.send(embed=MyEmbed)
    def Deck(self): #create the "deck" of scrolls for the dungeon
        print("Creating Deck") # counter block avoid
        self.createScroll("Fireball","Offensive",True,True,True,7,"So anyway I started blasting.","A basic attack spell.","Beru-Bot/Resources/fireball.png",1,True) # 7 Fireball can be countered blocked and avoided
        self.createScroll("Eldritch Blast","Offensive",True,True,False,5,"Almost as good as that Ghost Boy","A cryptic attack that always finds it's target.","Beru-Bot/Resources/eldritch.png",1,True) # Can't be avoided
        self.createScroll("Call Lightning","Offensive",False,True,True,5,"Talk about a STATIC SHOCK","Summon magical lightning bolts from above that can not be countered.","Beru-Bot/Resources/callliightning.png",2,True,True) # Can't be countered
        self.createScroll("Dragon Breath","Offensive",True,False,True,5,"Girl dragons are just Reeking of feminine beauty","A flame so hot it bypasses through shields of any kind.","Beru-Bot/Resources/dragonsbreath.png",1,True) # Can't be blocked
        self.createScroll("Explosion","Offensive",False,True,False,1,"爆裂爆裂ラララ","Summon an extremely powerful explosion that hurts everyone in the room. This spell can only be avoided by Teleport.","Beru-Bot/Resources/explosion.png",3) # This was a late addition back when it was a card game so I had forgotten to add it to the bot
        self.createScroll("Smite","Offensive",False,True,False,3,"You're God!", "Wield divine energy to smite ANY other player regardless of what room they are in. However this is only if you are able to *divine* the location of the player. If you are wrong you will be punished.","Beru-Bot/Resources/smite.png",2,True) # I had this idea today while making the message for if a player tries to attack someone in another room.
        self.createScroll("Holy Shield","Defensive",False,False,False,1,"Nothing can pierce my Holy Pope Box","A shield of Divinity.\n*Grants +5 shields*","Beru-Bot/Resources/holyshield.png",3) # Super Strong long lasting shield. numbers will be worked out later
        self.createScroll("Teleport","Defensive",False,False,False,6,"What the hell is all this black stuff on me?","A spell that can be used to return to a previous room or avoid an attack.","Beru-Bot/Resources/teleport.png",1) # 6 teleport scrolls it can not be countered blocked or avoided (it's not an attack or aimed at anyone)
        self.createScroll("Counter","Defensive",False,True,True,7,"*FULL Counter*","A spell that can be used to counter attack someone that tried to cast a spell at you.","Beru-Bot/Resources/counter.png",1) # Counter spell can be blocked and avoided but not countered
        self.createScroll("Mold Earth","Defensive",False,False,False,3,"THE BOULDER is conflicted","A defensive type of spell that can grant a shield to two different people or you can double up on one person or yourself","Beru-Bot/Resources/moldearth.png",2,True,True) # Covers two players #
        self.createScroll("Barbarian Rage","Defensive",False,False,False,3,"IMPOTENT RAGE!!!\n-# does not actually make you impotent","A spell that activates the dormant barbarian rage that sleeps in anyone. Allowing them to shield through attacks out of sheer anger.\n*Gives 2 shields*","Beru-Bot/Resources/barbarianrage.png",2) # Blocks TWO instances of damage
        self.createScroll("Invisibility","Defensive",False,False,False,3,"If I can't see them, then they can't see me.","You can go invisible to avoid attacks or cast it preemptively to be invisible for a limited time.","Beru-Bot/Resources/invisibility.png",2) # Rogues have extra perks with invis
        self.createScroll("Magic Shield","Defensive",False,False,False,6,"No you are not the Shield Hero","Project a magical shield that will protect you from a single attack.\n*Gives 1 shield*","Beru-Bot/Resources/magicshield.png",1,True) # Blocks a spell
        self.createScroll("Cure Wounds","Ancillary",False,False,False,4,"Just don't seek revenge...","Heal yourself or others.\n*Gives 1 HP*","Beru-Bot/Resources/curewounds.png",1,True) # heal 
        self.createScroll("Polymorph","Ancillary",True,False,False,2,"Now that I don't have a brain I don't even know what that means.","Turn your opponent into a useless wad of meat. They will be unable to complete actions for a limited time.","Beru-Bot/Resources/polymorph.png",2,True) # Prevent another player from taking action twice CAN only be countered.
        self.createScroll("Scrying","Ancillary",False,False,False,4,"I CAN SEE THE FUTURE","Casting this spell will allow you to see one of the scrolls of your target. But they get to choose.","Beru-Bot/Resources/scrying.png",1,True) # The target chooses which scroll to show
        self.createScroll("Divine Wisdom","Ancillary",False,False,False,3,"Filthy Ningen","Learn which scrolls your target owns currently.","Beru-Bot/Resources/divinewisdom.png",3,True) # Reveal all scrolls of one chosen player to the user
        self.createScroll("Wish","Ancillary",False,False,False,1,"","","Beru-Bot/Resources/wish.png",3) # TBD
        self.createScroll("Za Warudo","Ancillary",False,False,False,1,"","","Beru-Bot/Resources/zawarudo.png",3) # when prompting defensive scrolls need to also check for this.
        self.createScroll("Soul Knot","Ancillary",False,False,False,1,"Anything for my Senpai","Tie your soul and destiny to another player.","Beru-Bot/Resources/soulknot.png",3,True) # Link to another player when one dies the other dies but if they are both the only two to get out then they both win.
        if evil == True:
            self.createScroll("Steal","Offensive",False,False,True,4,"Please don't steal someone's panties.","Steal a random scroll from your target","Beru-Bot/Resources/steal.png",1,True) # TBD
            self.createScroll("Blood Altar","Offensive",False,False,False,3,"A fine tribute to the Gore Queen Garuda","Sap health from your enemy if damage is dealt to enemy health.","Beru-Bot/Resources/bloodaltar.png",2,True) # Sap Health if uninterupted. Won't heal if it is CBA
        sn = 0
        for i in deck:
            self.serialize(i,sn) # Add serial number to the Scrolls to further help keep track of. Not sure if I'll need this tbh kinda just an added precaution in case it comes in handy
            sn +=1
        print("Deck created")
    def createScroll(self,name,type,counter,block,avoid,count,flavor="If you see this I fucked up",effect="This spell does...something",image="image url here",rank=0,aim=False,aim2=False): # Function to create scrolls for the game
        i = 0
        global deck
        while (i < count):
            deck.append(Scroll(name,type,counter,block,avoid,i+1,count,flavor,effect,image,aim,aim2)) # Create Scroll and add it to the deck
            i+=1
    def serialize(self,scroll,sn):
        scroll.serial = sn
    async def deal(self, player,loot=False):
        if loot:
            dealt = random.choice(deck)
            deck.remove(dealt)
            await player.addScroll(dealt)
        else:
            print(f"Dealing to {player.name}:")
            for i in range(0,3): # Deal 3 scrolls at the start of the game
                dealt = random.choice(deck) # randomly pick a scroll
                deck.remove(dealt) # remove the scroll from the deck
                await player.addScroll(dealt) # add the scroll to the player's hand
    async def createRoom(self,exit=False):
        RC = len(floor)
        if exit:
            if difficulty==0:
                room = Room(name=f"Magic{RC}",id=RC,exit=True,roomType="Magic")
            else:
                room = Room(name=f"Exit{RC}",id=RC,exit=True,roomType="Exit")
        else:
            match (difficulty): #unsure how I want to tackle the exit situation.
                case 0:
                    types = ["Monster","Loot","Trap"]
                    weight = [0.15,0.80,0.05]
                    room = random.choices(types,weight,k=1)
                    room = Room(name=f"Room{RC}",id=RC,exit=False,roomType=str(room[0]))
                case 1:
                    types = ["Monster","Loot","Trap"]
                    weight = [0.4,0.4,0.2]
                    room = random.choices(types,weight,k=1)
                    room = Room(name=f"Room{RC}",id=RC,exit=False,roomType=str(room[0]))
                case 2:
                    types = ["Monster","Loot","Trap"]
                    weight = [0.33,0.34,0.33,]
                    room = random.choices(types,weight,k=1)
                    room = Room(name=f"Room{RC}",id=RC,exit=False,roomType=str(room[0]))
                case 3:
                    types = ["Monster","Loot","Trap"]
                    weight = [0.4,0.20,0.4]
                    room = random.choices(types,weight,k=1)
                    room = Room(name=f"Room{RC}",id=RC,exit=False,roomType=str(room[0]))
                case _:
                    await safeRoom.send("Something went wrong creating a room")
        room.channel = await guild.create_text_channel(name=room.name,category=category,position=RC,topic="A random room in the dungeon.",overwrites={everyone:nextcord.PermissionOverwrite(view_channel=False,read_messages=False,send_messages=False)})
        floor.append(room)
        return room
    def findRoom(self,name:str):
        for i in floor:
            if i.name == name:
                return i
    async def overwrite(self,room:nextcord.TextChannel,caster:Player,block:bool=False,vc:nextcord.VoiceChannel=None):
        if block:
            await room.set_permissions(caster.mem,view_channel=False,read_messages=False,send_messages=False)
            print(f"Permissions for {room.name} updated for {caster.name} to Block.")
            if vc!=None:
                await vc.set_permissions(caster.mem,view_channel=False,read_messages=False,send_messages=False)
                print(f"Permissions for {room.name} updated for {caster.name} to Block.")
        else:
            await room.set_permissions(caster.mem,view_channel=True,read_messages=True,send_messages=True)
            print(f"Permissions for {room.name} updated for {caster.name} to Allow.")
            if vc!=None:
                await vc.set_permissions(caster.mem,view_channel=True,read_messages=True,send_messages=True)
                print(f"Permissions for {room.name} updated for {caster.name} to Allow.")
    def deckWeight(self,deck): # I want to make a function to modify the weight of each scroll in the deck. I will either use this specifically when the difficulty changes or everytime Enemy Loottable is triggered.
        #weighted = list() ---------- Originally thought I needed this but I don't think I do
        weights = []
        c = 0
        r = 0
        u = 0
        match difficulty:
            case 1:
                c = 0.6
                r = 0.39
                u = 0.1
            case 2:
                c = 0.45
                r = 0.45
                u = 0.1
            case 3:
                c = 0.35
                r = 0.45
                u = 0.2
            case _:
                c = 0.7
                r = 0.3
        for i in deck:
            if i.rariry =="Common":
                #weighted.append(deck[i])
                weights.append(c)
            if i.rarity == "Rare":
                #weighted.append(deck[i])
                weights.append(r)
            if i.rarity == "Unique":
                #weighted.append(deck[i])
                weights.append(u)
        return weights
    @commands.command()
    @commands.check(is_me)
    async def reset(self,ctx,member:nextcord.Member):
        print(member)
        redo = self.identify(player=member)
        print(isinstance(redo,Player))
        redo.turnDone = False
        redo.movement = True
    @commands.command()
    @commands.check(is_me)
    async def bless(self,ctx,scroll:str,mem:nextcord.Member=None): #for now this is a test command for me
        if mem ==None:
            player = self.identify(ctx.author)
        else:
            player = self.identify(mem)
        for i in deck:
            if i.name == scroll:
                dealt = i
                deck.remove(dealt)
                await player.addScroll(dealt)
                break
    '''@bless.error
    async def errorhandler(ctx:nextcord.Interaction,error):
        if isinstance(error,nextcord.errors.ApplicationCheckFailure):
            await ctx.send("You're not my Master!")'''
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
        else:
            await interaction.response.defer()
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
        global difficulty
        difficulty = 0
        global uid
        uid=0
        j = 1
        for i in people:
            j = await self.addPlayer(i,j)
        match int(len(people)/2):#how many rogues there will be
            case 2:
                bads = 1
            case 3:
                bads = 2
            case 4:
                if len(people)>8: bads=3
                else:
                    bads = 2
            case _:
                print("Something happened")
        del people
        # Need to get the bot to create the channels.
        self.Deck()
        # Need to add Map related stuff
        await self.make(interaction)
        await safeRoom.send("The dungeon has supplied magic scrolls to help the party.")
        for i in players:
            await self.deal(i)
    @RogueGame.error
    async def errorhandler(ctx:nextcord.Interaction,error):
        if isinstance(error,nextcord.errors.ApplicationCommandOptionMissing):
            await ctx.send("Not enough players.")
    @nextcord.slash_command(name="teardown",description="End the game")
    @application_checks.check(is_me or ongoing)    
    async def teardown(self,interaction:nextcord.Interaction):
        await interaction.response.send_message("Shutting down Game...")
        global safe
        del safe
        await playerRole.delete()
        for i in category.channels:
            await i.delete()
        await category.delete()
        for x in floor:
            del x
        print("g")
        for k in players:
            for l in k.hand:
                l.remove()
                deck.append(l)
            del k
        for j in deck:
            del j
        print("o")
        global ready
        ready = True
        deck = []
        global evil
        evil = False
        players = []
        global deads
        deads = []
        global bads
        bads = 0
        global start
        start = False
        global vote
        vote = 0
        floor = []
        global floornum
        floornum = 1
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
    async def cast(self,interaction:nextcord.Interaction):
        caster = self.identify(interaction.user)
        if caster.pCount>0:
            await caster.mem.send(f"You are polymorphed the only actions you can take are moving to different rooms and ending your turn. You have {caster.pCount} turns left as a meatball.")
            await interaction.send(f"{caster.name} forgot they were a sentient meatball and can not do any actions.")
            return
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
        for i in players:
            if i.turnDone == True:
                await Rogues.dungeon()
    @player.subcommand(description="Display your stats")
    async def stats(self,interaction:nextcord.Interaction):
        caster = self.identify(interaction.user)
        caster.hpDis = ""
        caster.shieldDis = "None"
        caster.handDis = ""
        i=0
        while i < caster.hp:
            caster.hpDis = caster.hpDis + ":heart:"
            i+=1
        i=0
        if caster.shield ==0: caster.shieldDis = "None" 
        else: caster.shieldDis = ""
        while i < caster.shield:
            caster.shieldDis = caster.shieldDis + ":shield:"
            i+=1
        caster.handDis = ""
        if len(caster.hand)==0: 
            caster.handDis = "You have no scrolls. I'm surprised that you're even still alive."
        i=0
        while i < len(caster.hand):
            if len(caster.hand)==1:
                caster.handDis = f"{i+1}. **{caster.hand[i].name}** a(n) __{caster.hand[i].type}__ type of spell\n"
            elif i == len(caster.hand):
                break
            elif i == len(caster.hand)-1:
                caster.handDis = caster.handDis + f"{i+1}. **{caster.hand[i].name}** a(n) __{caster.hand[i].type}__ type of spell\n-# You can use the view command to inspect your scrolls"
            else:
                caster.handDis = caster.handDis + f"{i+1}. **{caster.hand[i].name}** a(n) __{caster.hand[i].type}__ type of spell\n"
            i+=1
        MyEmbed = nextcord.Embed(title = caster.name, description = "These are your stats",color = nextcord.Colour(0xFFD700))
        MyEmbed.set_thumbnail(url=caster.mem.display_avatar.url)
        MyEmbed.add_field(name="HP:heart:", value=caster.hpDis,inline=True)
        MyEmbed.add_field(name="Shields:shield:", value=caster.shieldDis,inline=True)
        MyEmbed.add_field(name="PlayerID",value=caster.uid,inline=True)
        if caster.Rogue:
            MyEmbed.add_field(name="Evil?",value="Yes",inline=True)
        if caster.dCount>0:
            MyEmbed.add_field(name="Invis?",value=f"{caster.dCount} turn(s)",inline=True)
        if caster.soul != "":
            MyEmbed.add_field(name="Soulmate?", value=caster.soul,inline=True)
        MyEmbed.add_field(name="Current room",value=caster.cRoom.name,inline=True)
        MyEmbed.add_field(name="Owned Scrolls",value=caster.handDis,inline=False)
        await interaction.response.send_message(embed=MyEmbed,ephemeral=True)
    @player.subcommand(description="Duel another player")
    async def duel(self,interaction:nextcord.Interaction,target:nextcord.Member):
        caster = self.identify(interaction.user)
        if caster.pCount>0:
            await caster.mem.send(f"You are polymorphed the only actions you can take are moving to different rooms and ending your turn. You have {caster.pCount} turns left as a meatball.")
            await interaction.send(f"{caster.name} forgot they were a sentient meatball and can not do any actions.")
            return
        victim = self.identify(target)
        await interaction.response.send_message(f"I have sanctioned a duel between {caster.name} and {victim.name}\nAll attacks made on these two will no longer work until the duel is over.\nI can not allow you to hear them but I will commentate if you would like to stay and await the thrilling conclusion.")
        #Need to add duel checks to EVERYTHING and a timer for the loser. I'm thinking they can duel over loot they find or freely duel to get scrolls from each other.
    @player.subcommand(name="view",description="Inspect one of your scrolls.")
    async def info(self,interaction:nextcord.Interaction):
        caster = self.identify(interaction.user)
        await self.chooseScroll(interaction,caster=caster,scrolls=caster.hand,info=True)
    @player.subcommand(name="move",description="Move to a new room.")
    async def move(self,interaction:nextcord.Interaction):
        # Change movement to false and set up system so that when all players end their turn they all reset turn(dungeon does it's turn first but so far no enemies yet.)
        caster = self.identify(interaction.user)
        if caster.movement == False:
            print("already moved")
            await interaction.response.send_message("You have already moved in this turn you will need to end your turn before you can move on.")
            return
        if caster.nRoom != []:
            if caster.cRoom.roomType == "Monster":
                print("monster room")
                if caster.cRoom.cleared == False:
                    print("not cleared yet M")
                    await interaction.response.send_message("You must deal with the monster in the room first.")
                    #return
            if caster.cRoom.roomType == "Loot":
                print("leaving loot room")
                await caster.mem.send("You are leaving the loot behind. It may not be here when/if you return.")
            print(caster.nRoom)
            MyEmbed = nextcord.Embed(title = caster.name, description = "Where you can move to...",color = nextcord.Colour(0x6f00eb))
            MyEmbed.set_thumbnail(url=caster.mem.display_avatar.url)
            moving = Rogues.mView(interaction,caster)
            await interaction.send(embed=MyEmbed,view=moving)
        else:
            print("No next room. Go back or wait?")
            MyEmbed = nextcord.Embed(title = caster.name, description = "Where you can move to...",color = nextcord.Colour(0x6f00eb))
            MyEmbed.set_thumbnail(url=caster.mem.display_avatar.url)
            print("to view?")
            moving = Rogues.mView(interaction,caster,prev=True)
            await interaction.response.send_message(embed=MyEmbed,view=moving)
    @player.subcommand(name="delve",description="Delve to the next floor of the dungeon")
    async def delve(self,interaction:nextcord.Interaction):
        # it removed all the channels except saferoom(including VC)
        caster = self.identify(interaction.user)
        vote = 0
        if caster.cRoom.exit == True:
            caster.delve = True
        for i in players:
            if i.delve:
                vote+=1
            if i.cRoom.exit == False:
                await interaction.response.send_message("Not all players are in the exit room. Please wait.")
                #implement group drag here.
        if vote >= len(players)/2:
            await self.newFloor()
    @player.subcommand(name="loot",description="This command can only be used in Loot type rooms.")
    async def loot(self,interaction:nextcord.Interaction):
        caster = self.identify(interaction.user)
        if caster.pCount>0:
            await caster.mem.send(f"You are polymorphed the only actions you can only take actions similar to moving to different rooms, viewing and sharing scrolls, and ending your turn. You have {caster.pCount} turns left as a meatball.")
            await interaction.send(f"{caster.name} forgot they were a sentient meatball and can not do any actions.")
            return
        if(caster.cRoom.roomType == "Loot"):
            caster.cRoom.event(caster)
        else:
            await interaction.response.send_message("You are not in a Loot room.")
    #idea for a map command the player can use
    @player.subcommand(name="map",description="This is your personal map. It will update as you explore.")
    async def path(self,interaction:nextcord.Interaction):
        caster = self.identify(interaction.user)
        MyEmbed = nextcord.Embed(title = caster.name, description = "This is your path.",color = nextcord.Colour(0xFFD700))
        MyEmbed.set_thumbnail(url=caster.mem.display_avatar.url)
        first = True
        if caster.map == [safe]:
            await interaction.response.send_message("You have not explored the dungeon yet...get off your ass.")
            return
        else:
            for i in caster.map:
                if first:
                    path = "The Saferoom"
                    first = False
                elif i == safe:
                    path = f"{path}-->The Saferoom"
                else:
                    path = f"{path}-->**{i.name}** a(n) **{i.roomType}** room"
        print("path done?")
        MyEmbed.add_field(name=f"Floor {floornum}",value=f"__Pathing:__\n{path}",inline=False)
        print ("embed done")
        await interaction.response.send_message(embed=MyEmbed,ephemeral=True)
    @player.error
    async def errorhandler(ctx:nextcord.Interaction,error):
        if isinstance(error,nextcord.errors.ApplicationCheckFailure):
            await ctx.send("There isn't a game happening right now.")
    async def moving(self,fro:Room,to:Room,who:Player,tele=False):
        if who.mem in safeVC.members:
            await who.mem.disconnect()
        else:
            pass
        print(fro.name)
        print(fro.guestList())
        fro.guests.pop(fro.guests.index(who))
        to.guests.append(who)
        who.map.append(to)
        who.cRoom = to
        who.pRoom = fro
        who.nRoom = to.next
        if fro == safe:
            print("from safe")
            await Rogues.overwrite(Rogues,fro.channel,who,True,safeVC)
            await Rogues.overwrite(Rogues,to.channel,who)
        elif to == safe:
            print("to safe")
            await Rogues.overwrite(Rogues,fro.channel,who,True)
            await Rogues.overwrite(Rogues,to.channel,who,False,safeVC)
        else:
            print("no safe")
            await Rogues.overwrite(Rogues,to.channel,who)
            await Rogues.overwrite(Rogues,fro.channel,who,True)
        if tele == False:
            who.movement = False
        if to.roomType == "Loot" or to.roomType == "Magic" or to.roomType == "Exit":
            await to.channel.send(f"*{who.name} entered this {to.roomType} room!*")
        else:
            await to.channel.send(f"*{who.name} entered this {to.roomType} room!*")
            await to.event(who)
    async def damage(self,victim,avoided=False,attacker=None,baku=False,block=True,smite=False):
        if baku:
            damage = 3
        elif smite:
            damage = 2
        else:
            damage = 1
        if victim.shield>0:
            if block:
                if avoided:
                    if baku:
                        await victim.mem.send("In the nick of time you teleported away from the explosion in the other room.")
                    else:
                        await victim.mem.send(f"You have avoided damage.")
                else:
                    if baku:
                        if damage > victim.shield:
                            damage-=victim.shield
                            victim.shield = 0
                            explode = await victim.mem.send(f"You have taken damage from the explosion caused by {attacker.name}. A portion of the damage has been blocked by your shields, but not all of it.")
                            victim.health-=damage
                            await explode.edit(f"{explode.content}\nYou have also taken {damage} health damage from the explosion.")
                        elif victim.shield > damage:
                            victim.shield-=damage
                            damage = 0
                            explode = await victim.mem.send(f"You managed to block all of the damage from {attacker.name}'s explosion using your shields.")
                        else:
                            victim.shield = 0
                            damage = 0
                            explode = await victim.mem.send(f"You had EXACTLY enough shields to block all of the damage from {attacker.name}'s explosion.")
                    else:
                        victim.shield-=damage
                        await victim.mem.send(f"You have taken damage that was blocked by one of your shields.")
            else:
                if avoided:
                    await victim.mem.send(f"You have avoided damage.")
                else:
                    await victim.mem.send("This attack cannot be blocked. You will take damage to your health regarless of your shields.")
                    victim.hp-=damage
        else:
            if baku:
                if avoided:
                    await victim.mem.send("In the nick of time you teleported away from the explosion in the other room.")
                else:
                    victim.hp-=damage
                    await attacker.cRoom.channel.send(f"{victim.name} was caught in the explosion!")
                    await victim.mem.send(f"You were caught in {attacker.name}'s Explosion")
            else:
                if avoided or victim.dCount>0:
                    await victim.mem.send(f"You have avoided damage.")
                    if victim.dCount>0:
                        victim.dCount -=1
                        if victim.dCount == 0:
                            await victim.mem.send(f"You have used up your invisibility.")
                else:
                    victim.hp-=damage
                    if smite:
                        await victim.cRoom.channel.send(f"{victim.name} was smited by the Gods")
                        await victim.mem.send(f"{attacker.name} communed with the Gods to smite you")
                    else:
                        await victim.mem.send(f"You have taken damage.")
        if victim.hp == 0 or victim.hp <0:
            if victim.soul != "":
                # kill both
                soul = Rogues.identify(Rogues,name=victim.soul)
                await Rogues.death(Rogues,victim,attacker,victim.reborn,soul)
                print("death for both")
            else:
                # make a death function
                await Rogues.death(Rogues,victim,attacker,victim.reborn)
    async def death(self,victim,killer=None,wish=False,soul=None):
        #await safeRoom.send(f"{victim.name} has perished.")
        await victim.cRoom.channel.send(f"{victim.name} has perished.")
        if killer != None: # if there is a killer
            if killer == soul: # if the killer is stupid
                await killer.mem.send("That was one of the decisions of all time...You murdered your own soul mate...for some reason. Well now you both die. Good job")
                deads.append(soul)
                soul.hp = 0
                soul.shield = 0
                for i in victim.hand:
                    victim.hand.remove(i)
                    i.owner = None
                    deck.append(i)
                await Rogues.death(Rogues,soul,wish=soul.reborn)
            else:
                msg = await killer.mem.send(f"You have murdered {victim.name}. You have earned one of their scrolls.")
                if killer.Rogue:
                    # Make a view for them to choose the scroll they want from the victim's hand.
                    print("Rogue kill")
                else:
                    loot = random.choice(victim.hand)
                    await killer.addScroll(loot)
                    await msg.edit(content=f"{msg.content}\nYou have received {victim.name}'s {loot.name} scroll")
                killer.greed +=1
        for i in victim.hand: # empty the dead's hand
            victim.hand.remove(i)
            i.owner = None
            deck.append(i)
        if soul != None: # if there's a soulmate
            soul.mem.send("Your soulmate has perished. As a result you have died as well.\nYour scrolls have returned to the dungeon.")
            soul.hp = 0
            soul.shield = 0
            await Rogues.death(Rogues,soul,wish=soul.reborn)
        if wish: # wish check for being reborn
            await victim.cRoom.channel.send(f"{victim.name} died and like a Phoenix from the ashes they were immediately reborn.")
            Rogues.deal(Rogues,victim)
            return
        players.pop(victim.uid)
        victim.mem.remove_roles(playerRole)
        deads.append(victim)
    class mView(nextcord.ui.View):
        def __init__(self,oginter,caster,smite=False,victim=None,prev=False):
            super().__init__(timeout=60)
            self.oginter = oginter
            self.caster = caster
            self.prev = prev
            if smite: # Smite in this view is a whole different bag of special.
                self.smite = True
            else:
                self.smite = False
            if smite:
                for i in floor:
                    print("move bID testing")
                    bID = f"{caster.bID}"
                    caster.bID += 1
                    self.add_item(Rogues.mButt(caster=caster,smite=smite,victim=victim,label=i.name,style=nextcord.ButtonStyle.green,custom_id=bID))
            else:
                if prev == False: # I'll be honest I kinda forogot why I added a prev bool and put it in the buttons as well so for now it's used for this.
                    for i in caster.nRoom:
                        bID = f"{caster.bID}"
                        caster.bID += 1
                        self.add_item(Rogues.mButt(caster=caster,label=i.name,style=nextcord.ButtonStyle.green,custom_id=bID))
                    if self.caster.cRoom.prev != []:
                        bID = f"{caster.bID}"
                        caster.bID += 1
                        self.add_item(Rogues.mButt(caster=caster,label="Previous Rooms",style=nextcord.ButtonStyle.red,custom_id=bID))
                else: # This is for when they're in a dead end room
                    for i in caster.cRoom.prev:
                        bID = f"{caster.bID}"
                        caster.bID += 1
                        self.add_item(Rogues.mButt(caster=caster,label=i.name,style=nextcord.ButtonStyle.green,custom_id=bID,prev=True))
                    bID = f"{caster.bID}"
                    caster.bID += 1
                    self.add_item(Rogues.mButt(caster=caster,prev=True,label="Next Rooms",style=nextcord.ButtonStyle.blurple,custom_id=bID))
        async def on_timeout(self):
            print("Move View Timeout")
            if self.smite:
                await self.caster.cRoom.channel.send(f"## Indecisiveness is Cowardice\nThe Gods have witnessed {self.caster.name}'s failure and have decided to cast judgement.")
                await Rogues.damage(Rogues,self.caster,smite=True)
            for i in self.children:
                i.disabled = True
            await self.oginter.edit_original_message(view=self)
            self.stop()
    class mButt(nextcord.ui.Button):
        def __init__(self,caster,smite=False,prev=False,label="",style=nextcord.ui.Button.style,custom_id=None,victim=None):
            super().__init__(label=label,style=style,custom_id=custom_id)
            self.caster = caster
            self.label = label
            self.style = style
            self.custom_id = custom_id
            self.smite = smite
            self.prev = prev
            if victim!=None:
                self.victim=victim
        async def callback(self,interaction:nextcord.Interaction):
            if Rogues.identify(Rogues,interaction.user).uid != self.caster.uid:
                print("Wrong person. mButt")
                return
            await interaction.response.defer()
            if self.smite:
                room = Rogues.findRoom(Rogues,self.label)
                if self.victim.cRoom == room:
                    await interaction.send(f"*Perhaps you are divine*. You have accurately divined the location of your target. You have cast judgment upon {self.victim.name}")
                    await Rogues.damage(Rogues,self.victim,attacker=self.caster,smite=True)
                for i in self.view.children:
                    i.disabled =True
                await self.view.oginter.edit_original_message(view=self.view)
                self.view.stop()
            else:
                if self.label == "Next Rooms":
                    for i in self.view.children:
                        i.disabled =True
                    self.view.clear_items()
                    for i in self.caster.cRoom.next:
                        bID = f"{self.caster.bID}"
                        self.caster.bID += 1
                        self.view.add_item(Rogues.mButt(caster=self.caster,label=i.name,style=nextcord.ButtonStyle.green,custom_id=bID))
                    bID = f"{self.caster.bID}"
                    self.caster.bID += 1
                    self.view.add_item(Rogues.mButt(caster=self.caster,prev=True,label="Previous Rooms",style=nextcord.ButtonStyle.blurple,custom_id=bID))
                    await self.view.oginter.edit_original_message(view=self.view)
                elif self.label == "Previous Rooms":
                    for i in self.view.children:
                        i.disabled =True
                    self.view.clear_items()
                    for i in self.caster.cRoom.prev:
                        bID = f"{self.caster.bID}"
                        self.caster.bID += 1
                        self.view.add_item(Rogues.mButt(caster=self.caster,label=i.name,style=nextcord.ButtonStyle.green,custom_id=bID))
                    bID = f"{self.caster.bID}"
                    self.caster.bID += 1
                    self.view.add_item(Rogues.mButt(caster=self.caster,prev=True,label="Next Rooms",style=nextcord.ButtonStyle.blurple,custom_id=bID))
                    await self.view.oginter.edit_original_message(view=self.view)
                else:
                    if self.label == "The Saferoom":
                        room = safe
                    else:
                        room = Rogues.findRoom(Rogues,self.label)
                    for i in self.view.children:
                        i.disabled =True
                    await self.view.oginter.edit_original_message(view=self.view)
                    await Rogues.moving(Rogues,self.caster.cRoom,room,self.caster)
                    self.view.stop()
    class Butt(nextcord.ui.Button):
        def __init__(self,scrolls,victim=None,caster=None,react=False,give=False,show=False,scroll=None,cast=False,block=True,info=False,full=False,msg=None,baku=False,scry=False,label="",style=nextcord.ui.Button.style,custom_id=None):
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
            self.scroll = scroll
            self.full=full
            self.block = block
            if full:
                self.msg = msg
            if baku:
                self.baku = baku
            self.scry = scry
        async def callback(self,interaction:nextcord.Interaction):
            try:
                check = self.view.getS()
                await interaction.response.defer()
                for i in self.scrolls:
                    if self.label == i.name:
                        if i.copy == self.scroll.copy:
                            spell = i
                            print(f"Breaking loop. Spell is: {spell.name} copy #{spell.copy}")
                            print(f"{spell.name} aim values are {spell.aim} and {spell.aim2}")
                            break
                    elif self.full:
                        if self.label == self.view.extra.name:
                            spell = self.view.extra
                            print(f"Breaking loop. Spell is the extra: {spell.name} copy #{spell.copy}")
                            break
                print(f"Full is {self.full}")
                print(f"give is {self.give}")
                if self.scry == False:
                    if self.label == "Scrying":
                        self.scry = True
                if self.react:
                    print("react")
                    match str.lower(self.label):
                        case "invisibility":
                            await self.victim.use(interaction,spell)
                            await Rogues.damage(Rogues,self.victim,True,attacker=self.caster,block=self.block)
                            if check==False:
                                self.victim.reacting = False                        
                            else:
                                check = False
                        case "teleport":
                            await self.victim.use(interaction,spell,self.caster)
                            await Rogues.damage(Rogues,self.victim,True,attacker=self.caster,baku=self.baku,block=self.block)
                            if check==False:
                                self.victim.reacting = False
                            else:
                                check = False 
                        case "counter":
                            await self.victim.use(interaction,spell,self.caster)
                            await Rogues.damage(Rogues,self.victim,True,attacker=self.caster,block=self.block)
                            #self.victim.reacting = False for my implementation I think I should NOT do this yet
                        case "za warudo":
                            await self.victim.use(interaction,spell,self.caster)
                            await Rogues.damage(Rogues,self.victim,True,attacker=self.caster,baku=self.baku,block=self.block)
                            if check==False:
                                self.victim.reacting = False
                            else:
                                check = False
                        case "take the hit":
                            await Rogues.damage(Rogues,self.victim,attacker=self.caster,block=self.block)
                            self.victim.reacting = False
                        case _:
                            print("label check "+ self.label)
                            await self.victim.use(interaction,spell)
                            await Rogues.damage(Rogues,self.victim,attacker=self.caster,block=self.block)
                            self.victim.reacting = False
                    if check: # same check but i don't think I need it to rerun choose scroll
                        self.view.setS(check=False)
                        inter = self.view.getI()
                        self.victim.reacting = True
                        await Rogues.chooseScroll(self=Rogues,interaction=inter,victim=self.victim,caster=self.caster,scrolls=self.scrolls,react=True,same=False)
                elif self.scry: # If scrying was used
                    await Rogues.inspect(Rogues,interaction,spell,scry=self.scry,scryer=self.victim)
                elif self.show: # Need to update to send the kind of embed that info creates
                    print("show")
                    if self.victim != None and self.victim != self.caster:
                        await self.victim.mem.send(f"{self.caster.name} has shown you that they own a {self.label} scroll")
                        await Rogues.inspect(Rogues,interaction,spell,scryer=self.victim,show=True)
                        await self.caster.mem.send(f"You showed {self.victim.name} your {self.label} scroll")
                    else:
                        print("all")
                        await self.caster.cRoom.channel.send(f"{self.caster.name} has shown everyone in the room that they own a {self.label} scroll")
                        await Rogues.inspect(Rogues,interaction,spell,show=True,all=True)
                        await self.caster.mem.send(f"You showed everyone in {self.caster.cRoom.channel} your {self.label} scroll")
                elif self.give == True and self.full == False:
                    print(self.full)
                    print("give")
                    if len(self.victim.hand) == 5:
                        await self.caster.mem.send("Your target already has the max amount of scrolls they will need to decide which scroll to give up to accept your gift.")
                        await self.victim.addScroll(spell,interaction,self.caster)
                    else:
                        await self.victim.mem.send(f"{self.caster.name} is giving you their {self.label} scroll")
                        self.caster.hand.remove(spell)
                        await self.victim.addScroll(spell,interaction)
                        await self.caster.mem.send(f"You are giving {self.victim.name} your {self.label} scroll")
                        self.disabled = True
                        inter = self.view.getI()
                        await inter.edit_original_message(view=self.view)
                        self.give = False
                elif self.info:
                    await Rogues.inspect(Rogues,interaction,i)
                elif self.cast:
                    if spell.aim:
                        print("cast")
                        MyEmbed = nextcord.Embed(title = "Who will be your victim(s)?", description = "These are the other Players in the room",color = nextcord.Colour(0xFFD700))
                        if len(self.caster.cRoom.guests)==1:
                            await interaction.send("There is no one in this room to target")
                            return
                        for i in self.caster.cRoom.guests:
                            if spell.type == "Offensive" and i.name == self.caster.name:
                                print("Can't target self")
                            else:
                                MyEmbed.add_field(name=f"Player {i.uid}",value=i.name,inline=True)
                        print(f"Spell: {spell.name}")                    
                        aim = Rogues.Aiming(interaction,scroll=spell,caster=self.caster,embed=MyEmbed)
                        await interaction.send(embed=MyEmbed,view=aim,ephemeral=True)
                    else:
                        print("i'm dumb")
                        await self.caster.use(interaction,spell)
                elif self.full:
                    if self.give:
                        print("960")
                        if spell in self.caster.hand:
                            self.caster.hand.remove(spell)
                            await self.caster.addScroll(self.view.extra)
                        elif self.victim !=None:
                            self.victim.hand.remove(spell)
                            print("removed from gifter")
                        for i in self.view.children:
                            i.disabled = True
                            print("full give disabled")
                        await self.msg.edit(content=self.msg.content,view=self.view)
                        print("break here?")
                        MyEmbed = nextcord.Embed(title = "Who will receive your scroll?", description = "These are the other Players.",color = nextcord.Colour(0xFFD700))
                        for i in players:
                            if i.name == self.caster.name:
                                print("not you")
                            else:
                                MyEmbed.add_field(name=f"Player {i.uid}",value=i.name,inline=True)
                        recip = Rogues.Aiming(interaction,scroll=spell,caster=self.caster,embed=MyEmbed,full=True,msg=self.msg)
                        await self.msg.edit(content=self.msg.content,embed=MyEmbed,view=recip)
                        self.view.stop()
                        return
                    if self.label != "Give": # Not paying it forward
                        if spell == self.view.extra: # Rejecting the extra scroll
                            if self.victim != None: # Rude
                                self.victim.mem.send(f"{self.caster.name} has rejected your gift and sent it back to the dungeon.")
                                self.msg.edit(content=f"You have rejected {self.victim.name}'s gift and sent it back to the dungeon.")
                                self.view.msg.content = f"You have rejected {self.victim.name}'s gift and sent it back to the dungeon."
                                self.victim.hand.remove(spell)
                                spell.owner = None
                                deck.append(spell)
                                for i in self.view.children:
                                    i.disabled = True
                                    await self.msg.edit(view=self.view)
                                self.view.stop()
                                return
                        print("no give")
                        if self.victim !=None: # Remove the extra from the giver
                            self.victim.hand.remove(self.view.extra)
                            print("removed from gifter")
                        spell.owner = None
                        deck.append(spell)
                        if spell in self.caster.hand:
                            self.caster.hand.remove(spell)
                            await self.caster.addScroll(self.view.extra)
                            await self.msg.edit(content="You have returned one of your scrolls to the dungeon.")
                            self.view.msg.content="You have returned one of your scrolls to the dungeon."
                            for i in self.view.children:
                                i.disabled = True
                                print("Give button disable")
                            await self.msg.edit(view=self.view)
                            self.view.stop()
                            return
                        else: # Realistically I don't believe this should trigger anymore
                            print("somehow? give messed up I think")
                            if self.victim !=None:
                                self.victim.hand.remove(spell)
                                print("removed from gifter???")
                            spell.owner = None
                            deck.append(spell)
                            await self.msg.edit(content="You have returned the extra scroll to the Dungeon.")
                            self.view.msg.content="You have returned one of your scrolls to the Dungeon."
                            for i in self.view.children:
                                i.disabled = True
                            await self.msg.edit(view=self.view)
                            self.view.stop()
                            return
                    else:
                        print("give was selected")
                        await Rogues.chooseScroll(Rogues,interaction,self.caster,self.scrolls,victim=self.victim,give=True,full=True,extra=self.view.extra,msg=self.msg)
                        return
                if self.cast==False and self.info==False:
                    for i in self.view.children:
                        i.disabled = True
                        print(f"{i.label} disabled. RCallback")
                    await self.view.oginter.edit_original_message(view=self.view)
                    self.view.stop()
            except Exception as e:
                print(f"1173 React Button Callback. An error occured: {e}")
                for i in self.view.children:
                    i.disabled = True
                await self.view.oginter.edit_original_message(view=self.view)
                self.view.stop()
    class Reacts(nextcord.ui.View):
        def __init__(self,oginter:nextcord.Interaction,scrolls,victim=None,caster=None,react=False,give=False,show=False,block=True,cast=False,info=False,same=False,full=False,extra=None,msg=None,baku=False,scry=False):
            super().__init__(timeout=45)
            self.oginter = oginter
            self.Scheck = same
            self.victim = victim
            self.caster = caster
            self.scrolls = scrolls
            self.info = info
            self.react = react
            self.full = full
            if baku:
                self.baku = baku
            self.scry = scry
            for i in scrolls:#I made the custom ids here match the serial number of the scrolls so I don't believe I'll have to add in a specific button ID the same way I did for the others
                if full:
                    self.extra = extra
                    self.msg = msg
                    self.add_item(Rogues.Butt(scrolls=scrolls,victim=victim,caster=caster,react=react,give=give,scroll=i,show=show,block=block,full=full,msg=msg,cast=cast,info=info,baku=baku,scry=scry,label=i.name,style=nextcord.ButtonStyle.green,custom_id=str(i.serial)))
                else:
                    self.add_item(Rogues.Butt(scrolls=scrolls,victim=victim,caster=caster,react=react,give=give,scroll=i,show=show,full=full,block=block,cast=cast,info=info,baku=baku,scry=scry,label=i.name,style=nextcord.ButtonStyle.green,custom_id=str(i.serial)))
            if full:
                self.extra = extra
                self.msg = msg
                self.add_item(Rogues.Butt(scrolls=scrolls,victim=victim,caster=caster,react=react,give=give,show=show,msg=self.msg,cast=cast,info=info,block=block,baku=baku,scry=scry,full=full,label=extra.name,style=nextcord.ButtonStyle.blurple,custom_id=str(79)))
                if give==False:
                    self.add_item(Rogues.Butt(scrolls=scrolls,victim=victim,caster=caster,react=react,give=give,msg=self.msg,show=show,cast=cast,info=info,block=block,baku=baku,scry=scry,full=full,label="Give",style=nextcord.ButtonStyle.red,custom_id=str(80)))
            if react:
                self.add_item(Rogues.Butt(scrolls=scrolls,victim=victim,caster=caster,react=react,give=give,show=show,cast=cast,info=info,baku=baku,scry=scry,block=block,label="Take the hit",style=nextcord.ButtonStyle.red,custom_id=str(77)))
        def getS(self): # getter to track Same check
            print(f"same is {self.Scheck}")
            return self.Scheck
        def setS(self,check:bool): # setter to track Same check
            self.Scheck = check
            print(f"same is set to {self.Scheck}")
        def getI(self): # grabbing the original view interaction
            print("get Interaction")
            return self.oginter
        async def on_timeout(self): # Disable all items in the view when it times out
            print("React Timeout")
            if self.full:
                for i in self.children:
                    i.disabled = True
                await self.msg.edit(content=self.msg.content,view=self)
                self.stop()
            elif self.scry:
                for i in self.children:
                    i.disabled = True
                await self.msg.edit(content=f"You did not choose in time so a random scroll of yours has been selected to be revealed to {self.victim.name}",view=self)
                self.stop()
                reveal = random.choice(self.caster.hand)
                await Rogues.inspect(Rogues,self.oginter,reveal,True,self.victim)
            else:
                for i in self.children:
                    i.disabled = True
                await self.oginter.edit_original_message(view=self)
                if self.Scheck and self.react:
                    await Rogues.chooseScroll(self=Rogues,interaction=self.oginter,victim=self.victim,caster=self.caster,scrolls=self.scrolls,react=True,same=False)
                self.stop()
    class AimButt(nextcord.ui.Button):
        def __init__(self,scroll=None,caster=None,label="",style:nextcord.ui.Button.style=None,custom_id=None,embed=None,full=False,msg=None):
            super().__init__(label=label,style=style,custom_id=custom_id)
            self = Rogues.AimButt
            self.scroll = scroll
            self.caster = caster
            self.t1 = None
            self.t2 = None
            self.embed= embed
            self.full = full
            self.msg = msg
        async def callback(self,interaction:nextcord.Interaction):
            if self.full:
                self.t1 = Rogues.identify(Rogues,name=self.label)
                await self.t1.addScroll(self.scroll)
                for i in self.view.children:
                    i.disabled = True
                await self.msg.edit(content=f"You have given away the scroll to {self.label}",embed=self.embed,view=self.view)
                self.view.stop()
                return
            else:
                try:
                    if self.scroll.aim2 and not self.view.aimCheck():
                        self.t1 = Rogues.identify(Rogues,name=self.label)
                        self.disabled = True
                        self.view.add_item(Rogues.AimButt(scroll=self.scroll,caster=self.caster,label="Same person",style=nextcord.ButtonStyle.blurple,custom_id=str(78),embed=self.embed))
                        await self.view.oginter.edit_original_message(embed=self.embed,view=self.view)
                        self.view.setT(target=self.label)
                        print("saving target 1?")
                        return
                    elif self.scroll.aim2 and self.view.aimCheck:
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
                        await self.view.oginter.edit_original_message(embed=self.embed,view=self.view)
                        self.view.stop()
                    else:
                        self.t1 = Rogues.identify(Rogues,name=self.label)
                        await self.caster.use(interaction,self.scroll,target=self.t1.mem)
                        for i in self.view.children:
                            i.disabled = True
                        await self.view.oginter.edit_original_message(embed=self.embed,view=self.view)
                        self.view.stop()
                except Exception as e:
                    print(f"1283 Aim button callback. An error occured: {e}")
                    for i in self.view.children:
                        i.disabled = True
                    await self.view.oginter.edit_original_message(view=self.view)
                    self.view.stop()
    class Aiming(nextcord.ui.View):
        def __init__(self,oginter:nextcord.Interaction,scroll=None,caster=None,embed=None,full=False,msg=None):
            super().__init__(timeout=60)
            self.scroll = scroll
            self.caster = caster
            self.oginter = oginter
            self.skip = False
            self.embed = embed
            self.test = None
            self.full = full
            if full:
                for i in players:
                    if i.name == self.caster.name:
                        print("same same")
                    else:
                        bID = f"{self.caster.bID}"
                        self.caster.bID += 1
                        self.add_item(Rogues.AimButt(scroll=self.scroll,caster=self.caster,label=i.name,style=nextcord.ButtonStyle.green,custom_id=bID,embed=self.embed,full=full,msg=msg))
            else:
                for i in self.caster.cRoom.guests:
                    bID = f"{self.caster.bID}"
                    self.caster.bID += 1
                    if scroll.type == "Defensive" and i.name == caster.name:
                        self.add_item(Rogues.AimButt(scroll=scroll,caster=caster,label="Myself",style=nextcord.ButtonStyle.green,custom_id=bID,embed=embed))
                    elif scroll.type == "Offensive" and i.name == caster.name:
                        print("same same")
                    elif scroll.type == "Ancillary" and i.name == caster.name:
                        if scroll.name == "Cure Wounds":
                            self.add_item(Rogues.AimButt(scroll=scroll,caster=caster,label="Myself",style=nextcord.ButtonStyle.green,custom_id=bID,embed=embed))
                        else:
                            print("same same2")
                    else:
                        self.add_item(Rogues.AimButt(scroll=scroll,caster=caster,label=i.name,style=nextcord.ButtonStyle.green,custom_id=bID,embed=embed))
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
            print("Aiming Timeout")
            for i in self.children:
                i.disabled = True
            self.embed.title = "Failed to choose a target in time."
            if self.full:
                self.scroll.owner = None
                deck.append(self.scroll)
                self.embed.description = "The scroll has returned to the dungeon."
            else:
                self.embed.description = "You did not select a target in time. Please try again."
            await self.oginter.edit_original_message(embed=self.embed,view=self)
    async def reactCheck(self,interaction:nextcord.Interaction,victim,caster,scroll,same=False,counter=True,block=True,avoid=True,used=False,tried=False): # Figured I should just turn this into a function rather than pasting under every offensive spell.
        if victim.reacting==True: # Players will need to react to spells one at a time.  
            await caster.mem.send(f"{victim.name} is already being attacked and is currently reacting to another spell. Give them a moment to think they are safe(max 15 sec). Then you can try again.")
            if same:
                await caster.mem.send(f"The {scroll.name} scroll will not be used since you only targetted {victim.name}")
                return False
            else:
                if used:
                    await caster.mem.send(f"Your second target, {victim.name}, is already being attacked and will not be targetted by this spell.")
                else:
                    if tried:
                        await caster.mem.send(f"The {scroll.name} scroll will not be used.")
                    else:
                        await caster.mem.send(f"The {scroll.name} scroll will still be used up if your second target is able to be hit by the attack.")
                return False
        else:
            hit = True # check to see if it automatically hits.
            reaction = [] # array of the options the victim has.
            if victim.hand != []:
                await victim.mem.send(f"You are being targetted by {caster.name} who casted {scroll.name}.\nYou have 15 seconds to react if you have any scrolls that can save you.")
                for i in victim.hand:
                    if i.type == "Defensive" or i.name == "Za Warudo": # check if they have a defensive spell or Za Warudo cuz it's special.
                        if i.name == "Counter" and scroll.counter == False:
                            continue
                        if "shield"in i.effect and scroll.block==False:
                            continue
                        if "avoid" in i.effect and scroll.avoid==False:
                            continue
                        reaction.append(i)
                        if len(reaction)==1:
                            await victim.mem.send(f"You have at least one scroll in your hand that can be used to save you from this spell. What will you do?")
                            hit = False # pause the hit
            else:
                await victim.mem.send("You have no scrolls to defend with. git gud")
                hit = True
            if hit:
                await victim.mem.send(f"You have no scrolls that can save you from this spell. Big rip")
                if same:
                    await Rogues.damage(Rogues,victim,attacker=caster,block=block)
                await Rogues.damage(Rogues,victim,attacker=caster,block=block)
                caster.turnDone = True
            else:
                victim.reacting = True
                if same==False:
                    await self.chooseScroll(self=self,interaction=interaction,victim=victim,caster=caster,scrolls=reaction,react=True,block=block,)
                    await caster.cRoom.channel.send(f"{caster.name} casted {scroll.name} at {victim.name}")
                elif same:
                    #if tried:
                    await self.chooseScroll(self=self,interaction=interaction,victim=victim,caster=caster,scrolls=reaction,react=True,same=same,block=block,)
                    #else:
                    #    await self.chooseScroll(self=self,interaction=interaction,victim=victim,caster=caster,scrolls=reaction,react=True,same=same)
                    #    victim.reacting = False
                    #    await Rogues.reactCheck(Rogues,interaction,victim,caster,scroll,same=True,counter=counter,block=block,avoid=avoid,used=used,tried=True)
            return True
    async def chooseScroll(self,interaction:nextcord.Interaction,caster,scrolls,victim=None,react=False,show=False,give=False,cast=False,same=False,info=False,block=True,baku=False,full=False,extra=None,msg=None,scry=False):
        if react:
            MyEmbed = nextcord.Embed(title = "Reaction Spells", description = "These are the scrolls you own that can be used to save you from this attack",color = nextcord.Colour(0xFFD700))
        elif scry:
            MyEmbed = nextcord.Embed(title = "Scrolls",description=f"Please choose which scroll to show to {caster.name}")
        elif give and full:
            MyEmbed = nextcord.Embed(title = "Scrolls",description="Please choose which scroll you would like to gift to another player.")
        elif full:
            MyEmbed = nextcord.Embed(title = "Scrolls",description="You have received an extra scroll. You can only hold 5. Please choose which scroll you would like to give back to the dungeon or choose give to gift a scroll to another player.")
        else:
            MyEmbed = nextcord.Embed(title = "Scrolls",description="These are the scrolls to choose from.")
        i=0
        if victim==None:
            victim=caster
        victim.handDis = ""
        while i < len(scrolls):
            if len(scrolls)==1:
                victim.handDis = f"{i+1}. **{scrolls[i].name}**\n"
            elif i == len(scrolls):
                break
            elif i == len(scrolls)-1:
                victim.handDis = victim.handDis + f"{i+1}. **{scrolls[i].name}**"
            else:
                victim.handDis = victim.handDis + f"{i+1}. **{scrolls[i].name}**\n"
            i+=1
        MyEmbed.add_field(name="Owned Scrolls",value=victim.handDis,inline=False)
        if extra!=None:
            MyEmbed.add_field(name="Extra Scroll",value=extra.name,inline=False)
        MyEmbed.set_thumbnail(url=caster.mem.display_avatar.url)
        if react:
            await interaction.send(f"Your target: {victim.name} is reacting to your spell.",ephemeral=True)
            view = self.Reacts(oginter=interaction,scrolls=scrolls,victim=victim,caster=caster,react=react,block=block,same=same)
            await victim.mem.send(embed=MyEmbed,view=view)
        elif scry:
            view = self.Reacts(oginter=interaction,scrolls=scrolls,victim=caster,caster=victim,block=block,scry=scry)
            await victim.mem.send(embed=MyEmbed,view=view)
        elif cast:
            view = self.Reacts(oginter=interaction,scrolls=scrolls,caster=caster,react=react,block=block,show=show,give=give,cast=cast)
            await interaction.response.send_message(embed=MyEmbed,view=view,ephemeral=True)
        elif info:
            view = self.Reacts(oginter=interaction,scrolls=scrolls,caster=caster,block=block,info=info)
            await interaction.response.send_message(embed=MyEmbed,view=view,ephemeral=True)
        elif give and full:
            print("both pass")
            view = self.Reacts(oginter=interaction,scrolls=scrolls,caster=caster,victim=victim,react=react,show=show,block=block,give=give,cast=cast,full=full,extra=extra,msg=msg)
            await msg.edit(content=msg.content,embed=MyEmbed,view=view)
        elif full:
            print("full pass")
            view = self.Reacts(oginter=interaction,scrolls=scrolls,caster=caster,victim=victim,react=react,block=block,show=show,give=give,cast=cast,full=full,extra=extra,msg=msg)
            await msg.edit(content=msg.content,embed=MyEmbed,view=view)
        else:
            view = self.Reacts(oginter=interaction,scrolls=scrolls,victim=victim,caster=caster,block=block,react=react,show=show,give=give,cast=cast)
            await interaction.response.send_message(embed=MyEmbed,view=view,ephemeral=True)
        return
    async def inspect(self,interaction:nextcord.Interaction,scroll,scry=False,scryer:Player=None,show=False,all=False):
        MyEmbed = nextcord.Embed(title = scroll.name,description=f"**{scroll.type}** type spell")
        image = nextcord.File(scroll.image,filename="scroll.png")
        MyEmbed.set_image(url="attachment://scroll.png")
        MyEmbed.add_field(name="Counterable?",value=scroll.counter,inline=True)
        MyEmbed.add_field(name="Blockable?",value=scroll.block,inline=True)
        MyEmbed.add_field(name="Avoidable?",value=scroll.avoid,inline=True)
        MyEmbed.add_field(name="Effect:",value=scroll.effect,inline=False)
        MyEmbed.add_field(name="Owner",value=f"**{scroll.owner}**",inline=True)
        MyEmbed.add_field(name="Serial",value=f"#{scroll.copy}",inline=True)
        MyEmbed.add_field(name="",value=f"*{scroll.flavor}*",inline=False)
        if scry:
            await scryer.mem.send(file=image,embed=MyEmbed)
        elif show:
            if all:
                await scryer.cRoom.channel.send(file=image,embed=MyEmbed,ephemeral=True)
            else:
                await scryer.mem.send(file=image,embed=MyEmbed)
        else:
            await interaction.send(file=image,embed=MyEmbed,ephemeral=True)
    async def roommate(self,caster:Player,victim:Player):
        if caster.cRoom == victim.cRoom:
            return True
        else:
            await caster.cRoom.channel.send(f"{caster.name} attempted to use a scroll directed at {victim.name}.")
            return False
    async def dungeon(self):
        '''for x in floor:
            for y in x.guests:
                if isinstance(y,Enemy):
                    y.turn()'''
        print("dungeon turn")
        for z in players:
            z.turnDone = False
            z.movement = True    
    async def newFloor(self):
        for i in category.text_channels:
            if i.name =="saferoom":
                continue
            else: #delete all rooms each floor or save them for post game review?
                await i.delete()
        await safeRoom.send("### I've brought back the Saferoom")
        RC = 0
        if floornum > 3:
            difficulty +=1
            floornum = 1
        match difficulty:
            case 0:
                match floornum:
                    case 1:
                        #bp for first floor
                        print(floornum)
                    case 2:
                        #bp for second floor
                        print(floornum)
                    case 3:
                        #bp for last floor before evil
                        print(floornum)
                    case _:
                        print("something went wrong")
            case 1:
                #create first evil floor
                print(difficulty)
            case 2:
                #create second evil floor
                print(difficulty)
            case 3:
                #create last evil floor.
                print(difficulty)
        await safeRoom.send("Advancing to the next Floor...")
        for i in players:
            print(f"Resetting {i.name} for the next floor")
            i.movement = True
            i.cRoom = safe
            i.pRoom = None
            i.delve = False
            i.shield = 0
            i.dCount = 0
            i.map = []
            await Rogues.overwrite(Rogues,safeRoom,i,False,safeVC)
            i.map.append(safe)
            i.nRoom = safe.next
        for i in floor:
            if i == safe:
                pass
            else:
                del i
        floornum+=1
class Scroll: #This will all be internal. No player interaction to create scrolls for the game.
    name = ""
    type = "" # Off Def Anc
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
    owner = None
    rarity = ""
    def __init__(self,name,stype,counter,block,avoid,copy,count,flavor,effect,image,rank,aim=False,aim2=False):
        self.name = name
        self.type = stype
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
        self.owner = None
        match rank:
            case 1:
                self.rarity =  "Common"
            case 1:
                self.rarity =  "Rare"
            case 1:
                self.rarity =  "Unique"
            case _:
                self.rarity =  ""
        if name == "Wish":
            wCount = 0
    def toPrint(self):
        print(f"{self.name}. Type: {self.type}. Serial Number: {self.copy}. There are {self.count} total in the dungeon.")
    async def action(self,interaction:nextcord.Interaction,target=None,target2=None,same:bool=False):
        caster = Rogues.identify(Rogues,interaction.user)# Can set all these up outside each individual action.
        if target!=None:
            victim = Rogues.identify(Rogues,target)
        if target2!=None:
            v2 = Rogues.identify(Rogues,target2)
        used = False
        match str.lower(self.name):
            case "teleport": # just used to avoid an attack for right now so not a lot needs to be here.
                print(f"{interaction.user} casted {self.name}")
                if caster.reacting == True:
                    await caster.cRoom.channel.send(f"{caster.name} teleported away from {target.name}'s attack")
                    caster.reacting = False
                    used = True
                    if caster.pRoom!=None:
                        await Rogues.moving(Rogues,caster.cRoom,caster.pRoom,caster,True)
                else:
                    print(self.name)
                    if caster.pRoom!=None:
                        used = True
                        await Rogues.moving(Rogues,caster.cRoom,caster.pRoom,caster,True)
                        caster.turnDone = True
                        await caster.mem.send("You have used your scroll and ended your turn")
                    else:
                        await interaction.send("You have not been to a room before this one. You can not use Teleport at this time. Please explore more.")
                        return
            case "fireball": # attacking a player so gotta check for a lot
                if await Rogues.roommate(Rogues,caster,victim):
                    print(f"{interaction.user} casted {self.name}")
                    used = await Rogues.reactCheck(Rogues,interaction,victim,caster,self,counter=self.counter,block=self.block,avoid=self.avoid)
                    caster.turnDone = True
                    await caster.mem.send("You have used your scroll and ended your turn")
                else:
                    await interaction.send(f"Is there a {victim.name} in the room with us right now?\n-# The answer is no. You can't attack someone who isn't here. You aren't God",ephemeral=True)
            case "counter": # avoid and counter attack
                print(f"{interaction.user} COUNTERED")
                if caster.reacting == True:
                    used = await Rogues.reactCheck(Rogues,interaction,target,caster,self,counter=self.counter,block=self.block,avoid=self.avoid)
                    caster.reacting = False
                else:
                    print(self.name)
                    await interaction.send(f"The {self.name} scroll can only be used in reaction to another spell.",ephemeral=True)
                    return
            case "mold earth":
                print(f"{interaction.user} casted {self.name}")
                if target2==None:
                    if await Rogues.roommate(Rogues,caster,victim):
                        victim.shield+=2
                        if victim == caster:
                            await interaction.send(f"{caster.name} casted Mold Earth and shielded themselves")
                        else:
                            await interaction.send(f"{caster.name} casted Mold Earth on {victim.name}!")
                        caster.turnDone = True
                        await caster.mem.send("You have used your scroll and ended your turn")
                    else:
                        await interaction.send(f"Is there a {victim.name} in the room with us right now?\n-# The answer is no. You can't attack someone who isn't here. You aren't God",ephemeral=True)
                elif target2!=None:
                    if await Rogues.roommate(Rogues,caster,victim) and await Rogues.roommate(Rogues,caster,v2):
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
                    else:
                        await interaction.send("One or both of your targets is not in the same room as you. Please pick better targets.")
                elif caster.reacting==True:
                    caster.shield+=2
                    await caster.mem.send(f"You casted Mold Earth and shielded yourself")
                    caster.reacting = False
                used = True
            case "eldritch blast": # can't be avoided
                if await Rogues.roommate(Rogues,caster,victim):
                    print(f"{interaction.user} casted {self.name}")
                    used = await Rogues.reactCheck(Rogues,interaction,victim,caster,self,counter=self.counter,block=self.block,avoid=self.avoid)
                    caster.turnDone = True
                    await caster.mem.send("You have used your scroll and ended your turn")
                else:
                    await interaction.send(f"Is there a {victim.name} in the room with us right now?\n-# The answer is no. You can't attack someone who isn't here. You aren't God",ephemeral=True)
            case "call lightning": # target two entities or one entity twice
                if await Rogues.roommate(Rogues,caster,victim) and await Rogues.roommate(Rogues,caster,v2):
                    print(f"{interaction.user} casted {self.name}")
                    tried = False
                    if target2!=None:
                        print("two people")
                        used = await Rogues.reactCheck(Rogues,interaction,victim,caster,self,counter=self.counter,block=self.block,avoid=self.avoid,used=used,tried=tried)
                        tried = True
                        if used:
                            await Rogues.reactCheck(Rogues,interaction,v2,caster,self,counter=self.counter,block=self.block,avoid=self.avoid,used=used,tried=tried)
                        else:
                            used = await Rogues.reactCheck(Rogues,interaction,v2,caster,self,counter=self.counter,block=self.block,avoid=self.avoid,used=used,tried=tried)
                    elif target2 == None or same: # if the target is double fucked
                        print("double fucked")
                        used = await Rogues.reactCheck(Rogues,interaction,victim,caster,self,same=same,counter=self.counter,block=self.block,avoid=self.avoid,used=False)
                    if used:
                        caster.turnDone = True
                        await caster.mem.send("You have used your scroll and ended your turn")
                    else:
                        await caster.mem.send("The attack was unsuccessful. The scroll will remain in your hand.")
                else:
                    await interaction.send("One or both of your victims is not in the same room as you. Please pick better targets.")
            case "dragon breath": # can't be blocked
                if await Rogues.roommate(Rogues,caster,victim):
                    print(f"{interaction.user} casted {self.name}")
                    victim = Rogues.identify(Rogues,target) # identify target player
                    used = await Rogues.reactCheck(Rogues,interaction,victim,caster,self,counter=self.counter,block=self.block,avoid=self.avoid)
                    caster.turnDone = True
                    await caster.mem.send("You have used your scroll and ended your turn")
                else:
                    await interaction.send(f"Is there a {victim.name} in the room with us right now?\n-# The answer is no. You can't attack someone who isn't here. You aren't God",ephemeral=True)
            case "scrying": # requires roommate and they get to choose which scroll to reveal
                if await Rogues.roommate(Rogues,caster,victim):
                    print(f"{interaction.user} casted {self.name}")
                    await Rogues.chooseScroll(Rogues,interaction,caster,victim.hand,victim,scry=True)
                else:
                    await interaction.send(f"Is there a {victim.name} in the room with us right now?\n-# The answer is no. You can't attack someone who isn't here. You aren't God",ephemeral=True)
            case "divine wisdom": # May revisit and change rarity of this spell and if it requires roommate. Reveal all scrolls in your target's hand
                if await Rogues.roommate(Rogues,caster,victim):
                    print(f"{interaction.user} casted {self.name}")
                    await victim.mem.send(f"{caster.name} has casted {self.name} on you. All your scrolls have been revealed to them.")
                    for i in victim.hand:
                        await Rogues.inspect(Rogues,interaction,i,True,caster)
                    used = True
                else:
                    await interaction.send(f"Is there a {victim.name} in the room with us right now?\n-# The answer is no. You can't attack someone who isn't here. You aren't God",ephemeral=True)
            case "barbarian rage": # +2 shields to yourself
                print(f"{interaction.user} casted {self.name}")
                if caster.reacting == True:
                    caster.shield +=2
                    await caster.mem.send("Your rage shields you allowing you to endure damage twice.")
                    caster.reacting = False
                else:
                    caster.shield +=2
                    await caster.mem.send("Your rage shields you allowing you to endure damage twice.")
                    caster.turnDone = True
                    await caster.mem.send("You have used your scroll and ended your turn")
            case "polymorph": # still gotta implement
                if await Rogues.roommate(Rogues,caster,victim):
                    print(f"{interaction.user} casted {self.name}")
                else:
                    await interaction.send(f"Is there a {victim.name} in the room with us right now?\n-# The answer is no. You can't attack someone who isn't here. You aren't God",ephemeral=True)
            case "invisibility": # need to more clearly define how this works but for the time being it will be an avoid spell only
                print(f"{interaction.user} casted {self.name}")
                if caster.reacting == True:
                    caster.dCount = 2
                else:
                    caster.dCount = 2
                    caster.turnDone = True
                    await caster.mem.send("You have used your scroll and ended your turn")
            case "magic shield": # +1 shield
                print(f"{interaction.user} casted {self.name}")
                if target != None:
                    if await Rogues.roommate(Rogues,caster,victim):
                        victim.shield+=1
                        same = caster==victim
                        if same:
                            await interaction.send(f"{caster.name} shielded themselves")
                            print(f"{victim.name} was shielded to {victim.shield} shields")
                        else:
                            await interaction.send(f"{caster.name} casted Magic Shield on {victim.name}!")
                            print(f"{victim.name} was shielded to {victim.shield} shields")
                        used = True
                        await caster.mem.send("You have ended your turn")
                    else:
                        await interaction.send(f"Is there a {victim.name} in the room with us right now?\n-# The answer is no. You can't attack someone who isn't here. You aren't God",ephemeral=True)
                elif caster.reacting == True:
                    caster.shield+=1
                    await caster.mem.send(f"You reacted and shielded yourself.")
                    caster.reacting = False
                else:
                    caster.shield+=1
                    await caster.mem.send(f"You shielded yourself.")
                    caster.turnDone = True
            case "steal": # will work on these when we get there.
                if await Rogues.roommate(Rogues,caster,victim):
                    print(f"{interaction.user} casted {self.name}")
                else:
                    await interaction.send(f"Is there a {victim.name} in the room with us right now?\n-# The answer is no. You can't attack someone who isn't here. You aren't God",ephemeral=True)
            case "blood altar": # ^
                if await Rogues.roommate(Rogues,caster,victim):
                    print(f"{interaction.user} casted {self.name}")
                else:
                    await interaction.send(f"Is there a {victim.name} in the room with us right now?\n-# The answer is no. You can't attack someone who isn't here. You aren't God",ephemeral=True)
            case "cure wounds":
                if await Rogues.roommate(Rogues,caster,victim):
                    print(f"{interaction.user} casted {self.name}")
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
                else:
                    await interaction.send(f"Is there a {victim.name} in the room with us right now?\n-# The answer is no. You can't attack someone who isn't here. You aren't God",ephemeral=True)
            case "holy shield":
                print(f"{interaction.user} casted {self.name}")
                await caster.mem.send("You *truly* have the power of **God** on your side.")
                caster.shield +=5
                if caster.reacting==True:
                    await caster.mem.send("This is a reaction and will not use up your turn.")
                else:
                    caster.turnDone = True
                    await caster.mem.send("You have used your scroll and ended your turn")
                used = True
            case "soul knot": # add implementation for this at LITERALLY the end of the game lol
                print(f"{interaction.user} casted {self.name}") # Not limited to room and will expose death if target is dead.
                if target == None or caster == victim:
                    await caster.mem.send("You can **not** *knot* your soul with itself.")
                    return
                used = True
                caster.soul = victim.mem
                victim.soul = caster.mem
                await caster.mem.send(f"Your soul is now linked with {victim.name}.\n**Regardless of any other factors** if you both are the only ones to make it out of the dungeon __alive__ you both will be considered the winners of this excursion.\n**However if one of you dies. You both perish.**")
                await victim.mem.send(f"Your soul is now linked with {caster.name}.\n**Regardless of any other factors** if you both are the only ones to make it out of the dungeon __alive__ you both will be considered the winners of this excursion.\n**However if one of you dies. You both perish.**")
            case "wish":
                # wish 1: second life. when you die you are reborn(full health, 3 random scrolls from deck) into a previous room if applicable.
                # wish 2: Wish to create power. Creates a duplicate spell and gives it to the wisher. Add in rarity
                # wish idea: wish will get added back into the deck two additional times. 3 wishes total in the game. after that no more.
                wCount +=1
                # Make a wish view with buttons for each wish
                print(f"{interaction.user} casted {self.name}")
                used = True
            case "za warudo":
                print(f"{interaction.user} casted {self.name}")
                if caster.reacting == True:
                    used = await Rogues.reactCheck(Rogues,interaction,target,caster,self,counter=self.counter,block=self.block,avoid=self.avoid)
                    caster.reacting = False
                else:
                    print(self.name)
                    await interaction.send(f"The {self.name} scroll can only be used in reaction to another spell.",ephemeral=True)
                    return
            #Maybe done with explosion
            case "explosion": # 3 damage to everyone else in the room...MAYBE some damage to the user 
                print(f"{interaction.user} casted {self.name}")
                if len(caster.cRoom.guests)>1:
                    print(caster.cRoom.guestList())
                    used = True
                    for i in caster.cRoom.guests:
                        if i == caster: # for now decided to make it so they can't move AFTER casting the spell
                            caster.movement = False
                            await interaction.send("You have casted the most powerful magic you've ever witnessed. It has taken a significant toll on you and you can no longer move.",ephemeral=True)
                        else:
                            reaction = []
                            for j in i.hand:
                                if j.name == "Teleport" or j.name == "Za Warudo":
                                    reaction.append(j)
                            if reaction != []:
                                await Rogues.chooseScroll(Rogues,interaction,victim=i,caster=caster,scrolls=reaction,react=True,baku=True)
                            else:
                                await Rogues.damage(Rogues,i,False,attacker=caster,baku=True)
                else:
                    await interaction.send("You are alone in this room. There is no one to explode.",ephemeral=True)
            case "smite":
                print(f"{interaction.user} casted {self.name}")
                MyEmbed = nextcord.Embed(title = caster.name, description = "Can you __divine__ which room your target is in?",color = nextcord.Colour(0x6f00eb))
                MyEmbed.set_thumbnail(url=victim.mem.display_avatar.url)
                guess = Rogues.mView(interaction,caster,smite=True,victim=victim)
                await interaction.send(embed=MyEmbed,view=guess,ephemeral=True)
            case _: #Default
                await interaction.send("That was not a valid name for a scroll. Orrrrrr something went wrong...tell my Master",ephemeral=True)
        if used:
            caster.hand.remove(self)
            if self.name == "Soul Knot":
                await safeRoom.send("# Soul Knot has been used and will not be returned to the dungeon.")
            elif self.name == "Wish":
                if wCount==3:
                    await safeRoom.send("# All 3 Wishes have been used and the magical wish granting...orbs will not return to the dungeon.")
                else:
                    deck.append(self)
            else:
                deck.append(self)
            self.owner=None
            await interaction.send(f"*Your {self.name} has returned to the Dungeon*",ephemeral=True)
            if caster.dCount>0: caster.dCount-=1
        else:
            await interaction.send("Your scroll was not used. If you try again. Be better.",ephemeral=True)

class Enemy:
    hp = 1 # MAYBE scale with difficulty
    atk = 1 # scale this with difficulty
    loot = set()
    room = None
    evil = True
    def __init__(self,diff,room):
        self.hp = self.hp * diff
        self.atk = self.atk * diff
        self.room = room
    async def turn(self,interaction:nextcord.Interaction):
        targets = []
        for i in self.room.guesets:
            if i.evil == False:
                targets.append(i)
        victim = random.choice(targets)
        # Need to think out attacking enemies and vice versa
        # Add a whole new branch to react check for enemies
    def lootTable(self): # I need to determine: rarity of loot the enemy can have, how much loot, which loot from selected rarity/rarities,
        enough = False # I want to put a cap on how much GOOD stuff the loot table can have.
        count = 0
        w = Rogues.deckWeight()
        match difficulty:
            case 1: # very small chance for unique. slightly higher for rare
                while len(self.loot)<4: # limit 1 unique and at most 2 rare. Should always be at least 1 common
                    l = random.choices(deck,w,k=1)
                    if count == 3:
                        enough = True
                    if l.rarity == "Common" or l.rarity == "Rare" and enough == False:
                        self.loot.add(l)
                        if l.rarity == "Rare":
                            count+=1
                    elif l.rarity == "Common" and enough==True:
                        self.loot.add(l)
                    elif l.rarity == "Unique" and enough==False:
                        if count < 3:
                            self.loot.add(l)
                            enough = True
            case 2: # better rates
                while len(self.loot)<5: # limit 2 unique and at most 2 rare. Should always be at least 1 common
                    l = random.choices(deck,w,k=1)
                    if count == 2:
                        enough = True
                    if l.rarity == "Common" or l.rarity == "Rare" and enough == False:
                        self.loot.add(l)
                        if l.rarity == "Rare":
                            count+=1
                    elif l.rarity == "Common" and enough==True:
                        self.loot.add(l)
                    elif l.rarity == "Unique" and enough==False:
                        if count < 3:
                            self.loot.add(l)
                            enough = True
            case 3: # decent chance for unique and rare
                while len(self.loot)<7: # limit 3 unique and at most 4 rare. May not have any common.
                    l = random.choices(deck,w,k=1)
                    if count == 4:
                        enough = True
                    if l.rarity == "Common" or l.rarity == "Rare" and enough == False:
                        self.loot.add(l)
                        if l.rarity == "Rare":
                            count+=1
                    elif l.rarity == "Common" and enough==True:
                        self.loot.add(l)
                    elif l.rarity == "Unique" and enough==False:
                        if count < 3:
                            self.loot.add(l)
                            enough = True
            case _: # no unique available
                while len(self.loot)<3:
                    l = random.choices(deck,w,k=1)
                    if count == 2:
                        enough = True
                    if l.rarity == "Common" or l.rarity == "Rare" and enough == False:
                        self.loot.add(l)
                        if l.rarity == "Rare":
                            count+=1
                    elif l.rarity == "Common" and enough==True:
                        self.loot.add(l)
        for i in self.loot:
            deck.remove(i)
    
# list of rooms I can randomize and then in second half I add the exit room to the list

#setup done outside the class
async def setup(bot):
    bot.add_cog(Rogues(bot))

'''2/13/26 Note: Move/remove the next room check when moving rooms so that the player can still go to previous rooms.
                 Find out why Map is looping but not responding to the interaction.'''

# Notes:
# Spells that still need to be implemented FULLY: Polymorph, Soul Knot, Wish, Za Warudo. Also Steal and Blood Altar
# Need to go back to floorplan and prepare to make all rooms in all floors
# Finish Room Events
# At some point make enemies
# Reminder to keep teardown up to date
# When dealing with Rooms make an exit check that will happen each time a room has been entered by a player
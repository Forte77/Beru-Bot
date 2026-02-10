import nextcord
from nextcord.ext import commands
from nextcord.ext import tasks
from nextcord.member import Member
import yt_dlp
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
# Need a join, leave, play, pause, skip, queue, and maybe move command
class Music(commands.Cog):
    #initialize Cog class..Don't have to redo bot and intents stuff.
    def __init__(self,bot): #not async
        self.bot = bot
    queueList = [] # Set these lists up
    deleteLater = [] # delete the songs after
    @commands.command() # Join VC
    async def join(self,ctx):
        if ctx.author.voice is None: # Make sure the user is in a VC
            await ctx.send("Join a VC first")
        else:
            channel = ctx.author.voice.channel
        if ctx.voice_client is not None: #if it's somewhere else. move.
            await ctx.voice_client.move_to(channel)
            print("moved and joined")
        else:
            await channel.connect() # connects to the vc
            print("joined")
    @commands.command() # Leave VC
    async def leave(self,ctx, help = "leaves the Voice Channel"):
        await ctx.voice_client.disconnect()
        print("leaving")
    # pip install yt_dlp
    @commands.command() # Play a song
    async def play(self,ctx,*,searchword): # takes context and search
        ydl_opts = {} # Options that ydl library takes in so it knows how to download specific files
        # Get Title
        if searchword[0:4] == "http" or searchword[0:3] == "www":
            with yt_dlp.YoutubeDL(ydl_opts) as ydl: # syntax from youtube_dl
                info = ydl.extract_info(searchword,download=False) #extracts info from search result
                title = info["title"]
        if searchword[0:4] != "http" or searchword[0:3] != "www":
            with yt_dlp.YoutubeDL(ydl_opts) as ydl: # syntax from youtube_dl
                info = ydl.extract_info(f"ytsearch: {searchword}",download=False)["entries"][0] #extracts info from search result
                title = info["title"]
                url = info["webpage_url"]
        
        ydl_opts = {
            "format" : "bestaudio/best",
            "outtmp1" : f"{title}.mp3",
            "postprocessors":
            [{"key" : "FFmpegExtractAudio", "preferredcodec" : "mp3", "preferredquality": "192"}]
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.dl([url])
        print("playing")
#Setup
async def setup(bot):
    bot.add_cog(Music(bot))
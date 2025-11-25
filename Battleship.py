import nextcord
from nextcord.ext import commands
#Cog Syntax:
class Battleship(commands.Cog):
    #initialize MyCog class..Don't have to redo bot and intents stuff.
    def __init__(self,bot): #not async
        self.bot = bot
        self.playing = False
        self.board1 = ""
        self.board2 = ""
        self.displayboard1 = ""
        self.displayboard2 = ""
        self.placed1 = False
        self.placed2 = False
        self.turn = ""
    async def render(self,ctx,board):
        numbers = [":one:",":two:",":three:",":four:",":five:",":six:",":seven:",":eight:",":nine:",":ten:"] #setting up column
        alphabet = [":regional_indicator_a:",":regional_indicator_b:",":regional_indicator_c:",":regional_indicator_d:",":regional_indicator_e:",":regional_indicator_f:",":regional_indicator_g:",":regional_indicator_h:",":regional_indicator_i:",":regional_indicator_j:",] #setting up row
        stringboard = "" 
        stringboard = stringboard + ":black_medium_square:" #initialize board with the black square in the corner
        for x in range(len(board[0])): #making the row of letters and going to the next row
            stringboard = stringboard + alphabet[x]
        stringboard = stringboard + "\n"
        i = 0
        for row in board: #nesting loop for creating the rest of the board
            stringboard = stringboard + numbers[i]
            i = i +1
            for square in row:
                stringboard = stringboard + square
            stringboard = stringboard + "\n"
        await ctx.send(stringboard)
        # Example of how the board will be
        #[[':blue_square:',':blue_square:',':blue_square:',':blue_square:',':blue_square:'],
         #[':blue_square:',':blue_square:',':blue_square:',':blue_square:',':blue_square:'],
         #[':blue_square:',':blue_square:',':blue_square:',':blue_square:',':blue_square:'],
         #[':blue_square:',':blue_square:',':blue_square:',':blue_square:',':blue_square:'],
         #[':blue_square:',':blue_square:',':blue_square:',':blue_square:',':blue_square:'],]
    @commands.command()
    async def battleship(self,ctx, player2 : nextcord.Member,ver : int = 5, hor : int = 5):
        if self.playing == False: # using global variables. checking if a game is going
            if self.placed1 == False and self.placed2 == False:#checking if a game has started and placements haven't started.
                self.playing = True
                self.player1 = ctx.author
                self.player2 = player2
                self.turn = self.player1
                self.board1 = [[":blue_square:"]*hor for x in range(ver)]
                self.board2 = [[":blue_square:"]*hor for x in range(ver)]
                self.displayboard1 = [[":blue_square:"]*hor for x in range(ver)]
                self.displayboard2 = [[":blue_square:"]*hor for x in range(ver)]
                await self.render(self.player1,self.board1)
                await self.render(self.player2,self.board2) 
                await self.player1.send("Welcome to Battleship! Type ?place to place your ships. Ex: ?place a3 b2 a1 c5...")
                await self.player2.send("Welcome to Battleship! Type ?place to place your ships. Ex: ?place a3 b2 a1 c5...")
            else:
                await ctx.send("Not all ships have been placed.")
        else:
            await ctx.send("There is already a game being played between",self.player1," and ",self.player2)
    def shipcount(self,board):
        count = 0
        for row in board:
            for square in row:
                if square == ":ship:":
                    count = count+1
        return count
    @commands.command()
    async def place(self,ctx,*coordinates):
        if self.playing == True:
            if self.placed1 == False or self.placed2 == False:
                if ctx.author == self.player1:
                    board = self.board1
                if ctx.author == self.player2:
                    board = self.board2
                if len(coordinates) == 0:
                    await ctx.send("Please type in the coordinates with the ?place command")
                for coordinate in coordinates:
                    if self.shipcount(board) == 6:
                        await ctx.send("No more than 6 ships.")
                    else:
                        alphabet = coordinate[0]
                        numbers = coordinate[1]
                        loweralphabet = alphabet.lower()
                        x = ord(loweralphabet) - 97 #ord converts alphabet to numbers but a starts at 97 and we need it at zero
                        y = int(numbers) - 1 # subtract one to line up properly
                        if board[y][x] != ":ship:":
                            board[y][x] = ":ship:"
                        else:
                            await ctx.send("One of you tried a duplicate placement! This will be ignored.")
                if self.shipcount(board) == 6:
                    if ctx.author == self.player1:
                            self.placed1 = True
                    if ctx.author == self.player2:
                            self.placed2 = True
                    if self.placed1 == True and self.placed2 == True:
                        await self.player1.send("All ships have been placed. It is now your turn to shoot. Use ?shoot [x][y]")
                        await self.player2.send("All ships have been placed. It is now Player 1's turn to shoot.")
                else:
                    await ctx.send("You have not placed all six of your ships")
                await self.render(ctx.author,board)
            elif self.placed1 == True and self.placed2 == True:
                await ctx.send("All ships have already been placed.")
            else:
                await ctx.send("Not all ships have been placed.")
        else:
            await ctx.send("Please start a game of battleship first. Use ?battleship @member [x] [y]")
    @commands.command()
    async def shoot(self,ctx,coordinate):
        if self.turn == ctx.author:
            if self.playing == True:#if a game has started
                if self.placed1 == True or self.placed2 == True:
                    if ctx.author == self.player1:
                        shootboard = self.board2
                        displayboard = self.displayboard2
                        nextTurn = self.player2
                    if ctx.author == self.player2:
                        shootboard = self.board1
                        displayboard = self.displayboard1
                        nextTurn = self.player1
                    loweralphabet = coordinate[0].lower()
                    numbers = coordinate[1]
                    skip = False
                    x = ord(loweralphabet) - 97 #ord converts alphabet to numbers but a starts at 97 and we need it at zero
                    y = int(numbers) - 1 # subtract one to line up properly
                    square = shootboard[y][x]
                    if square == ":ship:":#hit
                        await ctx.send("HIT!")
                        shootboard[y][x] = ":boom:"
                        displayboard[y][x] = ":boom:"
                        await ctx.send("Go AGAIN!!") # Letting the player know they can go again
                        if ctx.author == self.player1: # Telling the other player they have been hit.
                            #print("Test player 1")
                            await self.player2.send("Your ship has been hit!\nWhat your opponent sees: ")
                            await self.render(self.player2,displayboard)
                            skip = True
                        if ctx.author == self.player2: # Telling the other player they have been hit.
                            #print("Test player 2")
                            await self.player1.send("Your ship has been hit!\nWhat your opponent sees: ")
                            await self.render(self.player1,displayboard)
                            skip = True
                    if square == ":blue_square:":#miss
                        await ctx.send("*MISS!*")
                        shootboard[y][x] = ":white_medium_square:"
                        displayboard[y][x] = ":white_medium_square:"
                        self.turn = nextTurn #Changing turn
                        await self.turn.send("It is now your turn to shoot. Use ?shoot [x][y]")
                    if square ==":white_medium_square:" or square == "boom":#dumb
                        await ctx.send("You...you already did that one.... try again.")
                    #print(skip)
                    if skip == False: #Had to add this cuz I found out I can't render the board twice basically.
                        await self.render(ctx.author,displayboard) #update board
                    if self.shipcount(shootboard) == 0: #end the game
                        self.playing = False
                        #Notify players who won
                        if ctx.author == self.player1:
                            await self.player1.send("You have won the battle!")
                            await self.player2.send("You have lost the battle.")
                            await self.render(self.player1,self.board2)
                            await self.render(self.player2,self.board1)
                        if ctx.author == self.player2:
                            await self.player2.send("You have won the battle!")
                            await self.player1.send("You have lost the battle.")
                            await self.render(self.player2,self.board1)
                            await self.render(self.player1,self.board2)
            else:
                await ctx.send("Please start a game of battleship first. Use ?battleship @member [x] [y]")            
        else:
            await ctx.send("Not your turn")
    @battleship.error
    async def errorhandler(self,ctx,error):
        if isinstance(error,commands.errors.MissingRequiredArgument):
            await ctx.send("Please mention the second player.")
    @place.error
    async def errorhandler(self,ctx,error):
        if isinstance(error,commands.errors.CommandInvokeError):
            await ctx.send("Stay in bounds!")
    @shoot.error
    async def errorhandler(self,ctx,error):
        if isinstance(error,commands.errors.MissingRequiredArgument):
            await ctx.send("Please define the coordinate")
        if isinstance(error,commands.errors.TooManyArguments):
            await ctx.send("You can only shoot at one coordinate at a time.")
#setup done outside the class
async def setup(bot):
    await bot.add_cog(Battleship(bot))

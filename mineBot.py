import discord
from discord.ext import commands
import random
import os

client = commands.Bot(command_prefix="!", intents = discord.Intents.all())

WIDTH = 8
HEIGHT = 8


gameboard = []
num_mines = 10
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

squares = [':one:',':two:',':three:',':four:',':five:',':six:',':seven:',':eight:']
green_square = ':green_square:'
unplayed_space = ':blue_square:'
mine = ':bomb:'

game_over = False


def make_empty_board():
    for row in range(WIDTH):
        gameboard.append([])
        for col in range(HEIGHT):
            gameboard[row].append(unplayed_space)


def place_mines(num_mines):
    global mineMap
    mineMap = []
    for row in range(WIDTH):
        mineMap.append([])
        for col in range(HEIGHT):
            mineMap[row].append(0)
    for i in range (0,num_mines):
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)
        if mineMap[x][y] == 0:
            mineMap[x][y] = -1

def board_to_string():
    row_strings = []
    for row in gameboard:
        row_string = ''
        for cell in row:
            row_string += cell
        row_strings.append(row_string)
    return '\n'.join(row_strings)

def count_surrounding_mines(x, y):
    mine_count = 0
    #for direction x and direction y
    for dx, dy in DIRECTIONS:
        #direction x + user placed x
        #direction y + user placed y
        #Locates area on map user placed + directions to check
        nx, ny = x + dx, y + dy
        if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
            if mineMap[nx][ny] == -1:
                mine_count +=1
    return mine_count

def check_win():
    for row in range(WIDTH):
        for col in range(HEIGHT):
            if gameboard[row][col] == unplayed_space and mineMap[row][col] != -1:
                return False
    return True

def reveal_mines():
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if mineMap[x][y] == -1:
                gameboard[x][y] = mine

def reset_board():
    global gameboard, mineMap, game_over  # Reset global variables
    gameboard = []
    mineMap = []
    game_over = False  # Reset game over status

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.command()
async def start(ctx):
    reset_board()
    make_empty_board()
    place_mines(num_mines)
    board_string = board_to_string()
    await ctx.send("Here is your board")
    await ctx.send(board_string)
    await ctx.send("Use !place and an x and y co-ordinate for example !place 2 6")


@client.command()
async def place(ctx, x: int, y:int):
    global game_over
    if game_over == True:
        await ctx.send("The game is over start a new game!")
        return
    x = x - 1
    y = y - 1
    if 0 <= x < WIDTH and 0 <= y < HEIGHT: 
        if (mineMap[x][y] == -1): #Detect if Hit
            game_over = True
            await ctx.send("OUCH! You hit a mine! Game Over")
            gameboard[x][y] = mine
            board_string = board_to_string()
            await ctx.send("Updated board:")
            await ctx.send(board_string)
        else:
            mine_count = count_surrounding_mines(x, y)
            if mine_count > 0:
                gameboard[x][y] = squares[mine_count - 1]
            else:
                gameboard[x][y] = green_square
            board_string = board_to_string()
            await ctx.send("Updated board:")
            await ctx.send(board_string)

            if check_win():
                await ctx.send("Congratulations you have cleareda all the mines you WIN!")
                reveal_mines()
                await ctx.send("Final board with mines revealed")
                board_string = board_to_string()
                await ctx.send(board_string)
                game_over = True
    else:
        await ctx.send("Invalid Co-ordinates")

        
client.run('TOKEN')
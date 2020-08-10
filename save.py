# ---------- LIBRARIES ---------- # (0)

from random import randrange, random as randf, seed
import json
from math import *
import re
from time import perf_counter, sleep

# ---------- LIBRARIES ---------- # (0)




# ---------- CONSTANTS ---------- # (1)

TPS = 30 # ticks per second

TILE_SIZE = 1 # cm²

TIME_REG = {
    "hours": r"(\d+) ?h(?:our)?s?",
    "minutes": r"(\d+) ?m(?:inute|in)?s?",
    "seconds": r"(\d+) ?(?:second|sec)?s? ?(?!.)",
    "time": r"(?:(?:\d+) ?(?:h(?:our)?|m(?:inute|in)?|(?:second|sec)?)s?,?(?: ?and)? ?){1,3}"
}

SHIP = {
    "Liberty Ship":{
        "tonnage":0,
        "speed":11,
        "nationaity":"USA"
    }
}

# ---------- CONSTANTS ---------- # (1)




# ---------- CLASS OBJECTS ---------- # (2)

class vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        if type(x) == list or type(x) == tuple:
            self.y = x[1]
            self.x = x[0]
    
    def __str__(self): return "vector"

    def value(self): return (self.x, self.y)

    def length(self): return sqrt((self.x**2)+(self.y**2))

    def __len__(self): return round(self.length())

    def __getitem__(self, key): return self.value()[key]

    def normalize(self): return vector(self.x/max(x,y),self.y/max(x,y))

    def rotated(self, deg):
        rot = atan2(self.x,self.y)+radians(deg)
        return vector(sin(rot),cos(rot))

    def __add__(self, other):
        if other == "vector" and type(other) != str: return vector(self.x+other.x,self.y+other.y)
        else: return vector(self.x+other,self.y+other)

    def __sub__(self, other):
        if other == "vector" and type(other) != str: return vector(self.x-other.x,self.y-other.y)
        else: return vector(self.x-other,self.y-other)
    
    def __mul__(self,other):
        if other == "vector" and type(other) != str: return vector(self.x*other.x,self.y*other.y)
        else: return vector(self.x*other,self.y*other)
    
    def __truediv__(self, other):
        if other == "vector" and type(other) != str: return vector(self.x/other.x,self.y/other.y)
        else: return vector(self.x/other,self.y/other)
    
    def __floordiv(self, other):
        if other == "vector" and type(other) != str: return vector(self.x//other.x,self.y//other.y)
        else: return vector(self.x//other,self.y//other)

    def __mod__(self, other):
        if other == "vector" and type(other) != str: return vector(self.x%other.x,self.y%other.y)
        else: return vector(self.x%other,self.y%other)

    def __pow__(self, other):
        if other == "vector" and type(other) != str: return vector(self.x**other.x,self.y**other.y)
        else: return vector(self.x**other,self.y**other)
    
    def __eq__(self, other):
        if other == "vector" and type(other) != str: return self.value() == other.value()
        else: return "vector" == other
    
    def __ne__(self, other):
        if other == "vector" and type(other) != str: return self.value() != other.value()
        else: return self != other


class ship:
    def __init__(self, **args):
        self.type = ""
        self.position = vector()
        self.health = 100
        self.heading = 0
        self.speed = 0
        self.depth = 0
        self.destination = vector()

        self.__dict__.update(args)

    def ticktile(self, knots): return knots * 185200 * TILE_SIZE / (60**2 * TPS) # knots to tiles per tick

    def hit(self, dmg):
        self.health -= dmg

    def goto(self, pos, speed=0):
        speed = SHIP[self.type]["speed"]
        direction = (pos-self.position).normalize()
        direction = atan2(direction.x,direction.y)

    def __move(self):
        self.position = self.position + vector(self.ticktile(self.speed)).rotated(self.heading)

    def tick(self):


        pass

        self.__move()

# ---------- CLASS OBJECTS ---------- # (2)




# ---------- GLOBAL VARIABLES ---------- # (3)

current_game = ""

game = {
    "ships":[]#ship(**{"type":"Liberty Ship","position":vector(randrange(0,7000))}) for _ in range(10**6)]
}
# ---------- GLOBAL VARIABLES ---------- # (3)




# ---------- NON GAMEPLAY ---------- # (4)

def ask(question):
    answer = ""
    while answer != "n" or answer != "y":
        answer = input(str(question)+" [y/n]").lower() 
        if answer == "y": return True
        elif answer == "n": return False
        else: print('Invalid input: Answer must be "y" or "n".')

# ---------- NON GAMEPLAY ---------- # (4)




# ---------- SAVE/LOAD ---------- # (5)

def save():
    global current_game
    with open(current_game+".json", "w") as gamefile:
        json.dump(game,gamefile,sort_keys=True,indent=4)

def load(game_name):
    global game
    global current_game
    try:
        with open(game_name+".json", "r") as gamefile:
            game = json.load(gamefile)
        current_game = game_name
        print("Game loaded.")
    except FileNotFoundError:
        print("File does not exist.")

def new_game(game_name):
    global game
    global current_game
    current_game = game_name
    
    if ask("Would you like a random game seed?"): seed()
    else: seed(input("Insert game seed:\n"))
    
    print("Creating game...")

    generate_ships()
    
    print("Created new game - "+game_name)
    save()

# ---------- SAVE/LOAD ---------- # (5)




# ---------- PROCESS ---------- # (6)

def _process():
    for ship in game["ships"]:
        ship.tick()

# ---------- PROCESS ---------- # (6)




# ---------- GAMEPLAY ---------- # (7)

def wait(wait_time):
    start = perf_counter()
    wait_time = str(wait_time).lower()

    if not re.fullmatch(TIME_REG["time"], wait_time):
        return print("Invalid input.")

    else:

        total_sec = 0

        for i in range(3):
            x = ["seconds","minutes","hours"]
            if re.search(TIME_REG[x[i]], wait_time):
                total_sec += int(re.search(TIME_REG[x[i]], wait_time).group(1))*60**i
    


        print("Calculating...")

        for tick in range(total_sec*TPS):
            _process()

        
        # elapsed time

        delay = str(round((perf_counter()-start)*10**5)/100)

        s = ""
        if total_sec != 1: s = "s"

        print(f"Calculated {total_sec} game second{s} within {delay} milliseconds.")

# ---------- GAMEPLAY ---------- # (7)




# ---------- START GAME ---------- # (8)

# while current_game == "":
#     if ask("Would you like to create a new game?"):

#         game_name = input("Insert game name:\n")

#         try:
#             with open(game_name+".json", "r") as x:
#                 print("File already exists.")

#         except FileNotFoundError:
#             new_game(game_name)

#     else: load(input("Insert the name of the game you would like to load:\n"))

# ---------- START GAME ---------- # (8)



# ---------- LIBRARIES ---------- # (0)

from random import seed
import json
from math import *
import re
from time import perf_counter

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

class Vector:
    def __init__(self, x:float=0, y:float=0) -> None:
        self.x = x
        self.y = y
        if type(x) == list or type(x) == tuple:
            self.y = x[1]
            self.x = x[0]
    
    def __str__(self) -> str: return str(self.value)

    @property
    def value(self) -> tuple: return (self.x, self.y)

    @property
    def length_squared(self) -> float: return (self.x**2) + (self.y**2)

    @property
    def length(self) -> float: return sqrt(self.length_squared)

    def __len__(self) -> int: return round(self.length)

    def __getitem__(self, key) -> float: return self.value[key]

    def normalized(self) -> Vector: return Vector(self.x/max(self.x,self.y),self.y/max(self.x,self.y))

    def rotated(self, deg:float) -> Vector:
        rot = atan2(self.x,self.y) + radians(deg)
        return Vector(sin(rot),cos(rot))

    def __add__(self, other) -> Vector:
        if type(other) == Vector: return Vector(self.x+other.x,self.y+other.y)
        else: return Vector(self.x+other,self.y+other)

    def __sub__(self, other) -> Vector:
        if type(other) == Vector: return Vector(self.x-other.x,self.y-other.y)
        else: return Vector(self.x-other,self.y-other)
    
    def __mul__(self,other) -> Vector:
        if type(other) == Vector: return Vector(self.x*other.x,self.y*other.y)
        else: return Vector(self.x*other,self.y*other)
    
    def __truediv__(self, other) -> Vector:
        if type(other) == Vector: return Vector(self.x/other.x,self.y/other.y)
        else: return Vector(self.x/other,self.y/other)
    
    def __floordiv__(self, other) -> Vector:
        if type(other) == Vector: return Vector(self.x//other.x,self.y//other.y)
        else: return Vector(self.x//other,self.y//other)

    def __mod__(self, other) -> Vector:
        if type(other) == Vector: return Vector(self.x%other.x,self.y%other.y)
        else: return Vector(self.x%other,self.y%other)

    def __pow__(self, other) -> Vector:
        if type(other) == Vector: return Vector(self.x**other.x,self.y**other.y)
        else: return Vector(self.x**other,self.y**other)
    
    def __eq__(self, other) -> bool:
        if type(other) == Vector: return self.value == other.value
        else: return "vector" == other
    
    def __ne__(self, other) -> bool:
        if type(other) == Vector: return self.value != other.value
        else: return self != other


class Ship:
    def __init__(self, **args) -> None:
        self.type = ""
        self.position = Vector()
        self.health = 100
        self.heading = 0
        self.speed = 0
        self.depth = 0
        self.destination = Vector()

        self.__dict__.update(args)

    def ticktile(self, knots:float) -> float: return knots * 185200 * TILE_SIZE / (60**2 * TPS) # knots to tiles per tick

    def hit(self, dmg:float) -> None:
        self.health -= dmg

    def goto(self, pos:Vector, speed:float=0) -> None:
        speed = SHIP[self.type]["speed"]
        direction = (pos-self.position).normalize()
        direction = atan2(direction.x,direction.y)

    def _move(self) -> None:
        self.position = self.position + Vector(self.ticktile(self.speed)).rotated(self.heading)

    def tick(self) -> None:


        pass

        self._move()

# ---------- CLASS OBJECTS ---------- # (2)




# ---------- GLOBAL VARIABLES ---------- # (3)


game = {
    "name": "",
    "ships":[]#Ship(**{"type":"Liberty Ship","position":vector(randrange(0,7000))}) for _ in range(10**6)]
}
# ---------- GLOBAL VARIABLES ---------- # (3)




# ---------- NON GAMEPLAY ---------- # (4)

def ask(question:str) -> bool:
    answer = ""
    while answer != "n" or answer != "y":
        answer = input(str(question)+" [y/n]").lower() 
        if answer == "y": return True
        elif answer == "n": return False
        else: print('Invalid input: Answer must be "y" or "n".')

# ---------- NON GAMEPLAY ---------- # (4)




# ---------- SAVE/LOAD ---------- # (5)

def save() -> None:
    global game
    with open(game["name"]+".json", "w") as f:
        json.dump(game,f,sort_keys=True,indent=4)

def load(game_name:str) -> None:
    global game
    try:
        with open(game_name+".json", "r") as f:
            game = json.load(f)
        game["name"] = game_name
        print("Game loaded.")
    except FileNotFoundError:
        print("File does not exist.")

def new_game(game_name:str) -> None:
    global game
    game["name"] = game_name
    
    if ask("Would you like a random game seed?"): seed()
    else: seed(input("Insert game seed:\n"))
    
    print("Creating game...")

    #generate_ships()
    
    print("Created new game - "+game_name)
    save()

# ---------- SAVE/LOAD ---------- # (5)




# ---------- PROCESS ---------- # (6)

def _process() -> None:
    for ship in game["ships"]:
        ship.tick()

# ---------- PROCESS ---------- # (6)




# ---------- GAMEPLAY ---------- # (7)

def wait(wait_time) -> None:
    start = perf_counter()
    wait_time = str(wait_time).lower()

    if not re.fullmatch(TIME_REG["time"], wait_time):
        return print("Invalid input.")

    else:

        total_sec = 0

        for i in range(3):
            current_regex = TIME_REG[["seconds","minutes","hours"][i]]
            match = re.search(current_regex, wait_time)
            if match: total_sec += int(match.group(1))*60**i
    

        print("Calculating...")

        for _ in range(total_sec*TPS):
            _process()

        
        # elapsed time

        delay = str(round((perf_counter()-start)*10**5)/100)

        s = "" if total_sec == 1 else "s"

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



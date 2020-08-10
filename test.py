from random import randrange, random as randf, seed
import json
from math import *
import re
from time import perf_counter, sleep


TIME_REG = {
    "hours": r"(\d+) ?h(?:our)?s?",
    "minutes": r"(\d+) ?m(?:inute|in)?s?",
    "seconds": r"(\d+) ?(?:second|sec)?s? ?(?!.)",
    "time": r"(?:(?:\d+) ?(?:h(?:our)?|m(?:inute|in)?|(?:second|sec)?)s?,?(?: ?and)? ?){1,3}"
}


SHIPS = {
    "Liberty Ship":{
        "tonnage":0,
        "speed":11,
        "nationaity":"USA"
    }
}


# ---------- CLASS OBJECTS ()

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

    def hit(self, dmg):
        self.health -= dmg

    def set_speed(self, new_speed):
        speed

    def goto(self, pos, speed=0):
        speed = SHIPS[self.type]["speed"]
        direction = (pos-self.position).normalize()
        direction = atan2(direction.x,direction.y)

    def __move(self):
        return self.position + vector(self.speed).rotated(self.heading)

    def tick(self):


        pass

        self.position = self.__move()





game = {
    "name":"",
    "ships":[
        ship(type="Type VIIC U-boat"),ship(type="Liberty Ship")
    ]
}



















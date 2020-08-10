from math import *
from save import vector

lon = 4007501700 / 360
lat = 3994065300 / 360


def pos2map(pos):
    return vector(pos.y/lat,pos.x/lon)


position = vector(473,2996) * 10**5 * 2

print(pos2map(position).value())
print(position.length() / 10**5)



#1288
#   53.89997003804619, 8.803489715300683


# (54.00813051303893, 8.498062521096374)
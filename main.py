from b_test import *

game = Battleship()

import random
for b in boats.keys():
    coords = None
    while coords is None:
        print('trying to place')
        pos = (random.randint(0, 9), random.randint(0, 9))
        coords = game.placeboat(b, pos, random.randint(0,1))

print(game.drawboard())
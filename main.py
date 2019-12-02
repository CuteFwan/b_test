from b_test import *

game = Battleship()

import random
for b in boats.keys():
    coords = None
    while coords is None:
        print('trying to place')
        pos = (random.randint(0, 9), random.randint(0, 9))
        coords = game.placeboat(b, pos, random.randint(0,1))

i = 0
while True:
    x, y = random.choice(game.gethitboard(False))
    spot = game.attack((x, y))
    i += 1


print(game.drawboard('boats'))
print(game.drawboard('hits'))
print(game.drawboard())
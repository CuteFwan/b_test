from b_test import *

game = Battleship()

import random
for b in boats.keys():
    coords = None
    while coords is None:
        print('trying to place')
        pos = (random.randint(0, 9), random.randint(0, 9))
        coords = game.placeboat(b, pos, random.randint(0,1))

for h in range(10):
    x, y = random.randint(0, 9),random.randint(0, 9)
    spot = game.attack((x, y))
    print(x, y, spot)

print(game.drawboard('boats'))
print(game.drawboard('hits'))
print(game.drawboard())
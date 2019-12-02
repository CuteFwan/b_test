from b_test import *


game = Battleship()

import random
for boat, size in boats.items():
    coords = None
    while coords is None:
        rotated = bool(random.randint(0,1))
        pos = (random.randint(0, (9 - size) if not rotated else 9), random.randint(0, (9 - size) if rotated else 9))
        #print(f'trying to place {boat} on {pos}')
        coords = game.placeboat(boat, pos, rotated)

i = 0
'''
# totally random
while True:
    i += 1

    x, y = random.choice(game.gethitboard(False))
    spot = game.attack((x, y))

    if game.checkwin():
        break
'''
# some strategy
chain = []
while True:
    i += 1

    possible = game.gethitboard(False)

    x, y = random.choice([(x, y) for x, y in possible if (x + y) % 2 == 0]) if not chain else chain.pop()

    spot = game.attack((x, y))


    if spot != ' ':
        surrounding = [(x + xx, y + yy) for xx in range(-1,2,1) for yy in range(-1,2,1) if (0 <= x + xx < 10) and (0 <= y + yy < 10) and (xx == 0 or yy == 0) and not (xx == 0 and yy == 0)]
        chain.extend(list(set(surrounding) & set(possible)))
        chain = list(set(chain))

    if game.checkwin():
        break



print(f'won in {i} hits')

print(game.drawboard('boats'))
print('\n')
print(game.drawboard('hits'))
print('\n')
print(game.drawboard())
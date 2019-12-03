from b_test import *
import random

def setupgame():
    game = Battleship()

    for boat, size in boats.items():
        coords = None
        while coords is None:
            rotated = bool(random.randint(0,1))
            pos = (random.randint(0, (9 - size) if not rotated else 9), random.randint(0, (9 - size) if rotated else 9))
            #print(f'trying to place {boat} on {pos}')
            coords = game.placeboat(boat, pos, rotated)
    return game

def gethitboardstats(board, boatsalive):
    statboard = {(x, y) : 0 for x in range(10) for y in range(10)}
    for boat in boatsalive:
        boatsize = boats[boat]
        for r in range(2):
            for y in range(10):
                start = 0
                end = 0
                for x in range(10):
                    if r == 0:
                        spot = board[x,y]
                    else:
                        spot = board[y,x]
                    if spot == False:
                        end += 1
                    if spot == True or x == 9:
                        end -= 1
                        gap = (1 + end - start)
                        if gap >= boatsize:
                            # If the gap is large enough to fit at least one boat
                            h = 0
                            for i in range(gap):
                                if i <= (gap - boatsize):
                                    h += 1
                                if i >= boatsize:
                                    h -= 1
                                if r == 0:
                                    statboard[i+start,y] += h
                                else:
                                    statboard[y, i+start] += h
                        if x > (10 - boatsize):
                            break
                        else:
                            start = x + 1
                            end = start
                    
    return statboard

def rando(game):
    # totally random
    i = 0
    while True:
        i += 1

        x, y = random.choice(list(game.gethitboard('nothit').keys()))
        spot = game.attack((x, y))

        if game.checkwin():
            break
    return i

def hunt(game):
    # some strategy
    chain = []
    i = 0
    while True:
        i += 1

        possible = game.gethitboard('nothit').keys()

        x, y = random.choice([(x, y) for x, y in possible if (x + y) % 2 == 0]) if not chain else chain.pop()

        spot = game.attack((x, y))


        if spot != ' ':
            surrounding = [(x + xx, y + yy) for xx in range(-1,2,1) for yy in range(-1,2,1) if (0 <= x + xx < 10) and (0 <= y + yy < 10) and (xx == 0 or yy == 0) and not (xx == 0 and yy == 0)]
            chain.extend(list(set(surrounding) & set(possible)))
            chain = list(set(chain))

        if game.checkwin():
            break
    return i

def stats(game):
    # some statistics applied
    i = 0
    chain = []
    while True:
        i += 1

        possible = game.gethitboard('nothit').keys()

        aliveboats = [boat for boat in boats.keys() if game.checkboat(boat) == False]
        statboard = gethitboardstats(game.gethitboard('full'), aliveboats)


        x, y = random.choices(list(statboard.keys()), list(statboard.values()))[0] if not chain else chain.pop()

        spot = game.attack((x, y))


        if spot != ' ':
            surrounding = [(x + xx, y + yy) for xx in range(-1,2,1) for yy in range(-1,2,1) if (0 <= x + xx < 10) and (0 <= y + yy < 10) and (xx == 0 or yy == 0) and not (xx == 0 and yy == 0)]
            chain.extend(list(set(surrounding) & set(possible)))
            chain = list(set(chain))

        if game.checkwin():
            break
    return i



total = 0
for t in range(1000):
    game = setupgame()
    
    turns = rando(game)
    total += turns

print(total/1000)

total = 0
for t in range(1000):
    game = setupgame()
    
    turns = hunt(game)
    total += turns

print(total/1000)

total = 0
for t in range(1000):
    game = setupgame()
    
    turns = stats(game)
    total += turns

print(total/1000)
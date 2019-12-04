import random
import json

from .battleships import boats

class rando:
    def __init__(self, game):
        self.game = game
    def nextturn(self, opponentgame):

        x, y = random.choice(list(game.gethitboard('nothit').keys()))
        spot = game.attack((x, y))

        return (x,y), spot

class hunt:
    def __init__(self, game):
        self.game = game
        self.chain = []

    def nextturn(self, opponentgame):
        possible = opponentgame.gethitboard('nothit').keys()

        x, y = random.choice([(x, y) for x, y in possible if (x + y) % 2 == 0]) if not self.chain else self.chain.pop()

        spot = opponentgame.attack((x, y))

        if spot != ' ':
            surrounding = [(x + xx, y + yy) for xx in range(-1,2,1) for yy in range(-1,2,1) if (0 <= x + xx < 10) and (0 <= y + yy < 10) and (xx == 0 or yy == 0) and not (xx == 0 and yy == 0)]
            self.chain.extend(list(set(surrounding) & set(possible)))
            self.chain = list(set(self.chain))

        return (x,y), spot

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

class stats:
    def __init__(self, game):
        self.game = game
        self.chain = []

    def nextturn(self, opponentgame):
        possible = opponentgame.gethitboard('nothit').keys()

        aliveboats = [boat for boat in boats.keys() if opponentgame.checkboat(boat) == False]
        statboard = gethitboardstats(opponentgame.gethitboard('full'), aliveboats)


        x, y = random.choices(list(statboard.keys()), list(statboard.values()))[0] if not self.chain else self.chain.pop()

        spot = opponentgame.attack((x, y))

        if spot != ' ':
            surrounding = [(x + xx, y + yy) for xx in range(-1,2,1) for yy in range(-1,2,1) if (0 <= x + xx < 10) and (0 <= y + yy < 10) and (xx == 0 or yy == 0) and not (xx == 0 and yy == 0)]
            self.chain.extend(list(set(surrounding) & set(possible)))
            self.chain = list(set(self.chain))

        return (x,y), spot

class history:
    def __init__(self, game):
        self.game = game
        self.chain = []
        with open('b_test/history.json', 'r') as f:
            data = json.load(f)
            self.hithistory = {(x,y) : data[x+y*10] for y in range(10) for x in range(10)}

    def normalize(self, statboard):
        total = sum(statboard.values())
        if total == 0:
            return statboard
        return {(xy) : v/total for xy, v in statboard.items()}

    def nextturn(self, opponentgame):
        possible = opponentgame.gethitboard('nothit').keys()

        aliveboats = [boat for boat in boats.keys() if opponentgame.checkboat(boat) == False]
        statboard = gethitboardstats(opponentgame.gethitboard('full'), aliveboats)
        tempstatboard = self.normalize(statboard)
        temphithistory = self.normalize(self.hithistory)
        statboard = {(x, y) : max(0, tempstatboard[x,y] + temphithistory[x,y]) if statboard[x,y] != 0 else 0 for y in range(10) for x in range(10)}
        x, y = random.choices(list(statboard.keys()), list(statboard.values()))[0] if not self.chain else self.chain.pop()

        spot = opponentgame.attack((x, y))

        if spot != ' ':
            surrounding = [(x + xx, y + yy) for xx in range(-1,2,1) for yy in range(-1,2,1) if (0 <= x + xx < 10) and (0 <= y + yy < 10) and (xx == 0 or yy == 0) and not (xx == 0 and yy == 0)]
            self.chain.extend(list(set(surrounding) & set(possible)))
            self.chain = list(set(self.chain))
            self.hithistory[x,y] += 1

        return (x,y), spot

    def save(self):
        with open('b_test/history.json', 'w') as f:
            data = [self.hithistory[x,y] for y in range(10) for x in range(10)]
            json.dump(data, f)

    
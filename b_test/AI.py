import random
import json

from .battleships import boats
from .utils import *

class AI:
    """
    The base class of battleship AIs.

    Classes derived from this should override the :meth:`AI.nextturn` method
    to do the AI logic.
    """
    def nextturn(self, opponentgame):
        """
        The method to override to do the AI logic.

        Should make a single attack upon the opponent's game using the :meth:`Battleship.attack` method
        and return the position and result of the attack.

        Parameters
        ----------
        opponentgame: :class:`Battleship`
            The opponent's game.

        Returns
        -------
        tuple[:class:`tuple`, :class:`str`]
            The position and the result of the attack.
        """
        raise NotImplementedError('Derived classes need to implement this.')

    def save(self):
        """
        Optional method to save any board states for future runs.
        """
        pass


class manually(AI):
    """
    Manual play. All logic is given by user input.
    """

    def __init__(self, game):
        self.game = game
    def nextturn(self, opponentgame):
        print(opponentgame.drawboard("hits"))
        print(self.game.drawboard("full"))
        spot = False
        while spot == False:
            res = input("Attack? ")
            pos = lettertonum(res[0]), int(res[1:]) - 1
            spot = opponentgame.attack(pos)
            if spot == False:
                print("Already hit that spot, try again.")

        return pos, spot

class rando(AI):
    """
    Baseline rng AI.

    Picks a spot randomly on the board that hasn't been hit yet.

    Generally performs poorly, averaging around 95.5/100 shots to win in a test of 1000 games.
    """
    def __init__(self, game):
        self.game = game
    def nextturn(self, opponentgame):
        x, y = random.choice(list(opponentgame.gethitboard('nothit').keys()))
        spot = opponentgame.attack((x, y))

        return (x,y), spot

class hunt(AI):
    """
    Hunt and Target AI.

    Fires randomly at every other spot until a hit has been confirmed before focusing on adjacent spots to sink a ship.
    Uses a simple list to keep track of possible ship locations in adjacent spots.

    Performs considerably better, averaging around 61/100 shots to win in a test of 1000 games.
    """
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

class stats(AI):
    """
    Statistics AI.

    Generates a distribution of possible ship locations based on the spots that had already been hit
    to choose the next spot to attack. Switches to the same method as above to finish sinking a ship
    by firing upon adjacent spots upon hit.

    Performs marginally better, averaging around 50/100 shots to win in a test of 1000 games.
    Run time is generally longer than the previous methods.
    """
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

class history(AI):
    """
    history AI.

    Combines the above method with a simple history of shots landed to try to learn the opponent's ship placement.

    Performance uncertain due to not having a way to automate ship placement in a consistently non-random way yet.
    Seems to run roughly as well as the stats AI.
    """
    def __init__(self, game):
        self.game = game
        self.chain = []
        with open('b_test/history.json', 'r') as f:
            data = json.load(f)
            self.hithistory = {(x,y) : data[x+y*10] for y in range(10) for x in range(10)}

    def normalize(self, statboard):
        """
        Method to normalize the values in a dict to sum to 1.
        Example:
        {a : 1, b : 1} -> {a : 0.5, b : 0.5}
        {a : 1, b : 1, c : 1} -> {a : 0.33, b : 0.33, c : 0.33}
        {a : 1, b : 2} -> {a : 0.33, b : 0.66}

        Parameters
        ----------
        statboard: :class:`dict`
            The dict to normalize
            
        Returns
        -------
        :class:`dict`
            The normalized dict
        """
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

    
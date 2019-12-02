from .utils import letters
boats = {
        'Carrier' : 5,
        'Battleship' : 4,
        'Destroyer' : 3,
        'Submarine' : 3,
        'Patrol Boat' : 2,
        }
        

class Boat:
    def __init__(self, name, board, **kwargs):
        self.name = name
        self.size = boats.get(name)
        if not self.size:
            #Not a valid boat name somehow
            pass
        self.board = board
        self.start = kwargs.pop('start', None)
        self.rotated = kwargs.pop('rotated', False)
        if self.start:
            self.positions = self.placeboat(self.start, self.rotated)

    def canplaceboat(self, pos, rotated):
        temppos = list(pos)
        positions = []
        for i in range(self.size):
            if 0 <= temppos[0] < 10 and 0 <= temppos[1] < 10 and self.board[tuple(temppos)] == ' ':
                positions.append(tuple(temppos))
                temppos[rotated] += 1
            else:
                return None
        self.start = pos
        self.rotated = rotated
        self.positions = positions
        return positions

class Battleship:
    def __init__(self):
        self.hitboard = {(x, y) : False for x in range(10) for y in range(10)}
        self.boatboard = {(x, y) : ' ' for x in range(10) for y in range(10)}
        self.boats = {b : Boat(b, self.boatboard) for b in boats.keys()}

    def placeboat(self, boatname : str, xy : list, rotated : bool = False):

        positions = self.boats[boatname].canplaceboat(xy, rotated)

        if not positions:
            return None

        for p in positions:
            self.boatboard[p] = boatname[0]
        return positions

    def attack(self, xy : list):
        if self.hitboard[xy] == True:
            #Attacking spot already hit
            return False
        spot = self.checkspace(xy)
        self.hitboard[xy] = True
        return spot

    def checkspace(self, xy : list):
        if self.hitboard[xy] == True:
            if self.boatboard[xy] == ' ':
                return 'O'
            else:
                return 'X'
        return self.boatboard[xy]

    def gethitboard(self, mode : str = 'full'):
        if mode == 'full':
            return {xy : v for xy, v in self.hitboard.items()}
        elif mode == 'hit':
            return {xy : v for xy, v in self.hitboard.items() if v == True}
        elif mode == 'nothit':
            return {xy : v for xy, v in self.hitboard.items() if v == False}

    def checkboat(self, boat : str):
        for pos in self.boats[boat].positions:
            if self.hitboard[pos] == False:
                return False
        return True

    def checkwin(self):
        for boat in self.boats.keys():
            if self.checkboat(boat) == False:
                return False
        return True

    def drawboard(self, mode : str = 'full'):
        seps = '\n' + '-' + '+'.join('-'*11) + '\n'
        msg = '  |' + '|'.join(letters[:10]) + seps
        if mode == 'full':
            msg += seps.join(f'{y+1:2}' + '|' + '|'.join('X' if self.checkspace((x,y)) == True else self.checkspace((x,y)) for x in range(10)) for y in range(10))
        elif mode == 'boats':
            msg += seps.join(f'{y+1:2}' + '|' + '|'.join(self.boatboard[x,y] for x in range(10)) for y in range(10))
        elif mode == 'hits':
            msg += seps.join(f'{y+1:2}' + '|' + '|'.join('X' if self.hitboard[x,y] else ' ' for x in range(10)) for y in range(10))
        return msg
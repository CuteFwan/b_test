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
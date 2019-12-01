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
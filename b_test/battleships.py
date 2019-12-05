from .utils import letters
boats = {
        'Carrier' : 5,
        'Battleship' : 4,
        'Destroyer' : 3,
        'Submarine' : 3,
        'Patrol Boat' : 2,
        }
        

class Boat:
    """
    Represents a Boat on a board.

    Can be placed manually on a game board upon creation,
    but should be created and placed inside the game board.

    Attributes
    ----------
    name: :class:`str`
        The name of the boat. Should match up with one of the names of the
        boats on a standard battleship game with exact casing.
    board: :class:`dict`
        The board on which the boat is to exist on.
        A dict of strings keyed to a 2 tuple based on which ship is at which coordinate.
        Could be a space to indicate no ship.
        For example:
        {(0,0) : 'C', (1,0) : ' ', ... , (8,9) : 'D', (9,9) : 'D'}
    start: Optional[:class:`tuple`]
        The top left most coordinate the boat exists at.
    rotated: Optional[:class:`bool`]
        A boolean representing whether or not the boat is horizontal or vertical.
        Horizontal being False and Vertical being True.
    """
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

    def canplaceboat(self, xy, rotated):
        """
        Returns positions based on whether or not the boat can be placed at a certain position.

        Parameters
        ----------
        xy: :class:`tuple`
            The top left most coordinate of the boat.
        rotated: :class:`bool`
            A boolean representing whether or not the boat is to be horizontal or vertical.
            Horizontal being False and Vertical being True.

        Returns
        -------
        Union[List[:class:`tuple`], :class:`None`]
            A list of tuples representing the coordinates the boat can be placed at without obstruction
            or None if the boat cannot be placed at the given coordinate and rotation.
        """
        temppos = list(xy)
        positions = []
        for i in range(self.size):
            if 0 <= temppos[0] < 10 and 0 <= temppos[1] < 10 and self.board[tuple(temppos)] == ' ':
                positions.append(tuple(temppos))
                temppos[rotated] += 1
            else:
                return None
        self.start = xy
        self.rotated = rotated
        self.positions = positions
        return positions

class Battleship:
    """
    Represents a game of Battleships.
    """
    def __init__(self):
        self.hitboard = {(x, y) : False for x in range(10) for y in range(10)}
        self.boatboard = {(x, y) : ' ' for x in range(10) for y in range(10)}
        self.boats = {b : Boat(b, self.boatboard) for b in boats.keys()}

    def placeboat(self, boatname, xy, rotated = False):
        """
        Attempts to place a given boat at a certain position xy on the game's boatboard.

        Parameters
        ----------
        boatname: :class:`str`
            The name of the boat. Should match up with one of the names of the
            boats on a standard battleship game with exact casing.
        xy: :class:`tuple`
            The top left most coordinate of the boat.
        rotated: Optional[:class:`bool`]
            A boolean representing whether or not the boat is to be horizontal or vertical.
            Horizontal being False and Vertical being True.

        Returns
        -------
        Union[List[:class:`tuple`], :class:`None`]
            A list of tuples representing the coordinates the boat has been placed at without obstruction
            or None if the boat cannot be placed at the given coordinate and rotation.
        """

        positions = self.boats[boatname].canplaceboat(xy, rotated)

        if not positions:
            return None

        for p in positions:
            self.boatboard[p] = boatname[0]
        return positions

    def attack(self, xy):
        """
        Attempts to attack the board given a certain position xy.

        Parameters
        ----------
        xy: :class:`tuple`
            The position of the attack.

        Returns
        -------
        Union[:class:`str`, :class:`bool`]
            Either a single character representing no boat, which boat is attacked,
            or False if the position had already been attacked.

            False: A position that had already been previously hit
            ' ': The attack had not hit a boat
            'C': A part of a Carrier
            'B': A part of a Battleship
            'D': A part of a Destroyer
            'S': A part of a Submarine
            'P': A part of a Patrol Boat
        """
        if self.hitboard[xy] == True:
            #Attacking spot already hit
            return False
        spot = self.checkspace(xy)
        self.hitboard[xy] = True
        return spot

    def checkspace(self, xy):
        """
        Returns an X, O, space, or the first character of the name of a boat given a position xy.

        Parameters
        ----------
        xy: :class:`tuple`
            The position to check.

        Returns
        -------
        :class:`str`
            A single character representing what exists on the game board at a certain position.

            'X': A missed shot
            'O': A shot that hit a boat
            'C': A part of an unhit Carrier
            'B': A part of an unhit Battleship
            'D': A part of an unhit Destroyer
            'S': A part of an unhit Submarine
            'P': A part of an unhit Patrol Boat
        """
        if self.hitboard[xy] == True:
            if self.boatboard[xy] == ' ':
                return 'O'
            else:
                return 'X'
        return self.boatboard[xy]

    def gethitboard(self, mode = 'full'):
        """
        Returns a dict of shots fired upon this game's board.

        Parameters
        ----------
        mode: Optional[:class:`str`]
            Whether to return the entire board, only the spots hit, or the spots not hot yet.

            'full': The entire board regardless of an attack or not
            'hit': Only the positions where attacks have landed
            'nothit': Only the positions where not attacks have landed

        Returns
        -------
        :class:`dict`
            A dict of bools keyed to a 2 tuple representing whether or not a certain position had been attacked or not.
            For example:
            {(0,0) : False, (1,0) : True, ... , (8,9) : False, (9,9) : False}
        """
        if mode == 'full':
            return {xy : v for xy, v in self.hitboard.items()}
        elif mode == 'hit':
            return {xy : v for xy, v in self.hitboard.items() if v == True}
        elif mode == 'nothit':
            return {xy : v for xy, v in self.hitboard.items() if v == False}

    def checkboat(self, boat):
        """
        Returns whether or not a certain boat had been sunk.

        Parameters
        ----------
        boatname: :class:`str`
            The name of the boat. Should match up with one of the names of the
            boats on a standard battleship game with exact casing.

        Returns
        -------
        :class:`bool`
            True or False depending on whether or not the boat had been fully sunk.
        """
        for pos in self.boats[boat].positions:
            if self.hitboard[pos] == False:
                return False
        return True

    def checkwin(self):
        """
        Returns whether or not all boats have been sunk.

        Parameters
        ----------

        Returns
        -------
        :class:`bool`
            True or False depending on whether or not all boats have been sunk.
        """
        for boat in self.boats.keys():
            if self.checkboat(boat) == False:
                return False
        return True

    def drawboard(self, mode = 'full'):
        """
        Returns a string representation of the entire game board.

        Parameters
        ----------
        mode: Optional[:class:`str`]
            Whether to return the entire board, only boats, or only hits.

            'full': The entire board with boats and hits.
            'boats': Only the boats.
            'hits': Only the hits.

        Returns
        -------
        :class:`str`
            String representation of the entire game board.
        """
        seps = '\n' + '-' + '+'.join('-'*11) + '\n'
        msg = '  |' + '|'.join(letters[:10]) + seps
        if mode == 'full':
            msg += seps.join(f'{y+1:2}' + '|' + '|'.join('X' if self.checkspace((x,y)) == True else self.checkspace((x,y)) for x in range(10)) for y in range(10))
        elif mode == 'boats':
            msg += seps.join(f'{y+1:2}' + '|' + '|'.join(self.boatboard[x,y] for x in range(10)) for y in range(10))
        elif mode == 'hits':
            msg += seps.join(f'{y+1:2}' + '|' + '|'.join(self.checkspace((x,y)) if self.hitboard[x,y] else ' ' for x in range(10)) for y in range(10))
        return msg
from b_test import *
import random

def setupgamerandomly(game):
    """
    Randomly places boats on a game's board.
    Keeps trying until all boats fit.

    Need to add a timeout if the board gets into a configuration
    where no more boats can fit, but this isn't necessary for standard
    battleships.

    Parameters
    ----------
    game: :class:`Battleship`
        The game to populate ships upon.
    Returns
    -------
    :class:`Battleship`
        The populated game.
    """
    for boat, size in boats.items():
        coords = None
        while coords is None:
            rotated = bool(random.randint(0,1))
            pos = (random.randint(0, (9 - size) if not rotated else 9), random.randint(0, (9 - size) if rotated else 9))
            #print(f'trying to place {boat} on {pos}')
            coords = game.placeboat(boat, pos, rotated)
    return game
def setupgame(game):
    """
    Manually calls input() to populate a given game's board.

    Parameters
    ----------
    game: :class:`Battleship`
        The game to populate ships upon.
    Returns
    -------
    :class:`Battleship`
        The populated game.
    """
    for boat, size in boats.items():
        coords = None
        while coords is None:
            res = input(f"Where to put {boat}? (A4... etc) ")
            pos = lettertonum(res[0]), int(res[1:]) - 1
            rotated = bool(int(input("Rotated? (0 or 1) ")))
            coords = game.placeboat(boat, pos, rotated)
        print(game.drawboard())
    return game


def main():
    """
    Human vs AI battleships game.
    Human game is set up manually and AI game is set up randomly.
    Could be improved with a better system to select which AI to use.
    """
    mygame = setupgame(Battleship())
    AIgame = setupgamerandomly(Battleship())
    me = manually(mygame)
    AI = history(AIgame)
    
    myturn = True
    while True:
        if myturn:
            myturn = False
            spot = me.nextturn(AI.game)
            print(f"You attack {numtoletter(spot[0][0])}{spot[0][1]+1}{f' and hit opponent {spot[1]}' if spot[1] != ' ' else ''}")
            if AI.game.checkwin():
                print("You win!")
                break
        else:
            spot = AI.nextturn(me.game)
            myturn = True
            print(f"Opponent attacks {numtoletter(spot[0][0])}{spot[0][1]+1}{f' and hit your {spot[1]}' if spot[1] != ' ' else ''}")
            if me.game.checkwin():
                print("You lose!")
                break
    AI.save()

def aigame():
    """
    Purely AI vs AI battleships game.
    """
    AI1game = setupgamerandomly(Battleship())
    AI2game = setupgamerandomly(Battleship())
    AI1 = stats(AI1game)
    AI2 = history(AI2game)
    players = [AI1, AI2]

    turn = False
    while True:
        players[turn].nextturn(players[not turn].game)
        turn = not turn
        if players[not turn].game.checkwin():
            print(f'AI{int(turn)+1} wins')
            break
    print(AI1.game.drawboard())
    print(AI2.game.drawboard())
    AI1.save()
    AI2.save()
        

main()
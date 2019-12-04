from b_test import *
import random

def setupgamerandomly(game):
    for boat, size in boats.items():
        coords = None
        while coords is None:
            rotated = bool(random.randint(0,1))
            pos = (random.randint(0, (9 - size) if not rotated else 9), random.randint(0, (9 - size) if rotated else 9))
            #print(f'trying to place {boat} on {pos}')
            coords = game.placeboat(boat, pos, rotated)
    return game
def setupgame(game):
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
    mygame = setupgame(Battleship())
    AIgame = setupgamerandomly(Battleship())
    AI = history(AIgame)
    
    myturn = True
    while True:
        if myturn:
            print(AI.game.drawboard("hits"))
            print(mygame.drawboard("full"))
            spot = False
            while spot == False:
                res = input("Attack? ")
                pos = lettertonum(res[0]), int(res[1:]) - 1
                spot = AI.game.attack(pos)
                if spot == False:
                    print("Already hit that spot, try again.")
            myturn = False
            print(spot)
            if AI.game.checkwin():
                print("You win!")
                break
        else:
            spot = AI.nextturn(mygame)
            myturn = True
            print(f"Opponent attacks {numtoletter(spot[0][0])}{spot[0][1]+1}{f' and hit your {spot[1]}' if spot[1] != ' ' else ''}")
            if mygame.checkwin():
                print("You lose!")
                break
    AI.save()

def aigame():
    AI1game = setupgamerandomly(Battleship())
    AI2game = setupgamerandomly(Battleship())
    AI1 = stats(AI1game)
    AI2 = history(AI2game)

    turn = True
    while True:
        if turn:
            AI1.nextturn(AI2.game)
            turn = False
            if AI2.game.checkwin():
                print(f'AI1 wins')
                break
        else:
            AI2.nextturn(AI1.game)
            turn = True
            if AI1.game.checkwin():
                print(f'AI2 wins')
                break
    print(AI1.game.drawboard())
    print(AI2.game.drawboard())
    AI2.save()
        

aigame()


with open('b_test/history.json', 'r') as f:
    data = json.load(f)
    print('\n'.join(' '.join(f"{j:3}"for j in data[i: i+10]) for i in range(0,100,10)))
        



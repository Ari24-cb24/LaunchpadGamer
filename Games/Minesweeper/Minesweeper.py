from Controller import Controller
import random
import time

c = Controller()

class Colors:
    notRevealed = 70
    flagged = 108
    revealed = 0
    bomb = 8

    numbers = {
        "1": 45,
        "2": 86,
        "3": 5,
        "4": 51,
        "5": 7,
        "6": 34,
        "7": 71,
        "8": 70
    }

class Field:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.revealed = False
        self.flagged = False
        self.bee = False
        self.number = 0


gameOver = False
isRunning = False
game_field = []
isFlag = False
firstClick = False
everyBombFound = False
bombs = random.randint(7, 9)
bombs_left = bombs
def start():
    global game_field, isRunning

    isRunning = True
    game_field = [[Field(x, y) for x in range(0, 8)] for y in range(0, 8)]

def calc_neighbors():
    for col in range(8):
        for row in range(8):
            if game_field[col][row].bee:
                continue

            total = 0

            for colOff in range(-1, 2):
                for rowOff in range(-1, 2):
                    i = col + colOff
                    j = row + rowOff

                    if 0 <= i < 8 and 0 <= j < 8 and game_field[i][j].bee:
                        total += 1

            game_field[col][row].number = total

def restart():
    global isRunning, gameOver, firstClick, everyBombFound, isFlag, bombs, bombs_left
    isRunning = False
    isFlag = False
    everyBombFound = False
    firstClick = False
    gameOver = False
    bombs = random.randint(7, 9)
    bombs_left = bombs
    start()
    draw()

def toggle_flag():
    global isFlag
    isFlag = not isFlag

def floodfill(x, y):
    if 0 <= x < 8:
        if 0 <= y < 8:
            f = game_field[x][y]

            if not f.flagged:
                if f.number == 0 and not f.bee and not f.revealed:
                    f.revealed = True

                    # TODO: Ecken auch überprüfen
                    # TODO: Check, if alle Felder, die keine Bomben sind, geklickt wurden

                    floodfill(x, y+1)
                    floodfill(x, y-1)
                    floodfill(x+1, y)
                    floodfill(x-1, y)
                else:
                    f.revealed = True

def finishAnimation():
    for y in range(8):
        for x in range(0, 8) if y % 2 == 0 else range(7, -1, -1):
            c.ledOn(x, y, 3 if not game_field[x][y].bee else 5, pulse=not game_field[x][y].bee)
            time.sleep(.1)

def check_bomb_marked():
    global everyBombFound
    sumBobms = 0
    sumMarked = 0

    for x in range(8):
        for y in range(8):
            f = game_field[x][y]

            if f.flagged:
                sumMarked += 1

            if f.bee:
                sumBobms += 1

    if sumMarked == sumBobms:
        finishAnimation()
        everyBombFound = True

def draw(go=False):
    for x in range(8):
        for y in range(8):
            f = game_field[x][y]

            if not f.revealed:
                if f.flagged:
                    c.ledOn(x, y, Colors.flagged, pulse=go)
                else:
                    c.ledOn(x, y, Colors.notRevealed, pulse=go)
            else:
                if f.bee:
                    c.ledOn(x, y, Colors.bomb)
                else:
                    if f.number == 0:
                        c.ledOn(x, y, Colors.revealed, pulse=go)
                    else:
                        c.ledOn(x, y, Colors.numbers[str(f.number)], pulse=go)

    c.ledOn(8, 1, 6 if not isFlag else 75, pulse=go)  # flag
    c.ledOn(8, 0, 12, pulse=go)  # restart

    if bombs_left < 9:
        c.ledOn(8, 3, Colors.numbers[str(bombs_left)])
        c.ledOn(8, 4, 0)
    else:
        c.ledOn(8, 3, Colors.numbers["8"])
        c.ledOn(8, 4, Colors.numbers[str(bombs_left - 8)])

    c.ledOn(8, 2, 0)
    c.ledOn(8, 5, 0)

@c.event
def on_settings_button_press(index):
    if index == 1:
        restart()

    if index == 2:
        if not gameOver and not everyBombFound:
            toggle_flag()

    if not gameOver and not everyBombFound:
        draw()

@c.event
def on_profile_enter():
    c.fill(11)

    if isRunning:
        draw()
    else:
        start()
        draw()

@c.event
def on_button_press(x, y):
    global gameOver, firstClick, bombs_left
    f = game_field[x][y]

    if not everyBombFound:
        if not firstClick:
            firstClick = True

            options = []

            for x_ in range(8):
                for y_ in range(8):
                    if x_ != x and y_ != y:
                        options.append([x_, y_])

            for n in range(bombs):
                index = random.randint(0, len(options)-1)
                choice = options[index]
                i1, j1 = choice

                del options[index]
                game_field[i1][j1].bee = True

            calc_neighbors()

        if not gameOver:
            if not isFlag:
                if not f.flagged:
                    if f.number != 0 or f.bee:
                        f.revealed = True

                    floodfill(x, y)
            else:
                if bombs_left > 0:
                    if not f.flagged:
                        bombs_left -= 1
                    else:
                        bombs_left += 1

                    f.flagged = not f.flagged

            if not isFlag:
                draw(f.bee)
            else:
                draw(False)

        if f.bee and not isFlag:
            for x in range(8):
                for y in range(8):
                    if game_field[x][y].bee:
                        c.ledOn(x, y, Colors.bomb)

            gameOver = True

        check_bomb_marked()


if __name__ == '__main__':
    c.start()

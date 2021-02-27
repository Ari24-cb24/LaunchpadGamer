from Controller import Controller
import threading
import time
import random

c = Controller()

anima = False
running = False
end = False
pause = False
snake = []
head = [3, 4]
direction_queue = []
direction = [-1, 0]


movements = [
    [(3, 0), (4, 0), (3, 1), (4, 1), (3, 2), (4, 2), (2, 0), (2, 1), (5, 0), (5, 1)],
    [(0, 3), (0, 4), (1, 3), (1, 4), (2, 3), (2, 4), (0, 2), (1, 2), (0, 5), (1, 5)],
    [(3, 5), (4, 5), (3, 6), (4, 6), (3, 7), (4, 7), (5, 6), (2, 6), (5, 7), (2, 7)],
    [(5, 3), (5, 4), (6, 3), (6, 4), (7, 3), (7, 4), (6, 2), (7, 2), (6, 5), (7, 5)]
]

food = []


def draw():
    if end or pause:
        return

    for x in range(8):
        for y in range(8):
            c.ledOn(x, y, 0)

            for m in movements:
                if (x, y) in m:
                    c.ledOn(x, y, 1)

            if [x, y] in snake:
                c.ledOn(x, y, 80)
            elif [x, y] == head:
                c.ledOn(x, y, 9)
            elif [x, y] == food:
                c.ledOn(x, y, 87)


def draw_bp():
    for x in range(8):
        for y in range(8):
            if [x, y] in snake:
                c.ledOn(x, y, 80)
            elif [x, y] == head:
                c.ledOn(x, y, 9)
            elif [x, y] == food:
                c.ledOn(x, y, 87)

def enda():
    global end, running, anima
    end = True
    running = False
    anima = True

    for y in range(8):
        for x in range(8) if y % 2 == 0 else range(7, -1, -1):
            c.ledOn(x, y, 72)
            time.sleep(.1)

    anima = False

def update_snake():
    global snake, food, direction_queue, direction

    sleep = 1

    while not end:
        if pause:
            continue

        if head == food:
            food = [random.randint(0, 7), random.randint(0, 7)]
            snake.insert(0, [0, 0])

            sleep -= 0.03

        if len(direction_queue) > 0:
            direction = direction_queue.copy()
            direction_queue = []

        for i in range(len(snake)):
            if i < len(snake) - 1:
                snake[i] = snake[i + 1].copy()
            else:
                snake[i] = head.copy()

        head[0] += direction[0]
        head[1] += direction[1]

        if head[0] < 0 or head[0] > 7:
            enda()

        if head[1] < 0 or head[1] > 7:
            enda()

        for tile in snake:
            if head == tile:
                enda()
                break

        draw()
        time.sleep(sleep)


@c.event
def on_profile_enter():
    global pause

    if running:
        pause = False


t = threading.Thread(target=update_snake)

@c.event
def on_button_press(x, y):
    global running, snake, direction, t, food, direction_queue, end, head, pause

    if anima:
        return

    if not running:
        running = True
        c.fill(0)

        snake = []
        end = False
        pause = False
        direction = [-1, 0]
        head = [3, 4]

        food = [random.randint(0, 7), random.randint(0, 7)]

        t = threading.Thread(target=update_snake)
        t.start()

    else:
        if pause: return

        for block in movements:
            if (x, y) in block:
                index = movements.index(block)

                for x_, y_ in block:
                    c.ledOn(x_, y_, 126)

                draw_bp()

                if index == 0 and direction != [0, 1]:
                    # up
                    direction_queue = [0, -1]
                elif index == 1 and direction != [1, 0]:
                    # left
                    direction_queue = [-1, 0]
                elif index == 2 and direction != [0, -1]:
                    # down
                    direction_queue = [0, 1]
                elif index == 3 and direction != [-1, 0]:
                    # right
                    direction_queue = [1, 0]

                break

@c.event
def on_button_release(x, y):
    if anima:
        return

    if running and not end and not pause:
        for block in movements:
            if (x, y) in block:
                for x_, y_ in block:
                    c.ledOn(x_, y_, 1)

        draw_bp()

@c.event
def on_profile_exit():
    global pause

    if running:
        pause = True


@c.event
def on_exit():
    global end
    end = True

    time.sleep(1)

    if running:
        t.join()


if __name__ == '__main__':
    c.run()

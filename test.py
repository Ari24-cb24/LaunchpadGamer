from Controller import Controller
c = Controller()

fields = [
    [],
    [],
    [],
    []
]

index = 0

@c.event
def on_profile_enter():
    c.fill(0)

@c.event
def on_button_press(x, y):
    global fields, index

    if x == 7 and y == 7:
        index += 1

    else:
        fields[index].append((x, y))
        print(fields)

        c.ledOn(x, y, 3)


c.run()
import launchpad_py
from pynput.keyboard import Controller as KBController, Key as KBKey
from pynput.mouse import Controller as MController, Button as MButton
import time
import threading
from playsound import playsound

class Player:
    def play(self, wav_file):
        t = threading.Thread(target=lambda: playsound(wav_file))
        t.start()

class Controller(threading.Thread):
    def __init__(self):
        super().__init__()
        self.keyboard = KBController()
        self.mouse = MController()
        self.lp = launchpad_py.LaunchpadMk2()
        self.lp.Open(0)

        self.current_profile = None

        self.profiles = {}
        self.buttons = {}

        self.player = Player()

        self.events = {
            "on_button_press": None,
            "on_button_release": None,
            "on_settings_button_press": None,
            "on_exit": None,
            "on_profile_enter": None,
            "on_profile_exit": None
        }

    def play_sound(self, file):
        self.player.play(file)

    def on_button_press(self, x, y):
        if self.events["on_button_press"]:
            self.events["on_button_press"](x, y)

    def on_button_release(self, x, y):
        if self.events["on_button_release"]:
            self.events["on_button_release"](x, y)

    def on_settings_button_press(self, index):
        if self.events["on_settings_button_press"]:
            self.events["on_settings_button_press"](index)

    def on_exit(self):
        if self.events["on_exit"]:
            self.events["on_exit"]()

    def on_profile_enter(self):
        if self.events["on_profile_enter"]:
            self.events["on_profile_enter"]()

    def on_profile_exit(self):
        if self.events["on_profile_exit"]:
            self.events["on_profile_exit"]()

    def __register_setup(self):
        rl = self.registerProfile("rocketLeague")

        # TODO: Add volume config
        # registerButton(profile, name, launchpadPos, command (key, MBButton, up, down, left, right), keyMode (0 == mouseButton, 1 == key, 2 == mouseMotion), color, colorFeedback
        self.registerButton(rl, "forward", (2, 3), "w", 1, 67, 9)
        self.registerButton(rl, "left", (1, 4), "a", 1, 67, 9)
        self.registerButton(rl, "back", (2, 4), "s", 1, 67, 9)
        self.registerButton(rl, "right", (3, 4), "d", 1, 67, 9)

        self.registerButton(rl, "Boost", (6, 7), MButton.left, 0, 72, 126)
        self.registerButton(rl, "Jump", (4, 6), MButton.right, 0, 16, 7)
        self.registerButton(rl, "Airroll Left", (1, 3), "q", 1, 40, 10)
        self.registerButton(rl, "Airroll Right", (3, 3), "e", 1, 40, 10)

        self.registerButton(rl, "CameraSwitch", (4, 4), "y", 1, 16, 7)
        self.registerButton(rl, "Drift", (5, 4), KBKey.ctrl_l, 1, 9, 5)

        aus = self.registerProfile("AmongUs")
        self.registerButton(aus, "Bottm Right Button", (7, 7), "e", 1, 23, 61)
        self.registerButton(aus, "Exit", (0, 0), KBKey.esc, 1, 71, 61)
        self.registerButton(aus, "Map", (0, 2), KBKey.tab, 1, 18, 61)
        self.registerButton(aus, "Kill", (6, 7), "q", 1, 11, 61)
        self.registerButton(aus, "Report", (7, 4), "r", 1, 110, 61)

        self.registerButton(aus, "forward", (2, 3), "w", 1, 67, 9)
        self.registerButton(aus, "left", (1, 4), "a", 1, 67, 9)
        self.registerButton(aus, "back", (2, 4), "s", 1, 67, 9)
        self.registerButton(aus, "right", (3, 4), "d", 1, 67, 9)

        self.registerButton(aus, "MouseUp", (5, 1), "up", 2, 47, 62)
        self.registerButton(aus, "MouseDown", (5, 3), "down", 2, 47, 62)
        self.registerButton(aus, "MouseLeft", (4, 2), "left", 2, 47, 62)
        self.registerButton(aus, "MouseRight", (6, 2), "right", 2, 47, 62)

        self.registerButton(aus, "LeftMouseButton", (4, 1), MButton.left, 0, 4, 17)
        self.registerButton(aus, "RightMouseButton", (6, 1), MButton.right, 0, 4, 17)

        osu = self.registerProfile("osu!")
        self.registerButton(osu, "Y", (4, 1), "y", 1, 67, 9)
        self.registerButton(osu, "X", (4, 2), "x", 1, 67, 9)
        self.registerButton(osu, "Particles", (4, 3), "c", 1, 4, 17)

        tetris = self.registerProfile("tetris")  # https://tetr.io/
        self.registerButton(tetris, "Left", (1, 6), KBKey.left, 1, 67, 9)
        self.registerButton(tetris, "Right", (3, 6), KBKey.right, 1, 67, 9)
        self.registerButton(tetris, "Rotate", (2, 5), KBKey.up, 1, 76, 9)
        self.registerButton(tetris, "Fall", (2, 6), KBKey.down, 1, 50, 9)
        self.registerButton(tetris, "Hold", (1, 4), "c", 1, 50, 9)

        self.registerProfile("custom", color=66)

    def event(self, func):
        if self.events.__contains__(func.__name__):
            self.events[func.__name__] = func

    def change_profile(self, pos):
        last = self.current_profile
        if self.profiles.__contains__(pos):
            self.current_profile = self.profiles[pos][0]

            if last != self.current_profile:
                if self.current_profile != "custom":
                    self.lp.LedAllOn()
                else:
                    self.lp.LedAllOn()
                
                if last == "custom":
                    if self.profiles[pos][0] != last:
                        self.on_profile_exit()

                if self.profiles[pos][0] == "custom":
                    if self.profiles[pos][0] != last:
                        self.on_profile_enter()

                self.__setup_leds()

    def registerProfile(self, profileName, color=9, feedbackColor=5):
        x = len(self.profiles)
        y = 0

        self.profiles[(x, y)] = [profileName, color, feedbackColor]
        self.buttons[profileName] = {}

        return profileName

    def registerButton(self, profile, name, pos, button, isKeyboard, color, feedbackColor):
        # pos: [gotPressed, pressedBeforeState, isRunning, "char", keyMode, normalColor, feedbackColor, name]
        pos = (pos[0], pos[1]+1)
        self.buttons[profile][pos] = [False, False, False, button, isKeyboard, color, feedbackColor, name]

    def isButton(self, pos):
        return self.buttons[self.current_profile].__contains__(pos)

    def getProfile(self, name):
        for p in self.profiles:
            if self.profiles[p][0] == name:
                return p

        return None

    def ledOnByButton(self, btn, feedback):
        cc = self.buttons[self.current_profile][btn][5 if not feedback else 6]
        self.lp.LedCtrlXYByCode(btn[0], btn[1], cc)

    def ledOn(self, x, y, cc, pulse=False):
        y += 1

        if not pulse:
            self.lp.LedCtrlXYByCode(x, y, cc)
        else:
            self.lp.LedCtrlPulseXYByCode(x, y, cc)

        return x, y

    def ledOff(self, x, y):
        y += 1
        self.lp.LedCtrlXYByCode(x, y, 0)
        return x, y

    def fill(self, cc):
        for x in range(8):
            for y in range(8):
                self.ledOn(x, y, cc)

    def __setup_leds(self):
        for profile in self.profiles:
            self.ledOn(profile[0], profile[1]-1, self.profiles[profile][1] if self.profiles[profile][0] != self.current_profile else 52)

        for btn in self.buttons[self.current_profile]:
            self.ledOnByButton(btn, feedback=False)

        self.ledOn(8, 7, 121)

    def __mainloop(self):
        while True:
            buttonData = self.lp.ButtonStateXY()
            if buttonData:
                x, y, pressed = buttonData
                pressed = pressed == 127
                pos = (x, y)

                if y == 0:
                    if pressed:
                        self.change_profile(pos)

                elif self.current_profile == "custom":
                    if x < 8:
                        if pressed:
                            self.on_button_press(x, y-1)
                        else:
                            self.on_button_release(x, y-1)
                    else:
                        if pressed:
                            if y != 8:
                                self.on_settings_button_press(y)
                if pos == (8, 8):
                    self.lp.LedAllOn(0)
                    self.lp.Close()
                    print("Exitting program!")

                    if self.current_profile == "custom":
                        self.on_exit()

                    break

                elif self.isButton(pos):
                    self.buttons[self.current_profile][pos][0] = pressed
                    self.buttons[self.current_profile][pos][2] = pressed

                    if pressed:
                        self.buttons[self.current_profile][pos][1] = True

                    if self.current_profile != "custom":
                        print("Key" + ("press" if pressed else "release") + ": " + self.buttons[self.current_profile][pos][7],
                              end="\n\n" if not pressed else "\n")

            for btn in self.buttons[self.current_profile]:
                if self.buttons[self.current_profile][btn][0]:
                    self.buttons[self.current_profile][btn][0] = False
                    if self.buttons[self.current_profile][btn][4] == 1:
                        self.keyboard.press(self.buttons[self.current_profile][btn][3])
                    elif self.buttons[self.current_profile][btn][4] == 0:
                        self.mouse.press(self.buttons[self.current_profile][btn][3])
                    elif self.buttons[self.current_profile][btn][4] == 2:
                        direction = self.buttons[self.current_profile][btn][3]
                        pos_ = self.mouse.position
                        a = 11

                        if direction == "left":
                            self.mouse.position = (pos_[0] - a, pos_[1])

                        if direction == "right":
                            self.mouse.position = (pos_[0] + a, pos_[1])

                        if direction == "up":
                            self.mouse.position = (pos_[0], pos_[1] - a)

                        if direction == "down":
                            self.mouse.position = (pos_[0], pos_[1] + a)

                    self.ledOnByButton(btn, feedback=True)

                elif self.buttons[self.current_profile][btn][1] and not self.buttons[self.current_profile][btn][2]:
                    self.buttons[self.current_profile][btn][1] = False
                    if self.buttons[self.current_profile][btn][4] == 1:
                        self.keyboard.release(self.buttons[self.current_profile][btn][3])
                    elif self.buttons[self.current_profile][btn][4] == 0:
                        self.mouse.release(self.buttons[self.current_profile][btn][3])
                    elif self.buttons[self.current_profile][btn][4] == 2:
                        pass

                    self.ledOnByButton(btn, feedback=False)

    def intro(self):
        pass

    def run(self):
        self.__register_setup()
        self.lp.LedAllOn(0)
        self.current_profile = "rocketLeague"
        self.intro()

        time.sleep(1)

        self.lp.LedAllOn()
        time.sleep(1)

        self.__setup_leds()
        self.__mainloop()

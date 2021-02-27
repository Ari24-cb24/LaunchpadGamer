from Controller import Controller

class Tetris(Controller):
    running = False

    def on_profile_enter(self):
        pass

    def on_button_press(self, x, y):
        if not self.running:
            self.running = True


    def on_profile_exit(self):
        # pause game
        pass

    def on_exit(self):
        pass


t = Tetris()
t.run()

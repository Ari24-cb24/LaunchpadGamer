# LaunchpadGamer
This is a Python project for playing computer games on the Launchpad MK 2/Playing directly

# How to setup
First of all you have to download Python 3.7
You can download it here: https://www.python.org/

After that you need to install the following packages via pip e.g.
```bash
python3 -m pip install <packagename>
```
  
  
- launchpad_py (I'll explain in a second more details)
- pynput
- playsound (Currently not implemented)

### launchpad_py

Launchpad_py is the library used for controlling the launchpad.
Repo: https://github.com/FMMT666/launchpad.py

You may have to directly download it from the repo.

### Starting everything

So you got your Launchpad MK 2.
Now, plug it in.

And then go into your terminal and run
```bash
python3 Main.py
```

If everything worked fine, you should see on the top circles a pink, some orange and a blue circle.

# Profile pages

So you can see these orange, pink and blue circles.
If you press on one of them, the profile page changes. 
  
  
A profile can be the following:
- A game on the launchpad
- A Controller profile page for a specific game

Blue means Custom page. Developers can use the blue profile page in order to create games.
Oranges is just a normal gameController page.
Pink is the currently selected page.

## Playing specific games on the launchpad itself

So there are some games you can play on the launchpad itself.
Go to the Games directory, choose a game and run it with
```bash
python3 <GameName>.py
```

After that you have to go to the custom profile page in order to play your game.
You may have to press on the field itself to activate the game.

## Using the Launchpad as a controller for specific games

There's also the option to use the Launchpad to play specific games on the computer.
The launchpad simulates Keyboard and Mouse Clicks/presses.

The orange circles are these controller pages.
Just click on one. 

List of currently implemented games (from left to right):
- Rocket League
- Among Us
- osu!
- Tetris (designed for https://tetr.io/)

# Creating own GameControllers

I haven't implemented a Profile Manager yet so you have to edit the code.

1. Open the Controller.py file in a texteditor
2. Go to the __register_setup method (just search for "def __register_setup")
3. Use this preset:

```python
new_game_name_without_spaces = self.registerProfile("gamename_in_lower")
self.registerButton(new_game_name_without_spaces, "button_name", command, keymode, color, colorFeedback)
```

"button_name" is the name for the button. You can give it any name you want, it's mostly used for output in the console
command is the command that the program should do.
- If you want to choose a mouse button, use
  - MButton.left for left mouse button
  - MButton.right for right mouse button
  - MButton.middle for middle mouse button
- If you want to choose some special keyboard keys like control (ctrl) or space then use
  - KBKey.ctrl_l for left ctrl
  - KBKey.ctl_r for right ctrl
  - KBKey.space for space
  - KBKey.up for up arrow
  - ...
- If you want to use Mouse Motion, use
  - "up" for arrow
  - "down" for arrow
  - "left" for arrow
  - "right" for arrow 
- If you want to use a number, char or everything else, just write the keyname out.

keymode is the mode for the key used. You have to specifiy that.
- 0 means its a mouse button
- 1 means its a key
- 2 means its a mouse motion

color and color feedback are used for coloring the button.
Launchpad has a special color pallette so you can't use normal RGB Values.

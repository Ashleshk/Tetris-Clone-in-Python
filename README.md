# Tetris Clone

This is a clone of the classic tetris game.

This game comes with a tkinter GUI and a curses-based command-line
interface. If you are using Windows, the curses interface probably
doesn't work but you can run the GUI version like this:

    cd some\path\to\tetris-clone
    py -m tetris_clone.gui

If you are not using Windows, you probably have curses installed and you
can play the game with a command-line interface too.

    cd some/path/to/tetris-clone
    python3 -m tetris_clone.cli

Or you can use the GUI if you have tkinter installed:

    python3 -m tetris_clone.gui

import platform
import sys

# try to guess the python executable's name
if platform.platform() == 'Windows':
    python = 'py'
else:
    python = 'python3'

sys.stderr.write("""\
Usage:
  {0} -m tetris_clone.gui   # run the game with a tkinter GUI
  {0} -m tetris_clone.cli   # run the game with a curses interface
""".format(python))
sys.exit(2)

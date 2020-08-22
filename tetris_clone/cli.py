import atexit
import curses
import functools
import sys
import time
import traceback

from tetris_clone import core


COLORS = {
    'I': curses.COLOR_RED,
    'O': curses.COLOR_BLUE,
    'T': curses.COLOR_YELLOW,
    'L': curses.COLOR_MAGENTA,
    'J': curses.COLOR_WHITE,
    'S': curses.COLOR_GREEN,
    'Z': curses.COLOR_CYAN,
}



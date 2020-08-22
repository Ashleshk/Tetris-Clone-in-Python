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


class CursesUI:
    
    def __init__(self, window, game):
        self.window = window
        self.window.nodelay(1)
        self.game = game
        self._required_width = core.WIDTH * 2 + 2
        self._required_height = core.HEIGHT + 2
        self.update_size()

    def update_size(self):
        self.screenheight, self.screenwidth = self.window.getmaxyx()

    def draw(self):
        self.window.clear()

        x_offset = (self.screenwidth - core.WIDTH*2) // 2
        y_offset = (self.screenheight - core.HEIGHT) // 2

        # 1 is the border line
        if x_offset < 1 or y_offset < 1:
            sys.exit("Your terminal is too small :(")

        line = '-' * self._required_width
        self.window.addstr(y_offset-1, x_offset-1, line)
        self.window.addstr(y_offset + core.HEIGHT, x_offset-1, line)

        for y in range(core.HEIGHT):
            curses_y = core.HEIGHT - y + y_offset - 1
            self.window.addstr(curses_y, x_offset-1, '|')
            self.window.addstr(curses_y, x_offset + core.WIDTH*2, '|')

            for x in range(core.WIDTH):
                shape = self.game.shape_at(x, y)
                if shape is None:
                    continue

                curses_x = x * 2 + x_offset
                self.window.addstr(curses_y, curses_x, '  ',
                                   curses.color_pair(COLORS[shape]))

        self.window.addstr(
            0, 0, "Level %d, score %d" % (self.game.level, self.game.score),
            curses.color_pair(curses.COLOR_BLACK))

        self.window.refresh()

    
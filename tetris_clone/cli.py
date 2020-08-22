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

    def _handle_key(self, key):
        if key in list(b'Qq'):     # list() is needed because 256 in b''
            sys.exit("Goodbye!")
        if key in list(b'AaJj') + [curses.KEY_LEFT]:
            self.game.moving_block.move_left()
        elif key in list(b'DdLl') + [curses.KEY_RIGHT]:
            self.game.moving_block.move_right()
        elif key in list(b'Kk') + [curses.KEY_ENTER, curses.KEY_UP]:
            self.game.moving_block.rotate()
        elif key in [ord(' '), curses.KEY_DOWN]:
            self.game.moving_block.move_down_all_the_way()
        elif key == curses.KEY_RESIZE:
            self.update_size()
        else:
            return
        self.draw()

    def mainloop(self):
        last_do_something_time = time.time()

        while True:
            key = self.window.getch()
            if key != curses.ERR:
                self._handle_key(key)

            if time.time() - last_do_something_time > self.game.delay / 1000:
                last_do_something_time = time.time()
                self.game.do_something()
                self.draw()
                if self.game.game_over():
                    # this goes to stderr and not stdout, we can't print
                    # here but sys.exit prints later (see comments in
                    # simple_wrapper). this is simpler than using atexit
                    sys.exit("Game Over :(\n"
                             "You ended up on level %d with score %d."
                             % (self.game.level, self.game.score))

            time.sleep(0.01)


def main(stdscr):
    # this reuses COLOR_ constants as color pair numbers, it works
    # and makes the code a bit simpler
    for color_number in COLORS.values():
        curses.init_pair(color_number, curses.COLOR_RED, color_number)

    game = core.Game()
    ui = CursesUI(stdscr, game)
    ui.mainloop()


def simple_wrapper(function):
    """Like curses.wrapper(), but I know how to use this."""
    stdscr = None

    try:
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        stdscr.keypad(1)
        curses.start_color()
        function(stdscr)

    except KeyboardInterrupt:
        # this and other sys.exit messages will be printed after the
        # finally thing below runs
        sys.exit("Goodbye!")

    finally:
        if stdscr is not None:
            curses.nocbreak()
            curses.echo()
            curses.curs_set(1)
            curses.endwin()


if __name__ == '__main__':
    simple_wrapper(main)

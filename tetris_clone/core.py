from functools import partialmethod    # requires Python 3.4 or newer
import itertools
import random

WIDTH = 10
HEIGHT = 20


# the shapes are lists of (x, y) coordinates where (0, 0) is the point
# that the shape rotates around and top center of the game when the
# shape is added to it
# y is like in math, so more y means higher
SHAPES = {
    'I': [(0, 2), (0, 1), (0, 0), (0, -1)],
    'O': [(0, 0), (0, 1), (-1, 0), (-1, 1)],
    'T': [(-1, 0), (0, 0), (1, 0), (0, -1)],
    'L': [(0, 1), (0, 0), (0, -1), (1, -1)],
    'J': [(0, 1), (0, 0), (0, -1), (-1, -1)],
    'S': [(1, 1), (0, 1), (0, 0), (-1, 0)],
    'Z': [(-1, 1), (0, 1), (0, 0), (1, 0)],
}


class Block:
    """The block that is currently moving down the game."""

    def __init__(self, game, shape_letter):
        self._game = game
        self.shape_letter = shape_letter
        self.shape = SHAPES[shape_letter].copy()
        self.x = WIDTH // 2
        self.y = HEIGHT

    # for debugging
    def __repr__(self):
        coords = (self.x, self.y)
        return '<%s-shaped %s at %r>' % (
            self.shape_letter, type(self).__name__, coords)

    def get_coords(self):
        for shapex, shapey in self.shape:
            yield (self.x + shapex, self.y + shapey)

    def _bumps(self, x, y):
        return (x not in range(WIDTH) or y < 0
                or (x, y) in self._game.frozen_squares)

    def _move(self, deltax, deltay):
        for x, y in self.get_coords():
            if self._bumps(x + deltax, y + deltay):
                return False

        self.x += deltax
        self.y += deltay
        return True

    move_left = partialmethod(_move, -1, 0)
    move_right = partialmethod(_move, +1, 0)
    move_down = partialmethod(_move, 0, -1)

    def move_down_all_the_way(self):
        while self.move_down():
            pass

    def rotate(self):
        new_shape = []
        for old_x, old_y in self.shape:
            x, y = -old_y, old_x
            if self._bumps(self.x + x, self.y + y):
                return False
            new_shape.append((x, y))

        self.shape[:] = new_shape

        return True


class NonRotatingBlock(Block):

    def rotate(self):
        return False


class TwoRotationsBlock(Block):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._rotations = None

    def rotate(self):
        if self._rotations is None:
            # running this for the first time
            before = self.shape.copy()
            if not super().rotate():
                # bumping into a wall, maybe we can do something next time
                return False
            after = self.shape.copy()
            self._rotations = itertools.cycle([before, after])
            return True

        else:
            new_shape = next(self._rotations)
            for x, y in new_shape:
                if self._bumps(self.x + x, self.y + y):
                    return False
            self.shape = new_shape
            return True


class Game:

    def __init__(self):
        self.moving_block = None
        self.frozen_squares = {}   # {(x, y): block_shape}
        self.score = 0
        self.add_block()

    @property
    def level(self):
        # levels start at 1
        return self.score // 30 + 1

    @property
    def delay(self):
        """The waiting time between do_something() calls as milliseconds."""
        return 300 - (30 * self.level)

    def add_block(self):
        letter = random.choice(list(SHAPES))
        if letter == 'O':
            self.moving_block = NonRotatingBlock(self, letter)
        elif letter in {'I', 'S', 'Z'}:
            self.moving_block = TwoRotationsBlock(self, letter)
        else:
            self.moving_block = Block(self, letter)

    def shape_at(self, x, y):
        try:
            return self.frozen_squares[(x, y)]
        except KeyError:
            if (x, y) in self.moving_block.get_coords():
                return self.moving_block.shape_letter
            return None

    def freeze_moving_block(self):
        for x, y in self.moving_block.get_coords():
            self.frozen_squares[(x, y)] = self.moving_block.shape_letter

    def delete_full_lines(self):
        # this is much easier with a nested list
        lines = []
        for y in range(HEIGHT):
            line = [self.frozen_squares.pop((x, y), None)
                    for x in range(WIDTH)]
            if None in line:
                # it's not full, we can keep it
                lines.append(line)

        for y, line in enumerate(lines):
            for x, value in enumerate(line):
                if value is not None:
                    self.frozen_squares[(x, y)] = value

    def do_something(self):
        if self.moving_block.move_down():
            return

        self.freeze_moving_block()
        self.add_block()
        self.delete_full_lines()
        self.score += 1

    def game_over(self):
        """Return True if the game is over."""
        for x in range(WIDTH):
            if (x, HEIGHT) in self.frozen_squares:
                return True
        return False


if __name__ == '__main__':
    # simple demo
    game = Game()

    while True:
        for y in range(HEIGHT-1, -1, -1):
            row = []
            for x in range(WIDTH):
                row.append(game.shape_at(x, y) or ' ')
            print('|', ' '.join(row), '|')

        input("Press Enter to continue...")
        game.do_something()
        if game.game_over():
            print("game over :(")
            break

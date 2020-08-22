import tkinter as tk

from tetris_clone import core


COLORS = {
    'I': 'red',
    'O': 'blue',
    'T': 'yellow',
    'L': 'magenta',
    'J': 'white',
    'S': 'green',
    'Z': 'cyan',
}


class TkinterGUI(tk.Frame):

    def __init__(self, parent, game, scale=20, *, fg='white', bg='black'):
        super().__init__(parent, bg=bg)
        self.game = game

        # the canvas is in a separate frame because setting the
        # borderwidth of the canvas doesn't offset the items in the
        # canvas correctly :(
        canvasframe = tk.Frame(self, bg=bg, borderwidth=5, relief='ridge')
        canvasframe.pack()
        self.canvas = tk.Canvas(
            canvasframe, width=core.WIDTH * scale,
            height=core.HEIGHT * scale, bg=bg)
        self.canvas.pack()

        self.statusbar = tk.Label(self, relief='sunken', fg=fg, bg=bg)
        self.statusbar.pack(side='bottom', fill='x')

        for key in ['A', 'a', 'S', 's', 'D', 'd', 'F', 'f',
                    'Left', 'Right', 'Up', 'Down', 'Return', 'space']:
            parent.bind('<' + key + '>', self.move, add=True)

        self._canvas_content = {}
        for x in range(core.WIDTH):
            for y in range(core.HEIGHT):
                left = x * scale
                top = (core.HEIGHT - y - 1) * scale
                self._canvas_content[(x, y)] = self.canvas.create_rectangle(
                    left, top, left + scale, top + scale,
                    outline=self.canvas['bg'], fill=self.canvas['bg'])

        self._sleep_time = 300
        self._on_timeout()

    def refresh(self):
        for (x, y), item_id in self._canvas_content.items():
            shape = self.game.shape_at(x, y)
            if shape is None:
                color = self.canvas['bg']
            else:
                color = COLORS[shape]
            self.canvas.itemconfig(item_id, fill=color)
        self.statusbar['text'] = "Score %d, level %d" % (
            self.game.score, self.game.level)

    def move(self, event):
        if event.keysym in {'A', 'a', 'Left'}:
            self.game.moving_block.move_left()
        if event.keysym in {'D', 'd', 'Right'}:
            self.game.moving_block.move_right()
        if event.keysym in {'Return', 'Up'}:
            self.game.moving_block.rotate()
        if event.keysym in {'space', 'Down'}:
            self.game.moving_block.move_down_all_the_way()
        self.refresh()

    def _invert_color(self, color):
        r, g, b = (0xff - (value >> 8)
                   for value in self.canvas.winfo_rgb(color))
        return '#%02x%02x%02x' % (r, g, b)

    def _on_timeout(self):
        self.game.do_something()
        self.refresh()

        if self.game.game_over():
            centerx = int(self.canvas['width']) // 2
            centery = int(self.canvas['height']) // 3
            self.canvas.create_text(
                centerx, centery, anchor='center',
                text="Game Over :(", font="TkDefaultFont 16 bold",
                fill=self._invert_color(self.canvas['bg']))
        else:
            self.canvas.after(self.game.delay, self._on_timeout)


if __name__ == '__main__':
    root = tk.Tk()

    game = core.Game()
    gui = TkinterGUI(root, game, fg='white', bg='black')
    gui.pack(fill='both', expand=True)

    root.update()
    root.minsize(gui.winfo_reqwidth(), gui.winfo_reqheight())
    root.title("Tetris Clone")
    root.mainloop()

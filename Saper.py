"""Minesweeper game implemented via object oriented programming (OOP)."""
# %%
import tkinter as tk
from PIL import Image, ImageTk

ICON = {}  # minesweeper icon dictionary
ICON['c'] = Image.open("Minesweeper icons\\facingDown.png")
ICON['f'] = Image.open("Minesweeper icons\\flagged.png")
ICON['m'] = Image.open("Minesweeper icons\\bomb.png")
for i in range(9):
    ICON[str(i)] = Image.open("Minesweeper icons\\" + str(i) + ".png")

# %%


class MineField:
    """Contains playing field data.

    Args:
        num_of_mines (int, optional): Number of mines.
        rows (int, optional): Contains the number of rows.
        columns (int, optional): Contains the number of columns.
        force_empty (list or tuple, optional): Cells required to be empty by
            first player selection.
        cov (list of lists, optional): Contains the coordinates of covered
            fields.
        uncov (list of lists, optional): Contains the coordinates of uncovered
            fields.

    Attributes:
        num_of_mines (int): Number of mines.
        rows (int): Contains the number of rows.
        columns (int): Contains the number of columns.
        force_empty (list or tuple): Cells required to be empty by first
            player selection.
        cov (list of lists): Contains the coordinates of currently covered
            fields.
        uncov (list of lists): Contains the coordinates of currently uncovered
            fields.

    Raises:
        TypeError: If given values do not match their expected types.

    """

    def __init__(self, num_of_mines=40, rows=10, columns=10,
                 force_empty=None, cov=None, uncov=None):
        self.num_of_mines = num_of_mines
        self.rows = rows
        self.columns = columns
        if force_empty is not None:
            self.force_empty = force_empty
        if cov is not None:
            self.cov = cov
        if uncov is not None:
            self.uncov = uncov

    def __repr__(self):
        txt = "{"
        txt += f"'num_of_mines':{self.num_of_mines}, "
        txt += f"'rows':{self.rows}, "
        txt += f"'columns':{self.columns}, "
        txt += f"'cov':{self.cov}, "
        txt += f"'uncov':{self.uncov}, "
        txt += "}"
        return txt

    def gen_mines(self):
        """Generates a random arrangement of mines in the playing field."""
        pass

    @property
    def num_of_mines(self):
        return self._num_of_mines

    @num_of_mines.setter
    def num_of_mines(self, num_of_mines):
        if not isinstance(num_of_mines, int):
            raise TypeError('num_of_mines should be of type int')
        self._num_of_mines = num_of_mines

    @property
    def rows(self):
        return self._rows

    @rows.setter
    def rows(self, rows):
        if not isinstance(rows, int):
            raise TypeError('rows should be of type int')
        self._rows = rows

    @property
    def columns(self):
        return self._columns

    @columns.setter
    def columns(self, columns):
        if not isinstance(columns, int):
            raise TypeError('columns should be of type int')
        self._columns = columns

    @property
    def force_empty(self):
        return self._force_empty

    @force_empty.setter
    def force_empty(self, force_empty):
        if not isinstance(force_empty, (list, tuple)):
            raise TypeError('force_empty should be of type list or tuple')
        self._force_empty = force_empty

    @property
    def cov(self):
        return self._cov

    @cov.setter
    def cov(self, cov):
        if not isinstance(cov, list):
            raise TypeError('cov should be of type list of lists')
        self._cov = cov

    @property
    def uncov(self):
        return self._uncov

    @uncov.setter
    def uncov(self, uncov):
        if not isinstance(uncov, list):
            raise TypeError('uncov should be of type list of lists')
        self._uncov = uncov


# %%

# %%


class Tile:
    """A single tile on the board.

    Args:
        parent (tk.Frame): Parent Frame of Tile.
        x (int): x coordinate.
        y (int): y coordinate.
        func (function): Function for tile state change.
        state (str): Current state of the given tile covered ('c'), uncovered
            ('0' - '8'), flagged ('f') or mine ('m').
        size (int): Size of tile in pixels.

    Attributes:
        parent (tk.Frame): Parent Frame of Tile.
        x (int): x coordinate.
        y (int): y coordinate.
        func (function): Function for tile state change.
        state (int): Current state of the given tile covered, uncovered or
            flagged.
        size (int): Size of tile in pixels.

    Raises:
        TypeError: If given values do not match their expected types.

    """

    def __init__(self, parent, x, y, func, state='c', size=None):
        self.parent = parent
        self.x = x
        self.y = y
        self.func = func
        self.state = state
        if size is not None:
            self.size = size
        else:
            self.size = None
        self._update()

    def __repr__(self):
        txt = "{"
        txt += f"'parent':{self.parent}, "
        txt += f"'x':{self.x}, "
        txt += f"'y':{self.y}, "
        txt += f"'state':{self.state}, "
        txt += f"'size':{self.size}"
        txt += "}"
        return txt

    def switch(self, state):
        """Switch state of tile."""
        self.button.destroy()
        self.state = state
        self._update()

    def _update(self):
        """Initialize tile with current parameters."""
        bitmap = ICON.get(self.state)
        if self.size is not None:
            bitmap = bitmap.resize((self.size, self.size))
        self.bitmap = ImageTk.PhotoImage(image=bitmap)
        self.button = tk.Button(master=self.parent, image=self.bitmap)
        self.button.bind("<ButtonPress-1><ButtonRelease-1>", self.left_click)
        self.button.bind("<ButtonPress-3><ButtonRelease-3>", self.right_click)

    def left_click(self, event):
        self.switch('m')

    def right_click(self, event):
        state = self._func(self.x, self.y)
        self.switch(state)

    def pack(self, *args, **kwargs):
        self.button.pack(*args, **kwargs)

    def grid(self, *args, **kwargs):
        self.button.grid(*args, **kwargs)

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        if not isinstance(parent, tk.Frame):
            raise TypeError('parent should be of type tkinter.Frame')
        self._parent = parent

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        if not isinstance(x, int):
            raise TypeError('x should be of type int')
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        if not isinstance(y, int):
            raise TypeError('y should be of type int')
        self._y = y

    @property
    def func(self):
        return self._func

    @func.setter
    def func(self, func):
        if not callable(func):
            raise TypeError('func should be of type function')
        self._func = func

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        if not isinstance(state, str):
            raise TypeError('state should be of type str')
        self._state = state

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        if not isinstance(size, int):
            raise TypeError('size should be of type int')
        self._size = size


# %%
root = tk.Tk()
root.title('Minesweeper')
root.geometry('640x480')

frame1 = tk.Frame(root)
frame1.pack()


def t(*args, **kwargs):
    return '5'


button1 = Tile(frame1, 0, 0, t, '3', 50)
button1._update()
button1.pack()

root.mainloop()

# %%


class Board:
    """Displays the minesweeper board.

    Apart from displaying the board, allows updating currently displayed
    fields on the board.

    Args:
        parent (tk.Frame): Parent Frame of Tile.
        minefield (MineField): Instance of MineField.

    Attributes:
        parent (tk.Frame): Parent Frame of Tile.
        minefield (MineField): Instance of MineField.

    Raises:
        TypeError: If given values do not match their expected types.

    """

    def __init__(self, parent, minefield):
        self.set_parent(parent)
        self.set_minefield(minefield)
        self._board = []

    def __repr__(self):
        txt = "{"
        txt += f"'parent':{self.parent}, "
        txt += f"'minefield':{self.minefield}, "
        txt += f"'_board':{self._board}"
        txt += "}"
        return txt

    def _update_board(self):
        for i in range(self.minefield.rows):
            tmp = []
            for j in range(self.minefield.columns):
                tmp.append(Tile(self.parent, i, j, self.lookup, size=50))
            self._board.append(tmp)
        for i in range(self.minefield.rows):
            for j in range(self.minefield.columns):
                self._board[i][j].grid(row=i, column=j)

    def lookup(self):
        pass

    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        if not isinstance(parent, tk.Frame):
            raise TypeError('parent should be of type tkinter.Frame')
        self.parent = parent

    def get_minefield(self):
        return self.minefield

    def set_minefield(self, minefield):
        if not isinstance(minefield, MineField):
            raise TypeError('minefield should be of type MineField')
        self.minefield = minefield


# %%
root = tk.Tk()
root.title('Minesweeper')
# root.geometry('500x500')

frame1 = tk.Frame(root)
frame1.pack()

minefield = MineField()

board = Board(frame1, minefield)
board._update_board()

root.mainloop()

# %%


class UserInput:
    """User input for minesweeper gameplay.

    Enables the selection of a field on the board and the choice of whether
    to mark or uncover.

    Args:
        coordinates (list): Selected coordinates.
        action (str): Choice of action.
        board_size (list): Choice of board size.

    Attributes:
        coordinates (list): Current selected coordinates.
        action (str): Choice of action for currently selected coordinates.
        board_size (list): Currently active board size.

    Raises:
        TypeError: If given values do not match their expected types.

    """

    def __init__(self, coordinates, action, board_size):
        self.set_coordinates(coordinates)
        self.set_action(action)
        self.set_board_size(board_size)

    def __repr__(self):
        txt = "{"
        txt += f"'coordinates':{self.coordinates}, "
        txt += f"'action':{self.action}, "
        txt += f"'board_size':{self.board_size}"
        txt += "}"
        return txt

    def get_coordinates(self):
        return self.coordinates

    def set_coordinates(self, coordinates):
        if not isinstance(coordinates, list):
            raise TypeError('coordinates should be of type list')
        self.coordinates = coordinates

    def get_action(self):
        return self.action

    def set_action(self, action):
        if not isinstance(action, str):
            raise TypeError('action should be of type str')
        self.action = action

    def get_board_size(self):
        return self.board_size

    def set_board_size(self, board_size):
        if not isinstance(board_size, list):
            raise TypeError('board_size should be of type list')
        self.board_size = board_size


# %%


# %%


class Scoreboard:
    """Keeps a tally of the current score.

    Is responsible for keeping track of the number of uncovered mines,
    number of times played as well as setup and win conditions.

    Args:
        marked (list): List of currently marked fields.
        mines (list): List of mine loctaions.
        points (int): Number of points.

    Attributes:
        marked (list): List of currently marked fields.
        mines (list): List of mine locations.
        points (int): Number of points.

    Raises:
        TypeError: If given values do not match their expected types.

    """

    def __init__(self, marked, mines, points):
        self.set_marked(marked)
        self.set_mines(mines)
        self.set_points(points)

    def __repr__(self):
        txt = "{"
        txt += f"'marked':{self.marked}, "
        txt += f"'mines':{self.mines}, "
        txt += f"'points':{self.points}"
        txt += "}"
        return txt

    def get_marked(self):
        return self.marked

    def set_marked(self, marked):
        if not isinstance(marked, list):
            raise TypeError('marked should be of type list')
        self.marked = marked

    def get_mines(self):
        return self.mines

    def set_mines(self, mines):
        if not isinstance(mines, list):
            raise TypeError('mines should be of type list')
        self.mines = mines

    def get_points(self):
        return self.points

    def set_points(self, points):
        if not isinstance(points, int):
            raise TypeError('points should be of type int')
        self.points = points


# %%


# %%


def main():
    """Startup function for tkinter GUI Minesweeper game."""
    root = tk.Tk()
    root.title('Minesweeper')
    # root.geometry('720x480')

    score_frame = tk.Frame(root)
    score_frame.pack(side='top', fill='x', padx='1m',
                     pady='1m', ipadx='3m', ipady='3m')

    mines_left = tk.Label(score_frame, text='Mines left: 15')
    mines_left.pack(side='left', padx='3m')

    score = tk.Label(score_frame, text='Score: 3/10')
    score.pack(side='right', padx='3m')

    control_frame = tk.Frame(root)
    control_frame.pack(side='top', fill='x', padx='1m',
                       pady='1m', ipadx='1m', ipady='1m')

    left_frame = tk.Frame(control_frame)
    left_frame.pack(side='left', fill='y', padx='1m',
                    pady='1m', ipadx='3m', ipady='3m')

    x_label = tk.Label(left_frame, text='Number of columns:')
    x_label.pack(side='top', anchor='center')

    x = tk.Entry(left_frame)
    x.pack(side='top', anchor='center')

    y_label = tk.Label(left_frame, text='Number of rows:')
    y_label.pack(side='top', anchor='center')

    y = tk.Entry(left_frame)
    y.pack(side='top', anchor='center')

    middle_frame = tk.Frame(control_frame)
    middle_frame.pack(side='left', fill=tk.BOTH, padx='1m',
                      pady='1m', ipadx='3m', ipady='3m')

    nr_mines_label = tk.Label(middle_frame, text='Number of mines:')
    nr_mines_label.pack(side='top', anchor='center')

    nr_mines = tk.Entry(middle_frame)
    nr_mines.pack(side='top', anchor='center')

    right_frame = tk.Frame(control_frame)
    right_frame.pack(side='right', fill=tk.BOTH, padx='1m',
                     pady='1m', ipadx='3m', ipady='3m')

    start_button = tk.Button(right_frame, text='START')
    start_button.pack(anchor='center')

    board_frame = tk.Frame(root, background='blue')
    board_frame.pack(side='top', fill=tk.BOTH, expand=tk.YES,
                     padx='1m', pady='1m', ipadx='3m', ipady='3m')

    minefield = MineField(10)

    board = Board(board_frame, minefield)
    board._update_board()

    info = tk.Label(root, text='Version 0.1', bd=1,
                    relief='sunken', anchor='w')
    info.pack(side='bottom', fill='x')

    root.mainloop()


# %%
if __name__ == "__main__":
    main()
# %%

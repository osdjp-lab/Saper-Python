"""Minesweeper game implemented via object oriented programming (OOP).

Each Tile is initiated after minefield generation and field value calculation.

Each Tile holds its own state, location, value and references to neighbouring
Tiles.

User triggered Tile uncovering is handled by Tile method.

"""
# %%
import tkinter as tk
from PIL import Image, ImageTk
from random import randrange

ICON = {}  # minesweeper icon dictionary
ICON['c'] = Image.open("Minesweeper icons\\facingDown.png")
ICON['f'] = Image.open("Minesweeper icons\\flagged.png")
for i in range(9):
    ICON[i] = Image.open("Minesweeper icons\\" + str(i) + ".png")
ICON[9] = Image.open("Minesweeper icons\\bomb.png")

# %%


class Tile:
    """A single minesweeper Tile.

    TODO When field is flagged, field should not be uncoverable.

    NOTE Modification applied.

    Args:
        parent (tk.Frame): Parent Frame of Tile.
        x (int): x coordinate.
        y (int): y coordinate.
        state (int): State of the given Tile 0 (empty) or 1 (mine).
        cov (bool, optional): Defaults to True if Tile is covered False
            overwise.
        size (int, optional): Size of Tile in pixels. Defaults to None.

    Attributes:
        parent (tk.Frame): Parent Frame of Tile.
        x (int): x coordinate.
        y (int): y coordinate.
        state (int): State of the given Tile 0 (empty) or 1 (mine).
        cov (bool): Defaults to True if Tile is covered False overwise.
        size (int): Size of Tile in pixels. Defaults to None.
        board (Board): Tile parent Board.
        top_tile (Tile): Top Tile
        bottom_tile (Tile): Bottom Tile
        left_tile (Tile): Left Tile
        right_tile (Tile): Right Tile
        top_left_tile (Tile): Top left Tile
        top_right_tile (Tile): Top right Tile
        bottom_left_tile (Tile): Bottom left Tile
        bottom_right_tile (Tile): Bottom right Tile
        flagged (bool): False if Tile not flagged, True if flagged.
        triggered (bool): False if Tile not triggered, True if triggered.
        tmp_calc (bool): False if temporary Tile state values haven't been
            calculated.
        final_calc (bool): False if final Tile state values haven't been
            calculated.

    Raises:
        TypeError: If given values do not match their expected types.

    """

    def __init__(self, parent, x, y, state, cov=True, size=None):
        self.parent = parent
        self.x = x
        self.y = y
        self.state = state
        self.cov = cov
        if size is None:
            self._size = size
        else:
            self.size = size
        if self.cov:
            self._update('c')
        else:
            self._update(self.state)
        self._board = None
        # surrounding Tile pointers
        self._top_tile = None
        self._bottom_tile = None
        self._left_tile = None
        self._right_tile = None
        self._top_left_tile = None
        self._top_right_tile = None
        self._bottom_left_tile = None
        self._bottom_right_tile = None
        # flags
        self.flagged = False
        self.triggered = False
        self.tmp_calc = False
        self.final_calc = False

    def __repr__(self):
        txt = "{"
        txt += f"'x':{self.x}, "
        txt += f"'y':{self.y}, "
        txt += f"'state':{self.state}, "
        txt += f"'cov':{self.cov}, "
        txt += f"'size':{self.size}"
        txt += "}"
        return txt

    def switch(self, state):
        """Switch state of Tile."""
        self.button.destroy()
        self._update(state)

    def _update(self, state):
        """Initialize Tile with current parameters."""
        bitmap = ICON.get(state)
        if self.size is not None:
            bitmap = bitmap.resize((self.size, self.size))
        self.bitmap = ImageTk.PhotoImage(image=bitmap)
        self.button = tk.Button(master=self.parent, image=self.bitmap)
        self.button.bind("<ButtonPress-1><ButtonRelease-1>", self.left_click)
        self.button.bind("<ButtonPress-3><ButtonRelease-3>", self.right_click)
        self.grid()

    def left_click(self, event):
        """Uncover Tile."""
        if self.cov:
            if not self.flagged:
                if self.state == 9:
                    self._uncover_all()
                else:
                    self._uncover()

    def right_click(self, event):
        """Flag Tile."""
        if self.cov:
            if not self.flagged:
                self.switch('f')
                self.flagged = True
            else:
                self.switch('c')
                self.flagged = False

    def _uncover_all(self):
        """Recursive uncover of all Tiles.

        BUG Partial uncover: when triggered mine is on isolated island
        surrounded by uncovered Tiles.

        NOTE Solution separate out triggered flag from cov so that _uncover_all
        can traverse uncovered Tiles.

        ISSUE SOLVED

        """
        if not self.triggered:
            self.switch(self.state)
            self.cov = False
            self.triggered = True
            # uncover surrounding Tiles if their cov = True
            # top_tile
            if self.top_tile is not None:
                self.top_tile._uncover_all()
            # bottom_tile
            if self.bottom_tile is not None:
                self.bottom_tile._uncover_all()
            # left_tile
            if self.left_tile is not None:
                self.left_tile._uncover_all()
            # right_tile
            if self.right_tile is not None:
                self.right_tile._uncover_all()

    def _uncover(self):
        """Recursive uncover of zero value and surrounding Tiles.

        NOTE cov conditions could be limited down to one location.

        SOLVED

        """
        if self.cov:
            self.switch(self.state)
            self.cov = False
            if self.state == 0:
                # recursively check bordering Tiles
                # uncover and continue or leave
                # top_tile
                if self.top_tile is not None:
                    if self.top_tile.state == 0:
                        self.top_tile._uncover()
                    elif self.top_tile.state != 9:
                        self.top_tile.switch(self.top_tile.state)
                        self.top_tile.cov = False
                # bottom_tile
                if self.bottom_tile is not None:
                    if self.bottom_tile.state == 0:
                        self.bottom_tile._uncover()
                    elif self.bottom_tile.state != 9:
                        self.bottom_tile.switch(self.bottom_tile.state)
                        self.bottom_tile.cov = False
                # left_tile
                if self.left_tile is not None:
                    if self.left_tile.state == 0:
                        self.left_tile._uncover()
                    elif self.left_tile.state != 9:
                        self.left_tile.switch(self.left_tile.state)
                        self.left_tile.cov = False
                # right_tile
                if self.right_tile is not None:
                    if self.right_tile.state == 0:
                        self.right_tile._uncover()
                    elif self.right_tile.state != 9:
                        self.right_tile.switch(self.right_tile.state)
                        self.right_tile.cov = False

    def _value(self):
        """Method for calculating transitioning field state values.

        Original values 0 or 1.

        Calculated values (0-9) projected onto transitional range (10-19).

        """
        value = 0
        if self.state == 1:
            value = 9
        else:
            if self.top_tile is not None:
                if self.top_tile.state in (0, 1):
                    value += self.top_tile.state
                elif self.top_tile.state == 19:
                    value += 1
            if self.bottom_tile is not None:
                if self.bottom_tile.state in (0, 1):
                    value += self.bottom_tile.state
                elif self.bottom_tile.state == 19:
                    value += 1
            if self.left_tile is not None:
                if self.left_tile.state in (0, 1):
                    value += self.left_tile.state
                elif self.left_tile.state == 19:
                    value += 1
            if self.right_tile is not None:
                if self.right_tile.state in (0, 1):
                    value += self.right_tile.state
                elif self.right_tile.state == 19:
                    value += 1
            if self.top_left_tile is not None:
                if self.top_left_tile.state in (0, 1):
                    value += self.top_left_tile.state
                elif self.top_left_tile.state == 19:
                    value += 1
            if self.top_right_tile is not None:
                if self.top_right_tile.state in (0, 1):
                    value += self.top_right_tile.state
                elif self.top_right_tile.state == 19:
                    value += 1
            if self.bottom_left_tile is not None:
                if self.bottom_left_tile.state in (0, 1):
                    value += self.bottom_left_tile.state
                elif self.bottom_left_tile.state == 19:
                    value += 1
            if self.bottom_right_tile is not None:
                if self.bottom_right_tile.state in (0, 1):
                    value += self.bottom_right_tile.state
                elif self.bottom_right_tile.state == 19:
                    value += 1
        return value + 10

    def calculate_values(self):
        """In-place field value calculation.

        NOTE reason why original commented final value calculation failed.

        """
        self.tmp_value_calc()
        self.final_value_calc()
        # if not self.final_calc:
        #     self.state -= 10
        #     self.final_calc = True

    def tmp_value_calc(self):
        """Transitional value calculation."""
        if not self.tmp_calc:
            self.state = self._value()
            self.tmp_calc = True
            # recursively check bordering Tiles calculate their
            # transitional state value and continue
            # top_tile
            if self.top_tile is not None:
                self.top_tile.tmp_value_calc()
            # bottom_tile
            if self.bottom_tile is not None:
                self.bottom_tile.tmp_value_calc()
            # left_tile
            if self.left_tile is not None:
                self.left_tile.tmp_value_calc()
            # right_tile
            if self.right_tile is not None:
                self.right_tile.tmp_value_calc()

    def final_value_calc(self):
        """Final value calculation."""
        if not self.final_calc:
            self.state -= 10
            self.final_calc = True
            # recursively check bordering Tiles calculate their
            # final state value and continue
            # top_tile
            if self.top_tile is not None:
                self.top_tile.final_value_calc()
            # bottom_tile
            if self.bottom_tile is not None:
                self.bottom_tile.final_value_calc()
            # left_tile
            if self.left_tile is not None:
                self.left_tile.final_value_calc()
            # right_tile
            if self.right_tile is not None:
                self.right_tile.final_value_calc()

    def grid(self, *args, **kwargs):
        self.button.grid(row=self.x, column=self.y, *args, **kwargs)

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
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        if not isinstance(state, int):
            raise TypeError('state should be of type int')
        self._state = state

    @property
    def cov(self):
        return self._cov

    @cov.setter
    def cov(self, cov):
        if not isinstance(cov, bool):
            raise TypeError('cov should be of type bool')
        self._cov = cov

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        if not isinstance(size, int):
            raise TypeError('size should be of type int')
        self._size = size

    @property
    def top_tile(self):
        return self._top_tile

    @top_tile.setter
    def top_tile(self, top_tile):
        if not isinstance(top_tile, Tile):
            raise TypeError('top_tile should be of type Tile')
        self._top_tile = top_tile

    @property
    def bottom_tile(self):
        return self._bottom_tile

    @bottom_tile.setter
    def bottom_tile(self, bottom_tile):
        if not isinstance(bottom_tile, Tile):
            raise TypeError('bottom_tile should be of type Tile')
        self._bottom_tile = bottom_tile

    @property
    def left_tile(self):
        return self._left_tile

    @left_tile.setter
    def left_tile(self, left_tile):
        if not isinstance(left_tile, Tile):
            raise TypeError('left_tile should be of type Tile')
        self._left_tile = left_tile

    @property
    def right_tile(self):
        return self._right_tile

    @right_tile.setter
    def right_tile(self, right_tile):
        if not isinstance(right_tile, Tile):
            raise TypeError('right_tile should be of type Tile')
        self._right_tile = right_tile

    @property
    def top_left_tile(self):
        return self._top_left_tile

    @top_left_tile.setter
    def top_left_tile(self, top_left_tile):
        if not isinstance(top_left_tile, Tile):
            raise TypeError('top_left_tile should be of type Tile')
        self._top_left_tile = top_left_tile

    @property
    def top_right_tile(self):
        return self._top_right_tile

    @top_right_tile.setter
    def top_right_tile(self, top_right_tile):
        if not isinstance(top_right_tile, Tile):
            raise TypeError('top_right_tile should be of type Tile')
        self._top_right_tile = top_right_tile

    @property
    def bottom_left_tile(self):
        return self._bottom_left_tile

    @bottom_left_tile.setter
    def bottom_left_tile(self, bottom_left_tile):
        if not isinstance(bottom_left_tile, Tile):
            raise TypeError('bottom_left_tile should be of type Tile')
        self._bottom_left_tile = bottom_left_tile

    @property
    def bottom_right_tile(self):
        return self._bottom_right_tile

    @bottom_right_tile.setter
    def bottom_right_tile(self, bottom_right_tile):
        if not isinstance(bottom_right_tile, Tile):
            raise TypeError('bottom_right_tile should be of type Tile')
        self._bottom_right_tile = bottom_right_tile

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, board):
        if not isinstance(board, Board):
            raise TypeError('board should be of type Board')
        self._board = board


# %%


class Board:
    """Minesweeper Board consisting of Tiles.

    TODO Instead of parent frame containing the board create secondary frame
    within the parent frame for the score frame above and the status frame
    below. The change will also allow for more tkinter gui like packing and
    grid behaviour of Minesweeper.

    NOTE Modification applied.

    TODO 1) Main frame, subframes and Tile resizing.
    TODO 2) Force first Tile to be uncovered to be empty.
    TODO 3) Play, win and lose self resizing, and self repositioning frames.
    TODO 4) Interactive only when no active game score frame controls.
    TODO 5) Auto updated status frame values.

    NOTE Extra features:

    TODO 6) Before play button is pressed automatically playing
    non-interactive Minesweeper game in the background.

    NOTE First move can be random under the assumption that point 2 is
    implemented.
    while loop
    Halt program exectution for a random amount of time in the range (1-3) s.
    Generate list of deduceable empty fields based upon rules of deduction.
    I. List all cov == True fields with at least one cov == False neighbouring
    field the state of which is not equal 9.
    II. From remaining list remove remaining non-deduceable fields.
    Selected and uncover a randomly field.
    exit condition: win (all empty fields have been uncovered)

    TODO Find information on codetags/markup in vscode
    https://www.python.org/dev/peps/pep-0350/

    Args:
        parent (tk.Frame): Parent Frame Minesweeper.
        x (int): Vertical size of minefield.
        y (int): Horizontal size of minefield.
        z (int): Number of mines.
        debug (bool, optional): Debug flag. Defaults to False.

    Attributes:
        parent (tk.Frame): Parent Frame Minesweeper.
        x (int): Vertical size of minefield.
        y (int): Horizontal size of minefield.
        z (int): Number of mines.
        debug (bool): Debug flag. Defaults to False.
        main_frame (tk.Frame): Main frame for containing Minesweeper subframes.
        score_frame (tk.Frame): Subframe containing current score tally
            including number of games played, number of losses and number of
            wins.
        board_frame (tk.Frame): Subframe containing Minesweeper board.
        status_frame (tk.Frame): Subframe containing game status including
            current board size and number of mines.
        minefield (list of lists of int): Representation of minesweeper board
            containing 0 (empty fields) and 1 (mines).
        board (list of lists of Tile): Contains Tiles which make up the
            minesweeper board.

    """

    def __init__(self, parent, x, y, z, debug=False):
        self.parent = parent
        self.x = x
        self.y = y
        self.z = z
        self.debug = debug
        self.main_frame = tk.Frame(self.parent)
        self.score_frame = tk.Frame(self.main_frame)
        self.board_frame = tk.Frame(self.main_frame)
        self.status_frame = tk.Frame(self.main_frame)
        self._generate_minefield()
        self._init_tiles()
        self._link_tiles()

    def __repr__(self):
        txt = "{"
        txt += f"'x':{self.x}, "
        txt += f"'y':{self.y}, "
        txt += f"'z':{self.z}, "
        txt += f"'debug':{self.debug}, "
        txt += f"'minefield':{self.minefield}"
        txt += "}"
        return txt

    def _generate_minefield(self):
        """Generate and fill empty minefield."""
        self.minefield = []

        # generation of empty minefield
        for _ in range(self.x):
            self.minefield.append(self.y * [0])

        # addition of mines to the minefield
        j = 0
        while j < self.z:
            a = randrange(1, self.x)
            b = randrange(1, self.y)
            if self.minefield[a][b] == 0:
                self.minefield[a][b] = 1
                j += 1
        if self.debug:
            print("0/1 minefield representation:\n")
            for line in self.minefield:
                print(line)

    def _init_tiles(self):
        """Tile initialization.

        NOTE Empty minefield generation and selection of mine locations could
        be integrated into Tile initialization.

        """
        self.board = [self.y * [0] for _ in range(self.x)]
        for i in range(self.x):
            for j in range(self.y):
                self.board[i][j] = Tile(self.board_frame, i, j,
                                        self.minefield[i][j], size=50)

    def _link_tiles(self):
        """Tile linking."""
        # Horizontal linking
        for i in range(self.x):
            for j in range(self.y-1):
                self.board[i][j].right_tile = self.board[i][j + 1]
                self.board[i][j + 1].left_tile = self.board[i][j]

        # Vertical linking
        for i in range(self.x-1):
            for j in range(self.y):
                self.board[i][j].bottom_tile = self.board[i + 1][j]
                self.board[i + 1][j].top_tile = self.board[i][j]

        # Bottom-Right and Top-Left cross linking
        for i in range(self.x-1):
            for j in range(self.y-1):
                self.board[i][j].bottom_right_tile = self.board[i + 1][j + 1]
                self.board[i + 1][j + 1].top_left_tile = self.board[i][j]

        # Bottom-Left and Top-Right cross linking
        for i in range(1, self.x):
            for j in range(self.y-1):
                self.board[i][j].bottom_left_tile = self.board[i - 1][j + 1]
                self.board[i - 1][j + 1].top_right_tile = self.board[i][j]

        # Calculation of values for each field
        self.board[0][0].calculate_values()
        if self.debug:
            print("\nMinefield with calculated values:\n")
            for line in self.board:
                print([i.state for i in line])
        self.score_frame.pack(side='top')
        self.board_frame.pack(side='top')
        self.status_frame.pack(side='top')

    def pack(self, *args, **kwargs):
        self.main_frame.pack(*args, **kwargs)

    def grid(self, *args, **kwargs):
        self.main_frame.grid(*args, **kwargs)
    
    def destroy(self, *args, **kwargs):
        self.main_frame.destroy(*args, **kwargs)

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        if not isinstance(parent, (tk.Tk, tk.Frame)):
            msg = 'parent should be of type tkinter.Tk or tkinter.Frame'
            raise TypeError(msg)
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
    def z(self):
        return self._z

    @z.setter
    def z(self, z):
        if not isinstance(z, int):
            raise TypeError('z should be of type int')
        self._z = z

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, debug):
        if not isinstance(debug, bool):
            raise TypeError('debug should be of type bool')
        self._debug = debug

    @property
    def main_frame(self):
        return self._main_frame

    @main_frame.setter
    def main_frame(self, main_frame):
        if not isinstance(main_frame, tk.Frame):
            raise TypeError('main_frame should be of type tkinter.Frame')
        self._main_frame = main_frame

    @property
    def score_frame(self):
        return self._score_frame

    @score_frame.setter
    def score_frame(self, score_frame):
        if not isinstance(score_frame, tk.Frame):
            raise TypeError('score_frame should be of type tkinter.Frame')
        self._score_frame = score_frame

    @property
    def board_frame(self):
        return self._board_frame

    @board_frame.setter
    def board_frame(self, board_frame):
        if not isinstance(board_frame, tk.Frame):
            raise TypeError('board_frame should be of type tkinter.Frame')
        self._board_frame = board_frame

    @property
    def status_frame(self):
        return self._status_frame

    @status_frame.setter
    def status_frame(self, status_frame):
        if not isinstance(status_frame, tk.Frame):
            raise TypeError('status_frame should be of type tkinter.Frame')
        self._status_frame = status_frame


# %%


class Minesweeper:
    """Minesweeper game.

    Args:
        parent (tk.Tk or tk.Frame): Parent tkinter Window or Frame Minesweeper.
        debug (bool, optional): Debug flag. Defaults to False.

    Attributes:
        parent (tk.Tk or tk.Frame): Parent tkinter Window or Frame Minesweeper.
        debug (bool): Debug flag. Defaults to False.

    Raises:
        TypeError: If given values do not match their expected types.

    """

    def __init__(self, parent):
        self.parent = parent

    def start(self):
        self.minesweeper = Board(self.parent, self.x, self.y,
                                 self.z, self.debug)
    
    def pack(self, *args, **kwargs):
        self.minesweeper.pack(*args, **kwargs)

    def grid(self, *args, **kwargs):
        self.minesweeper.grid(*args, **kwargs)

    def destroy(self, *args, **kwargs):
        self.minesweeper.destroy(*args, **kwargs)

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        if not isinstance(parent, (tk.Tk, tk.Frame)):
            msg = 'parent should be of type tkinter.Tk or tkinter.Frame'
            raise TypeError(msg)
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
    def z(self):
        return self._z

    @z.setter
    def z(self, z):
        if not isinstance(z, int):
            raise TypeError('z should be of type int')
        self._z = z

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, debug):
        if not isinstance(debug, bool):
            raise TypeError('debug should be of type bool')
        self._debug = debug


# %%

root = tk.Tk()
root.title('Minesweeper')
game1 = Minesweeper(root)
game1.pack()
root.mainloop()

# %%

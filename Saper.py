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
    """A single tile on the board.

    Args:
        parent (tk.Frame): Parent Frame of Tile.
        x (int): x coordinate.
        y (int): y coordinate.
        state (int): State of the given tile values from range 0 to 9.
        cov (bool): Defaults to True if Tile is covered False overwise.
        size (int): Size of tile in pixels. Defaults to None.

    Attributes:
        parent (tk.Frame): Parent Frame of Tile.
        x (int): x coordinate.
        y (int): y coordinate.
        state (int): State of the given tile values from range 0 to 9.
        cov (bool): Defaults to True if Tile is covered False overwise.
        size (int): Size of tile in pixels. Defaults to None.

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
        self._top_tile = None
        self._bottom_tile = None
        self._left_tile = None
        self._right_tile = None

    def __repr__(self):
        txt = "{"
        txt += f"'parent':{self.parent}, "
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
            if self.state == 9:
                self._uncover_all()
            else:
                self._uncover()

    def _uncover_all(self):
        """Recursive uncover of all Tiles.
        
        BUG Partial uncover: when triggered mine is on isolated island
        surrounded by uncovered Tiles.

        NOTE Solution separate out triggered flag from cov so that _uncover_all
        can traverse uncovered Tiles.
        
        """
        self.switch(self.state)
        self.cov = False
        # uncover surrounding Tiles if their cov = True
        # top_tile
        if self.top_tile is not None:
            if self.top_tile.cov:
                self.top_tile._uncover_all()
        # bottom_tile
        if self.bottom_tile is not None:
            if self.bottom_tile.cov:
                self.bottom_tile._uncover_all()
        # left_tile
        if self.left_tile is not None:
            if self.left_tile.cov:
                self.left_tile._uncover_all()
        # right_tile
        if self.right_tile is not None:
            if self.right_tile.cov:
                self.right_tile._uncover_all()

    def _uncover(self):
        """Recursive uncover of zero value and surrounding Tiles."""
        self.switch(self.state)
        self.cov = False
        if self.state == 0:
            # recursively check bordering Tiles
            # uncover and continue or leave
            # top_tile
            if self.top_tile is not None:
                if self.top_tile.cov:
                    if self.top_tile.state == 0:
                        self.top_tile._uncover()
                    elif self.top_tile.state != 9:
                        self.top_tile.switch(self.top_tile.state)
                        self.top_tile.cov = False
            # bottom_tile
            if self.bottom_tile is not None:
                if self.bottom_tile.cov:
                    if self.bottom_tile.state == 0:
                        self.bottom_tile._uncover()
                    elif self.bottom_tile.state != 9:
                        self.bottom_tile.switch(self.bottom_tile.state)
                        self.bottom_tile.cov = False
            # left_tile
            if self.left_tile is not None:
                if self.left_tile.cov:
                    if self.left_tile.state == 0:
                        self.left_tile._uncover()
                    elif self.left_tile.state != 9:
                        self.left_tile.switch(self.left_tile.state)
                        self.left_tile.cov = False
            # right_tile
            if self.right_tile is not None:
                if self.right_tile.cov:
                    if self.right_tile.state == 0:
                        self.right_tile._uncover()
                    elif self.right_tile.state != 9:
                        self.right_tile.switch(self.right_tile.state)
                        self.right_tile.cov = False

    def right_click(self, event):
        """Flag Tile."""
        if self.cov:
            self.switch('f')

    def pack(self, *args, **kwargs):
        self.button.pack(*args, **kwargs)

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


# %%


def value_calc_ver_1(minefield, x, y):
    """Minimal amount of code value calculation.

    85 lines.

    Args:
        minefield (list of lists): Minefield containing 0 (empty fields) and 1
            (mines).
        x (int): Vertical size of minefield.
        y (int): Horizontal size of minefield.

    Returns:
        list of lists: Minefield containing calculated values.

    """
    minefield_values = [y * [0] for _ in range(x)]
    for i in range(x):
        for j in range(y):
            # if a field in either direction along the horizontal or vertical
            # axis is out of bound then other fields sharing the same
            # coordiate are also out of bound
            up, down, left, right = True, True, True, True
            # up-down check
            if i == 0:
                up = False
            elif i + 1 == x:
                down = False
            # left-right check
            if j == 0:
                left = False
            elif j + 1 == y:
                right = False
            if minefield[i][j] == 1:
                value = 9
            else:
                # current field
                value = minefield[i][j]
                if up:
                    # field above
                    value += minefield[i-1][j]
                    if down:
                        # field below
                        value += minefield[i+1][j]
                        if left:
                            # field to the left
                            value += minefield[i][j-1]
                            if right:
                                # field to the right
                                value += minefield[i][j+1]
                                # remaining available fields
                                value += minefield[i-1][j-1]
                                value += minefield[i-1][j+1]
                                value += minefield[i+1][j-1]
                                value += minefield[i+1][j+1]
                            else:
                                value += minefield[i-1][j-1]
                                value += minefield[i+1][j-1]
                        else:
                            # field to the right
                            value += minefield[i][j+1]
                            # remaining available fields
                            value += minefield[i+1][j+1]
                            value += minefield[i-1][j+1]
                    else:
                        if left:
                            # field to the left
                            value += minefield[i][j-1]
                            if right:
                                # field to the right
                                value += minefield[i][j+1]
                                # remaining available fields
                                value += minefield[i-1][j-1]
                                value += minefield[i-1][j+1]
                            else:
                                value += minefield[i-1][j-1]
                        else:
                            # field to the right
                            value += minefield[i][j+1]
                            # remaining available fields
                            value += minefield[i-1][j+1]
                else:
                    # field below
                    value += minefield[i+1][j]
                    if left:
                        # field to the left
                        value += minefield[i][j-1]
                        if right:
                            # field to the right
                            value += minefield[i][j+1]
                            # remaining available fields
                            value += minefield[i+1][j-1]
                            value += minefield[i+1][j+1]
                        else:
                            value += minefield[i+1][j-1]
                    else:
                        # field to the right
                        value += minefield[i][j+1]
                        value += minefield[i+1][j+1]
            minefield_values[i][j] = value
    return minefield_values


def value_calc_ver_2(minefield, x, y):
    """Minimal amount of code value calculation.

    74 lines.

    Args:
        minefield (list of lists): Minefield containing 0 (empty fields) and 1
            (mines).
        x (int): Vertical size of minefield.
        y (int): Horizontal size of minefield.

    Returns:
        list of lists: Minefield containing calculated values.

    """
    minefield_values = [y * [0] for _ in range(x)]
    for i in range(x):
        for j in range(y):
            # if a field in either direction along the horizontal or vertical
            # axis is out of bound then other fields sharing the same
            # coordiate are also out of bound
            if minefield[i][j] == 1:
                value = 9
            else:
                # current field
                value = minefield[i][j]
                if i != 0:
                    # field above
                    value += minefield[i-1][j]
                    if i + 1 != x:
                        # field below
                        value += minefield[i+1][j]
                        if j != 0:
                            # field to the left
                            value += minefield[i][j-1]
                            if j + 1 != y:
                                # field to the right
                                value += minefield[i][j+1]
                                # remaining available fields
                                value += minefield[i-1][j-1]
                                value += minefield[i-1][j+1]
                                value += minefield[i+1][j-1]
                                value += minefield[i+1][j+1]
                            else:
                                value += minefield[i-1][j-1]
                                value += minefield[i+1][j-1]
                        else:
                            # field to the right
                            value += minefield[i][j+1]
                            # remaining available fields
                            value += minefield[i+1][j+1]
                            value += minefield[i-1][j+1]
                    else:
                        if j != 0:
                            # field to the left
                            value += minefield[i][j-1]
                            if j + 1 != y:
                                # field to the right
                                value += minefield[i][j+1]
                                # remaining available fields
                                value += minefield[i-1][j-1]
                                value += minefield[i-1][j+1]
                            else:
                                value += minefield[i-1][j-1]
                        else:
                            # field to the right
                            value += minefield[i][j+1]
                            # remaining available fields
                            value += minefield[i-1][j+1]
                else:
                    # field below
                    value += minefield[i+1][j]
                    if j != 0:
                        # field to the left
                        value += minefield[i][j-1]
                        if j + 1 != y:
                            # field to the right
                            value += minefield[i][j+1]
                            # remaining available fields
                            value += minefield[i+1][j-1]
                            value += minefield[i+1][j+1]
                        else:
                            value += minefield[i+1][j-1]
                    else:
                        # field to the right
                        value += minefield[i][j+1]
                        value += minefield[i+1][j+1]
            minefield_values[i][j] = value
    return minefield_values


def value_calc_ver_3(minefield, x, y):
    """Minimal number of steps value calculation.

    78 lines.

    Args:
        minefield (list of lists): Minefield containing 0 (empty fields) and 1
            (mines).
        x (int): Vertical size of minefield.
        y (int): Horizontal size of minefield.

    Returns:
        list of lists: Minefield containing calculated values.

    """
    minefield_values = [y * [0] for _ in range(x)]
    # top-left corner (0, 0)
    if minefield[0][0] == 1:
        value = 9
    else:
        value = minefield[0][0] + minefield[0][1]
        value += minefield[1][0] + minefield[1][1]
    minefield_values[0][0] = value
    # top-right corner (0, y-1)
    if minefield[0][y-1] == 1:
        value = 9
    else:
        value = minefield[0][y-1] + minefield[0][y-2]
        value += minefield[1][y-1] + minefield[1][y-2]
    minefield_values[0][y-1] = value
    # bottom-left corner (x-1, 0)
    if minefield[x-1][0] == 1:
        value = 9
    else:
        value = minefield[x-1][0] + minefield[x-1][1]
        value += minefield[x-2][0] + minefield[x-2][1]
    minefield_values[x-1][0] = value
    # bottom-right corner (x-1, y-1)
    if minefield[x-1][y-1] == 1:
        value = 9
    else:
        value = minefield[x-1][y-1] + minefield[x-1][y-2]
        value += minefield[x-2][y-1] + minefield[x-2][y-2]
    minefield_values[x-1][y-1] = value
    # upper edge (0, (1, y-2))
    for j in range(1, y-1):
        if minefield[0][j] == 1:
            value = 9
        else:
            value = minefield[0][j-1] + minefield[0][j]
            value += minefield[0][j+1] + minefield[1][j-1]
            value += minefield[1][j] + minefield[1][j+1]
        minefield_values[0][j] = value
    # lower edge (x-1, (1, y-2))
    for j in range(1, y-1):
        if minefield[x-1][j] == 1:
            value = 9
        else:
            value = minefield[x-1][j-1] + minefield[x-1][j]
            value += minefield[x-1][j+1] + minefield[x-2][j-1]
            value += minefield[x-2][j] + minefield[x-2][j+1]
        minefield_values[x-1][j] = value
    # left edge ((1, x-2), 0)
    for i in range(1, x-1):
        if minefield[i][0] == 1:
            value = 9
        else:
            value = minefield[i-1][0] + minefield[i][0]
            value += minefield[i+1][0] + minefield[i-1][1]
            value += minefield[i][1] + minefield[i+1][1]
        minefield_values[i][0] = value
    # right edge ((1, x-2), y-1)
    for i in range(1, x-1):
        if minefield[i][y-1] == 1:
            value = 9
        else:
            value = minefield[i-1][y-1] + minefield[i][y-1]
            value += minefield[i+1][y-1] + minefield[i-1][y-2]
            value += minefield[i][y-2] + minefield[i+1][y-2]
        minefield_values[i][y-1] = value
    # all non border fields
    for i in range(1, x-1):
        for j in range(1, y-1):
            if minefield[i][j] == 1:
                value = 9
            else:
                value = minefield[i][j]
                value += minefield[i][j-1] + minefield[i][j+1]
                value += minefield[i-1][j-1] + minefield[i-1][j]
                value += minefield[i-1][j+1] + minefield[i+1][j-1]
                value += minefield[i+1][j] + minefield[i+1][j+1]
            minefield_values[i][j] = value
    return minefield_values


def value_calc_ver_4(minefield, x, y):
    """In-place field value calculation and substitution.

    Issues: Once a single value is replaced behaviour of algorithm must
    change adjusting to the now heterogenous environment caused by the
    substituted value.

    Any field value already substituted could be changed to (string format or
    to a int value exceeding 9) as an indicator of having been processed.

    Args:
        minefield (list of lists): Minefield containing 0 (empty fields) and 1
            (mines).
        x (int): Vertical size of minefield.
        y (int): Horizontal size of minefield.

    Returns:
        list of lists: Minefield containing calculated values.

    """
    pass


# %%


def generate_minefield(x, y, z):
    """Main minesweeper function.

    Generate minefield, calculate values of each field and display minefield.

    Args:
        x (int): Vertical size of minefield.
        y (int): Horizontal size of minefield.
        z (int): Number of mines.

    """
    minefield = []
    # generation of empty minefield
    for _ in range(x):
        minefield.append(y * [0])
    # addition of mines to the field
    j = 0
    while j < z:
        a = randrange(1, x)
        b = randrange(1, y)
        if minefield[a][b] == 0:
            minefield[a][b] = 1
            j += 1
    for line in minefield:
        print(line)
    print("-----------------------")
    # calculation of values for each field and substitution
    minefield_values = value_calc_ver_3(minefield, x, y)
    for line in minefield_values:
        print(line)
    # Initialization of Tiles
    root = tk.Tk()
    root.title('Minesweeper')
    frame1 = tk.Frame(root)
    frame1.pack()
    board = [y * [0] for _ in range(x)]
    for i in range(x):
        for j in range(y):
            board[i][j] = Tile(frame1, i, j, minefield_values[i][j], size=50)
    # Tile linking
    for i in range(x):
        for j in range(y-1):
            board[i][j].right_tile = board[i][j + 1]
            board[i][j + 1].left_tile = board[i][j]
    for i in range(x-1):
        for j in range(y):
            board[i][j].bottom_tile = board[i + 1][j]
            board[i + 1][j].top_tile = board[i][j]
    root.mainloop()


# %%
generate_minefield(10, 10, 15)

# %%

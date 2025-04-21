# #This class represents an entire Sudoku board. A Board object has 81 Cell objects.
#
# def __init__(self, width, height, screen, difficulty):
# 	# Constructor for the Board class.
# 	# screen is a window from PyGame.
# 	# difficulty is a variable to indicate if the user chose easy medium, or hard.
#
# def draw(self):
# 	Draws an outline of the Sudoku grid, with bold lines to delineate the 3x3 boxes.
# 	Draws every cell on this board.
#
#
# def select(self, row, col):
# 	Marks the cell at (row, col) in the board as the current selected cell.
# 	Once a cell has been selected, the user can edit its value or sketched value.
#
# def click(self, row, col):
# 	If a tuple of (x,y) coordinates is within the displayed board,
# this function returns a tuple of the (row, col) of the cell which was clicked.
# Otherwise, this function returns None.
#
# def clear(self):
# 	Clears the value cell.
# Note that the user can only remove the cell values and
# sketched values that are filled by themselves.
#
# def sketch(self, value):
# 	Sets the sketched value of the current selected cell equal to the user entered value.
# 	It will be displayed at the top left corner of the cell using the draw() function.
#
# def place_number(self, value):
# 	Sets the value of the current selected cell equal to the user entered value.
# Called when the user presses the Enter key.
#
# def reset_to_original(self):
# 	Resets all cells in the board to their original values
# (0 if cleared, otherwise the corresponding digit).
#
# def is_full(self):
# 	Returns a Boolean value indicating whether the board is full or not.
#
# def update_board(self):
# 	Updates the underlying 2D board with the values in all cells.
#
# def find_empty(self):
# 	Finds an empty cell and returns its row and col as a tuple (x,y).
#
# def check_board(self):
# Check whether the Sudoku board is solved correctly.

import pygame
from sudoku_generator import generate_sudoku
from Cell import Cell

class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        if difficulty == 'easy':
            self.removed_cells = 30
        elif difficulty == 'medium':
            self.removed_cells = 40
        elif difficulty == 'hard':
            self.removed_cells = 50
        else:
            self.removed_cells = 40
        self.board = generate_sudoku(9, self.removed_cells)
        self.original = []
        for r in range(9):
            row = []
            for c in range(9):
                row.append(self.board[r][c])
            self.original.append(row)
        self.cells = []
        for r in range(9):
            row_cells = []
            for c in range(9):
                cell = Cell(self.board[r][c], r, c, self.screen)
                row_cells.append(cell)
            self.cells.append(row_cells)
        self.selected = None

    def draw(self):
        cell_size = self.width / 9
        for i in range(10):
            if i % 3 == 0:
                line_width = 4
            else:
                line_width = 1
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * cell_size), (self.width, i * cell_size), line_width)
            pygame.draw.line(self.screen, (0, 0, 0), (i * cell_size, 0), (i * cell_size, self.height), line_width)
        for r in range(9):
            for c in range(9):
                self.cells[r][c].draw()

    def select(self, row, col):
        if self.selected is not None:
            old_r, old_c = self.selected
            self.cells[old_r][old_c].selected = False
        self.selected = (row, col)
        self.cells[row][col].selected = True

    def click(self, x, y):
        cell_size = self.width / 9
        if x < 0 or x > self.width or y < 0 or y > self.height:
            return None
        row = int(y // cell_size)
        col = int(x // cell_size)
        return (row, col)

    def clear(self):
        if self.selected is None:
            return
        r, c = self.selected
        if self.original[r][c] == 0:
            self.cells[r][c].set_cell_value(0)
            self.cells[r][c].set_sketched_value(0)

    def sketch(self, value):
        if self.selected is None:
            return
        r, c = self.selected
        if self.original[r][c] == 0:
            self.cells[r][c].set_sketched_value(value)

    def place_number(self, value):
        if self.selected is None:
            return False
        r, c = self.selected
        if self.original[r][c] == 0:
            self.cells[r][c].set_cell_value(value)
            self.cells[r][c].set_sketched_value(0)
            self.update_board()
            return True
        else:
            return False

    def reset_to_original(self):
        for r in range(9):
            for c in range(9):
                val = self.original[r][c]
                self.cells[r][c].set_cell_value(val)
                self.cells[r][c].set_sketched_value(0)
        self.update_board()

    def is_full(self):
        for r in range(9):
            for c in range(9):
                if self.cells[r][c].value == 0:
                    return False
        return True

    def update_board(self):
        for r in range(9):
            for c in range(9):
                self.board[r][c] = self.cells[r][c].value

    def find_empty(self):
        for r in range(9):
            for c in range(9):
                if self.board[r][c] == 0:
                    return (r, c)
        return None

    def check_board(self):
        for r in range(9):
            nums = []
            for c in range(9):
                nums.append(self.board[r][c])
            nums.sort()
            if nums != [1,2,3,4,5,6,7,8,9]:
                return False
        for c in range(9):
            nums = []
            for r in range(9):
                nums.append(self.board[r][c])
            nums.sort()
            if nums != [1,2,3,4,5,6,7,8,9]:
                return False
        for br in range(3):
            for bc in range(3):
                nums = []
                for r in range(br*3, br*3 + 3):
                    for c in range(bc*3, bc*3 + 3):
                        nums.append(self.board[r][c])
                nums.sort()
                if nums != [1,2,3,4,5,6,7,8,9]:
                    return False
        return True

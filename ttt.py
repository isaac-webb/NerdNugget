from time import sleep
from gfx_pack import GfxPack
from drawing_helpers import clear
from nugget import Scene

# Configuration constants
box_width = 18

class Square:
    def draw(self, display, i, j):
        return

class Ex(Square):
    def draw(self, display, i, j):
        display.set_pen(15)
        display.line(64-int(3*box_width/2)+int(i*box_width), int(j*box_width), 64-int(3*box_width/2)+int((i+1)*box_width), int((j+1)*box_width), 1)
        display.line(64-int(3*box_width/2)+int(i*box_width), int((j+1)*box_width), 64-int(3*box_width/2)+int((i+1)*box_width), int(j*box_width), 1)

class Oh(Square):
    def draw(self, display, i, j):
        display.set_pen(15)
        display.circle(64-box_width+int(i*box_width), int(j*box_width+box_width/2), int(box_width/2)-1)
        display.set_pen(0)
        display.circle(64-box_width+int(i*box_width), int(j*box_width+box_width/2), int(box_width/2)-2)

X = Ex()
O = Oh()
BLANK = Square()

class Board:
    def __init__(self):
        self._grid = [
            [BLANK, BLANK, BLANK],
            [BLANK, BLANK, BLANK],
            [BLANK, BLANK, BLANK]
        ]

    def draw(self, display):
        # Draw the grid
        display.set_pen(15)
        display.line(64-int(box_width/2), 0, int(64-box_width/2), int(box_width*3), 1)
        display.line(64+int(box_width/2), 0, 64+int(box_width/2), int(box_width*3), 1)
        display.line(64-int(3*box_width/2), box_width, 64+int(3*box_width/2), box_width, 1)
        display.line(64-int(3*box_width/2), int(box_width*2), 64+int(3*box_width/2), int(box_width*2), 1)
        
        # Draw the xs and os
        for i in range(3):
            for j in range(3):
                self._grid[i][j].draw(display, i, j)
        display.update()
    
    def get_cursor(self):
        i = 0
        while i < 9:
            if self._grid[i//3][i%3] == BLANK:
                return [i//3, i%3]
            i += 1
        return [-1, 0]
    
    def inc_i(self, cursor):
        original = [cursor[0], cursor[1]]
        for i in range(1, 3):
            cursor = [(original[0] + i) % 3, original[1]]
            if self._grid[cursor[0]][cursor[1]] == BLANK:
                return cursor
            for j in range(3):
                cursor[1] = j
                if self._grid[cursor[0]][cursor[1]] == BLANK:
                    return cursor
        return original
    
    def inc_j(self, cursor):
        original = [cursor[0], cursor[1]]
        for j in range(1, 3):
            cursor[1] = (original[1] + j) % 3
            if self._grid[cursor[0]][cursor[1]] == BLANK:
                return cursor
        for j in range(1, 3):
            cursor[1] = (original[1] + j) % 3
            for i in range(3):
                cursor[0] = i
                if self._grid[cursor[0]][cursor[1]] == BLANK:
                    return cursor
        return original
    
    def x(self, i, j):
        self._grid[i][j] = X
    
    def o(self, i, j):
        self._grid[i][j] = O
    
    def clear(self, i, j):
        self._grid[i][j] = BLANK
    
    def winner(self):
        # Check rows
        for i in range(3):
            if self._grid[i][0] == self._grid[i][1] == self._grid[i][2] != BLANK:
                return self._grid[i][0]
        # Check columns
        for j in range(3):
            if self._grid[0][j] == self._grid[1][j] == self._grid[2][j] != BLANK:
                return self._grid[0][j]
        # Check diagonals
        if self._grid[0][0] == self._grid[1][1] == self._grid[2][2] != BLANK:
            return self._grid[0][0]
        if self._grid[0][2] == self._grid[1][1] == self._grid[2][0] != BLANK:
            return self._grid[0][2]
        return BLANK

class TicTacToe(Scene):
    def __init__(self):
        self.board = Board()
        self.cursor = self.board.get_cursor()
        self.board.x(self.cursor[0], self.cursor[1])
        self.on_x = True
        self.winner = BLANK
    
    def pressed_b(self):
        self.board.clear(self.cursor[0], self.cursor[1])
        self.cursor = self.board.inc_i(self.cursor)
        self.board.x(self.cursor[0], self.cursor[1]) if self.on_x else self.board.o(self.cursor[0], self.cursor[1])
        sleep(0.3)
        return False
    
    def pressed_d(self):
        self.board.clear(self.cursor[0], self.cursor[1])
        self.cursor = self.board.inc_j(self.cursor)
        self.board.x(self.cursor[0], self.cursor[1]) if self.on_x else self.board.o(self.cursor[0], self.cursor[1])
        sleep(0.3)
        return False
    
    def pressed_e(self):
        self.winner = self.board.winner()
        if self.winner != BLANK:
            return True
        self.on_x = not self.on_x
        self.cursor = self.board.get_cursor()
        if self.cursor == [-1, 0]:
            return True
        self.board.x(self.cursor[0], self.cursor[1]) if self.on_x else self.board.o(self.cursor[0], self.cursor[1])
        # TODO: Implement a check for finishing the game and returning control to the nugget
        sleep(0.3)
        return False
    
    def draw(self, display):
        clear(display)
        self.board.draw(display)
        display.set_pen(15)
        display.set_font("bitmap6")
        display.text("ESC", 5, 56, scale=1)
        display.text("COL", 30, 56, scale=1)
        display.text("ROW", 80, 56, scale=1)
        display.text("OK", 115, 56, scale=1)
        display.update()
    
    def end_screen(self, display):
        clear(display)
        display.set_pen(15)
        display.set_font("bitmap6")
        display.text("WINNER", 30, 20, scale=2)
        if self.winner == BLANK:
            display.text("TIE", 64, 40, scale=3)
        else:
            display.text("X" if self.winner == X else "O", 64, 40, scale=3)
        display.update()
        sleep(5)
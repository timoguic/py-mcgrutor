import random
from classes.MazeGenerator import maze
from classes.Player import Player

class LabObject:
    def __init__(self, symbol, labyrinthe):
        self.symbol = str(symbol)
        self.line, self.column = random.sample(labyrinthe.empty_positions, 1)[0]
        labyrinthe.set_symbol(self.symbol, self.line, self.column)

    def __str__(self):
        return '<{}({},{})>'.format(self.symbol, self.line, self.column)

class Labyrinthe:
    EMPTY_SYMBOL = ' '
    def __init__(self, lines=15, cols=15, num_objects=3):
        self.level = maze(lines, cols)
        
        self.num_lines = len(self.level)
        self.num_cols = len(self.level[0])
        
        for i in range(1, num_objects+1):
            o = LabObject(i, self)

        self.player = Player(self)
        

    def set_symbol(self, symbol, line, column):
        self.level[line][column] = symbol

    def validate_coords(self, line, column):
        if (line, column) not in self.empty_positions:
            if line >= self.num_lines - 1:
                line = self.num_lines - 1
            elif line < 0:
                line = 0
            
            if column >= self.num_cols - 1:
                column = self.num_cols - 1
            elif column < 0:
                column = 0

        return (line, column, self.level[line][column])

    def move_symbol(self, symbol, line, column, direction):
        new_line = line
        new_col = column

        if direction == 'up':
            new_line = line - 1
        elif direction == 'down':
            new_line = line + 1
        elif direction == 'left':
            new_col = column - 1
        elif direction == 'right':
            new_col = column + 1
            
        new_line, new_col, new_symbol = self.validate_coords(new_line, new_col)
        if new_symbol == 'X':
            new_line, new_col = line, column
        elif new_symbol.isdigit():
            self.player.pickup(new_symbol)
        elif new_symbol == 'B':
            self.player.fight()

        if new_line is not line or new_col is not column:
            self.set_symbol(self.EMPTY_SYMBOL, line, column)
            self.set_symbol(symbol, new_line, new_col)

        return new_line, new_col


    @property
    def empty_positions(self):
        ret = []
        for nl, line in enumerate(self.level):
            ret += [(nl, nc) for nc, col in enumerate(line) if col == ' ']

        return set(ret)

    def __repr__(self):
        return '<Labyrinthe({})>'.format(self.filepath)

    def __str__(self):
        return '\n'.join(self.level)
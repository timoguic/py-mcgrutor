import pygame
import random
from classes.Screen import Screen
from classes.MazeGenerator import maze


class Game:
    def __init__(self, window, lines=15, cols=15, num_objects=3, sprite_size=30):
        self.window = window
        self.clock = pygame.time.Clock()

        self.labyrinthe = Labyrinthe(lines=lines, cols=cols, num_objects=num_objects)
        screens_list = ('init_screen', 'game_screen', 'end_screen')
        
        for i in screens_list:
            my_screen = Screen(window, i, labyrinthe=self.labyrinthe, sprite_size=sprite_size)
            setattr(self, i, my_screen)
            
        self.current_screen = screens_list[1]

    def run(self):
        run = True
        self.display()
        
        while run:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
                        run = False
                    elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                        if self.current_screen == 'init_screen':
                            self.current_screen = 'game_screen'
                        if self.current_screen == 'end_screen':
                            self.current_screen = 'init_screen'
                            self.labyrinthe = Labyrinthe(self.labyrinthe.filepath)
                    elif self.current_screen == 'game_screen':
                        if event.key == pygame.K_RIGHT:
                            self.labyrinthe.player.move('right')
                        if event.key == pygame.K_LEFT:
                            self.labyrinthe.player.move('left')
                        if event.key == pygame.K_UP:
                            self.labyrinthe.player.move('up')
                        if event.key == pygame.K_DOWN:
                            self.labyrinthe.player.move('down')
                    
                if self.labyrinthe.player.has_finished:
                    self.current_screen = 'end_screen'
                    if self.labyrinthe.player.has_won:
                        self.display(red=0, green=0, blue=255)
                    else:
                        self.display(red=255, green=0, blue=255)
                else:                         
                    self.display()

                self.clock.tick(50)
    
    def display(self, **kwargs):
        getattr(self, self.current_screen).display(**kwargs)

class Player:
    def __init__(self, labyrinthe, line=0, col=0):
        self.symbol = 'M'
        self.items = []
        self.labyrinthe = labyrinthe
        self.line, self.column = random.sample(labyrinthe.empty_positions, 1)[0]
        self.has_finished, self.has_won = False, False

        labyrinthe.set_symbol('M', self.line, self.column)

    def move(self, direction):
        self.line, self.column = self.labyrinthe.move_symbol('M', self.line, self.column, direction)

    def pickup(self, obj):
        self.items.append(obj)
        self.items.sort()

    def fight(self):
        self.has_finished = True

        if len(self.items) >= 3:
            self.has_won = True

        self.has_won = True

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

class LabObject:
    def __init__(self, symbol, labyrinthe):
        self.symbol = str(symbol)
        self.line, self.column = random.sample(labyrinthe.empty_positions, 1)[0]
        labyrinthe.set_symbol(self.symbol, self.line, self.column)

    def __str__(self):
        return '<{}({},{})>'.format(self.symbol, self.line, self.column)



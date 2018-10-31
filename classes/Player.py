import random

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
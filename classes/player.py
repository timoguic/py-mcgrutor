""" Module for player management """

import random


class Player:
    """ Player class """

    def __init__(self, labyrinthe, num_objects):
        """ Constructor """
        self.symbol = "M"
        self.items = []
        self.labyrinthe = labyrinthe
        self.line, self.column = random.sample(labyrinthe.empty_positions, 1)[0]
        self.has_finished, self.has_won = False, False
        self.objects_needed = num_objects

        labyrinthe.set_symbol("M", self.line, self.column)

    def move(self, direction):
        """ Move """
        self.line, self.column = self.labyrinthe.move_symbol(
            "M", self.line, self.column, direction
        )
        self.labyrinthe.pathfinder.find_path()

    def pickup(self, obj):
        """ Pickup """
        self.items.append(obj)
        self.items.sort()

    def fight(self):
        """ Fight """
        self.has_finished = True

        if len(self.items) >= self.objects_needed:
            self.has_won = True

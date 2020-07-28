""" Game module """

import pygame
from classes.labyrinthe import Labyrinthe
from classes.screen import Screen


class Game:
    """ Game class """

    def __init__(
        self,
        window,
        lines=15,
        cols=15,
        num_objects=3,
        sprite_size=30,
        density=0.75,
        complexity=0.75,
    ):
        """ Constructor """
        self.window = window
        self.clock = pygame.time.Clock()

        self.lines = lines
        self.cols = cols
        self.num_objects = num_objects
        self.sprite_size = sprite_size
        self.current_screen = None
        self.density = density
        self.complexity = complexity

        self.init_screens(window)
        self.display()

    def init_screens(self, window):
        """ Screen initialization """
        self.labyrinthe = Labyrinthe(
            lines=self.lines,
            cols=self.cols,
            num_objects=self.num_objects,
            density=self.density,
            complexity=self.complexity,
        )

        screens_list = ("init_screen", "game_screen", "end_screen")

        for i in screens_list:
            my_screen = Screen(
                window, i, labyrinthe=self.labyrinthe, sprite_size=self.sprite_size
            )
            setattr(self, i, my_screen)

        self.current_screen = screens_list[1]

    def run(self):
        """ Run method """
        run = True

        while run:
            direction = None

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if (
                            self.current_screen == "init_screen"
                            or self.current_screen == "game_screen"
                        ):
                            self.init_screens(self.window)
                            self.current_screen = "game_screen"
                            self.display()
                        elif self.current_screen == "end_screen":
                            self.current_screen = "init_screen"
                            self.display()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                run = False

            if self.current_screen == "game_screen":
                if keys[pygame.K_RIGHT]:
                    direction = "right"
                if keys[pygame.K_LEFT]:
                    direction = "left"
                if keys[pygame.K_UP]:
                    direction = "up"
                if keys[pygame.K_DOWN]:
                    direction = "down"

                if direction:
                    self.labyrinthe.player.move(direction)
                    self.display()

            if (
                self.labyrinthe.player.has_finished
                and self.current_screen == "game_screen"
            ):
                self.current_screen = "end_screen"
                self.display(has_won=self.labyrinthe.player.has_won)

            self.clock.tick(20)

    def display(self, **kwargs):
        """ Display method """
        getattr(self, self.current_screen).display(**kwargs)

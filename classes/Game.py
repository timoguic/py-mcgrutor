import pygame
from classes.Labyrinthe import Labyrinthe
from classes.Screen import Screen

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
                
        while run:
            direction = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                        
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                run = False

            if self.current_screen == 'init_screen':
                if keys:
                    self.current_screen = 'game_screen'
            
            if self.current_screen == 'end_screen':
                if keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
                    self.current_screen = 'init_screen'
                    self.labyrinthe = Labyrinthe()

            if self.current_screen == 'game_screen':
                if keys[pygame.K_RIGHT]:
                    direction = 'right'
                if keys[pygame.K_LEFT]:
                    direction = 'left'
                if keys[pygame.K_UP]:
                    direction = 'up'
                if keys[pygame.K_DOWN]:
                    direction = 'down'
            
            if direction:
                self.labyrinthe.player.move(direction)
                    
            if self.labyrinthe.player.has_finished:
                self.current_screen = 'end_screen'
                if self.labyrinthe.player.has_won:
                    self.display(red=0, green=0, blue=255)
                else:
                    self.display(red=255, green=0, blue=255)
            else:                         
                self.display()

            self.clock.tick(20)

    def display(self, **kwargs):
        getattr(self, self.current_screen).display(**kwargs)
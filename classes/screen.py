""" Module for screen management """

from random import randint
from pygame.font import Font
from pygame import Surface, gfxdraw
from pygame.display import flip as display_flip

class Screen:
    """ Screen class """
    def __init__(self, window, my_type, sprite_size=15, labyrinthe=None):
        """ Constructor """
        self.window = window
        self.type = my_type
        self.sprite_size = sprite_size
        self.never_displayed = True

        if labyrinthe:
            self.labyrinthe = labyrinthe

    def display(self, **kwargs):
        """ Display """
        if self.type == 'init_screen':
            self.display_init(**kwargs)
        elif self.type == 'end_screen':
            self.display_end(**kwargs)
        elif self.type == 'game_screen':
            self.display_game(**kwargs)

        display_flip()

    def display_game(self):
        """ Display game """
        sprite_size = self.sprite_size
        myfont = Font(None, int(sprite_size * 1.2))

        for index, line in enumerate(self.labyrinthe.level):
            for col, symbol in enumerate(line):
                elem = Surface((sprite_size, sprite_size))

                if symbol == 'X':
                    elem.fill([0, 0, 0])
                    self.window.blit(elem, (col*sprite_size, index*sprite_size))
                elif symbol == 'B':
                    elem.fill([255, 255, 255])
                    gfxdraw.aacircle(elem, sprite_size//2, sprite_size//2, \
                      sprite_size//2 - 3, [255, 0, 0])
                    gfxdraw.filled_circle(elem, sprite_size//2, sprite_size//2, \
                      sprite_size//2 - 3, [255, 0, 0])
                    self.window.blit(elem, (col*sprite_size, index*sprite_size))
                elif symbol == 'M':
                    elem.fill([255, 255, 255])
                    gfxdraw.aacircle(elem, sprite_size//2, sprite_size//2, \
                      sprite_size//2 - 3, [0, 0, 0])
                    gfxdraw.filled_circle(elem, sprite_size//2, sprite_size//2, \
                      sprite_size//2 - 3, [0, 0, 0])
                    self.window.blit(elem, (col*sprite_size, index*sprite_size))
                elif symbol.isdigit() and int(symbol) > 0:
                    #if self.never_displayed:
                    for i in range(0, sprite_size):
                        for j in range(0, sprite_size):
                            pixel = Surface((1, 1))
                            pixel.fill([randint(50, 100), randint(150, 250), randint(0, 50)])
                            elem.blit(pixel, (i, j))
                    self.window.blit(elem, (col*sprite_size, index*sprite_size))
                elif symbol == ' ':
                    elem.fill([255, 255, 255])
                    self.window.blit(elem, (col*sprite_size, index*sprite_size))

        self.never_displayed = False
        footer = Surface(((self.labyrinthe.num_cols-5)*sprite_size, sprite_size))
        footer.fill([0, 0, 0])

        for i in self.labyrinthe.player.items:
            gfxdraw.aacircle(footer, int(i)*sprite_size, \
              sprite_size//2, sprite_size//2 - 1, [255, 255, 255])
            gfxdraw.filled_circle(footer, int(i)*sprite_size, \
              sprite_size//2, sprite_size//2 - 1, [255, 255, 255])
            txt_surface = myfont.render(i, 1, (0, 0, 0))
            txt_size = myfont.size(i)
            footer.blit(txt_surface, \
              (int(i)*sprite_size-(txt_size[0]//2), (sprite_size-txt_size[1])//2 +1))

        self.window.blit(footer, (0, (self.labyrinthe.num_lines-1)*sprite_size))

    def display_init(self):
        """ Init display """
        self.window.fill([0, 0, 255])

    def display_end(self):
        """ End display """
        self.window.fill([0, 255, 0])

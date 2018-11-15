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

    def display_wall(self, elem):
        elem.fill([0, 0, 0])

    def display_boss(self, elem):
        elem.fill([255, 255, 255])
        
        gfxdraw.aacircle(elem, self.sprite_size//2, self.sprite_size//2, \
            self.sprite_size//2 - 3, [255, 0, 0])
        gfxdraw.filled_circle(elem, self.sprite_size//2, self.sprite_size//2, \
            self.sprite_size//2 - 3, [255, 0, 0])

    def display_player(self, elem):
        elem.fill([255, 255, 255])
        gfxdraw.aacircle(elem, self.sprite_size//2, self.sprite_size//2, \
            self.sprite_size//2 - 3, [0, 0, 0])
        gfxdraw.filled_circle(elem, self.sprite_size//2, self.sprite_size//2, \
            self.sprite_size//2 - 3, [0, 0, 0])
    
    def display_path(self, elem):
        elem.fill([200, 255, 200])

    def display_object(self, item, elem):
        if self.never_displayed:
            for i in range(0, self.sprite_size):
                for j in range(0, self.sprite_size):
                    pixel = Surface((1, 1))
                    pixel.fill([randint(50, 100), randint(150, 250), randint(0, 50)])
                    elem.blit(pixel, (i, j))

    def display_empty(self, elem):
        elem.fill([255, 255, 255])

    def display_game(self):
        """ Display game """
        for idx_l, line in enumerate(self.labyrinthe.level):
            for idx_col, elm in enumerate(line):
                if elm == '^':
                    self.labyrinthe.level[idx_l][idx_col] = ' '
        
        self.labyrinthe.pathfinder.create_path(
            (self.labyrinthe.player.line, self.labyrinthe.player.column),
            (10, 10),
            self.labyrinthe
        )

        sprite_size = self.sprite_size
        myfont = Font(None, int(sprite_size * 1.2))

        for index, line in enumerate(self.labyrinthe.level):
            for col, symbol in enumerate(line):
                elem = Surface((sprite_size, sprite_size))

                if symbol == '|':
                    self.display_wall(elem)
                elif symbol == 'B':
                    self.display_boss(elem)
                elif symbol == 'M':
                    self.display_player(elem)
                elif symbol == '^':
                    self.display_path(elem)
                elif symbol.isdigit() and int(symbol) > 0:
                    self.display_object(symbol, elem)
                elif symbol == ' ':
                    self.display_empty(elem)

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
        print(self.window)
        self.window.fill([255, 30, 30])
        myfont = Font(None, 36)
        intro_text = 'Press <space> to continue...'
        print(intro_text)
        
        txt_size = myfont.size(intro_text)
        txt_surface = myfont.render(intro_text, 1, [255, 255, 255])

        self.window.blit(txt_surface, ((self.window.get_width()-txt_size[0])//2, (self.window.get_height()-txt_size[1])//2))

    def display_end(self, has_won=False):
        """ End display """

        if has_won:
            end_text = "Well done, captain!"
            self.window.fill([0, 200, 200])
            txt_color = [0, 0, 0]
            self.display_centered_text(end_text, txt_color, 36, y_offset=-1)
        else:
            end_text = "Loser >__<"
            self.window.fill([200, 30, 30])
            txt_color = [0, 50, 50]
            self.display_centered_text(end_text, txt_color, 36, y_offset=-1)

        end_text = 'Press <space> to continue...'
        self.display_centered_text(end_text, txt_color, 36, y_offset=1)

    def display_centered_text(self, txt, color, size, y_offset=0):
        myfont = Font(None, size)
        txt_size = myfont.size(txt)
        txt_surface = myfont.render(txt, 1, color)
        pos_x = (self.window.get_width()-txt_size[0])//2
        pos_y = (self.window.get_height()-txt_size[1])//2 + (y_offset*size)

        self.window.blit(txt_surface, (pos_x, pos_y))
        

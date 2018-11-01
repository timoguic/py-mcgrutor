from pygame.display import flip as display_flip
from pygame.font import Font
from pygame import Surface, gfxdraw
from random import randint

class Screen:
    def __init__(self, window, type, sprite_size=15, labyrinthe=None):
        self.window = window
        self.type = type
        self.sprite_size = sprite_size

        if labyrinthe:
            self.labyrinthe = labyrinthe

    def display(self, **kwargs):
        if self.type == 'init_screen':
            self.display_init(**kwargs)
        elif self.type == 'end_screen':
            self.display_end(**kwargs)
        elif self.type == 'game_screen':
            self.display_game(**kwargs)

        display_flip()

    def display_game(self, **kwargs):
        sprite_size = self.sprite_size
        myfont = Font(None, int(sprite_size * 1.2))

        for index, line in enumerate(self.labyrinthe.level):
            for col, symbol in enumerate(line):
                elem = Surface((sprite_size, sprite_size))
                elem.fill([255, 255, 255])
                if symbol == 'X':
                    elem.fill([0, 0, 0])
                elif symbol == 'B':
                    gfxdraw.aacircle(elem, sprite_size//2, sprite_size//2, sprite_size//2 - 3, [255, 0, 0])
                    gfxdraw.filled_circle(elem, sprite_size//2, sprite_size//2, sprite_size//2 - 3, [255, 0, 0])
                elif symbol == 'M':
                    gfxdraw.aacircle(elem, sprite_size//2, sprite_size//2, sprite_size//2 - 3, [0, 0, 0])
                    gfxdraw.filled_circle(elem, sprite_size//2, sprite_size//2, sprite_size//2 - 3, [0, 0, 0])
                elif symbol.isdigit():
                    for i in range(0, sprite_size):
                        for j in range(0, sprite_size):
                            pixel = Surface((1,1))
                            pixel.fill([randint(0, 255), randint(0, 255), randint(0, 255)])
                            elem.blit(pixel, (i, j))

                    #elem.fill([0, 150, 0])
                    #txt = myfont.render(symbol, 1, (255, 255, 255))
                    ##size_x, size_y = myfont.size(symbol)
                    #offset_1 = (sprite_size - size_x) // 2
                    #offset_2 = (sprite_size - size_y) // 2 + 1
                    #elem.blit(txt, (offset_1, offset_2))

                self.window.blit(elem, (col*sprite_size, index*sprite_size))

        footer = Surface(((self.labyrinthe.num_cols-5)*sprite_size, sprite_size))

        for i in self.labyrinthe.player.items:
            gfxdraw.aacircle(footer, int(i)*sprite_size, sprite_size//2, sprite_size//2 - 1, [255, 255,255])     
            gfxdraw.filled_circle(footer, int(i)*sprite_size, sprite_size//2, sprite_size//2 - 1, [255, 255,255])     
            txt_surface = myfont.render(i, 1, (0, 0, 0))
            txt_size = myfont.size(i)
            footer.blit(txt_surface, (int(i)*sprite_size-(txt_size[0]//2), (sprite_size-txt_size[1])//2 +1))

        self.window.blit(footer, (0, (self.labyrinthe.num_lines-1)*sprite_size))
            
    def display_init(self, **kwargs):
        self.window.fill([0, 0, 255])

    def display_end(self, **kwargs):
        self.window.fill([0, 255, 0])
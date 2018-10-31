import sys
import configparser
import pygame
from classes.Game import Game

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    pygame.key.set_repeat(0, 100)

    config = configparser.ConfigParser()
    config.read('mcgyver.conf')

    if not 'McGyver' in config.sections():
        print('Please check your config file.')
        sys.exit(-1)
    else:
        lines = int(config['McGyver'].get('height'))
        cols = int(config['McGyver'].get('width'))
        sprite_size = int(config['McGyver'].get('sprite_size'))
        num_objects = int(config['McGyver'].get('num_objects'))

        window = pygame.display.set_mode((cols*sprite_size, lines*sprite_size))

        game = Game(window, cols=cols, lines=lines, num_objects=num_objects, sprite_size=sprite_size)
        game.run()
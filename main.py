""" MAIN PROGRAM FOR MCGYVER MAZE """

import sys
import configparser
import pygame
from classes.game import Game

def main():
    """ Main function """
    pygame.init()
    pygame.font.init()

    config = configparser.ConfigParser()
    config.read('mcgyver.conf')

    if 'McGyver' not in config.sections():
        print('Please check your config file.')
        sys.exit(-1)
    else:
        lines = int(config['McGyver'].get('height'))
        cols = int(config['McGyver'].get('width'))
        sprite_size = int(config['McGyver'].get('sprite_size'))
        num_objects = int(config['McGyver'].get('num_objects'))

        window = pygame.display.set_mode(((cols+1)*sprite_size, (lines+1)*sprite_size))

        game = Game(window, cols=cols, lines=lines, \
            num_objects=num_objects, sprite_size=sprite_size)
        game.run()

if __name__ == '__main__':
    main()

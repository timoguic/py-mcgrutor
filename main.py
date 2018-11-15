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
        my_conf = config['McGyver']
        lines = int(my_conf.get('height'))
        cols = int(my_conf.get('width'))
        sprite_size = int(my_conf.get('sprite_size'))
        num_objects = int(my_conf.get('num_objects'))
        density = float(my_conf.get('density'))
        complexity = float(my_conf.get('complexity'))

        window = pygame.display.set_mode(((cols+1)*sprite_size, (lines+1)*sprite_size))

        game = Game(window, cols=cols, lines=lines, \
            num_objects=num_objects, sprite_size=sprite_size, density=density, complexity=complexity)
        game.run()

if __name__ == '__main__':
    main()

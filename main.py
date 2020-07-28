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
    config.read("mcgyver.conf")

    if "McGyver" not in config.sections():
        print("Please check your config file.")
        sys.exit(-1)
    else:
        my_conf = config["McGyver"]
        defaults = {
            "lines": 15,
            "cols": 15,
            "sprite_size": 20,
            "num_objects": 5,
            "density": 0.75,
            "complexity": 0.5,
        }

        for key, default_value in defaults.items():
            value = my_conf.get(key)
            if not value:
                continue

            value_type = type(default_value)
            defaults[key] = value_type(value)

        window_size = (
            (defaults["lines"]+1) * defaults["sprite_size"],
            (defaults["cols"]+1) * defaults["sprite_size"],
        )
        window = pygame.display.set_mode(window_size)

        game = Game(window, **defaults)
        game.run()


if __name__ == "__main__":
    main()

# py-mcgrutor
Demo maze game (OpenClassrooms educational project).

* You are the black dot.
* You move around with the arrow keys.
* You need to collect all green dots, and exit the maze (red dot).

The maze is automatically generated. Items are randomly created and placed in the maze.

## Configuration

You can change values in `mcgyver.conf`:
* `LINES`, `COLS`: dimension of the grid
* `SPRITE_SIZE`: dimensions of a square sprite (in pixels)
* `NUM_OBJECTS`: number of objects to collect
* `COMPLEXITY` and `DENSITY`: affect the maze pattern

## Install and run
* create a virtual environment: `python -m venv venv && source venv/bin/activate`
* install dependencies: `pip install -r requirements.txt`
* run the game: `python main.py`
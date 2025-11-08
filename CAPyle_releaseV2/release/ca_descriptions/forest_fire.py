# Name: Forest Fire simulation
# Dimensions: 2

# --- Set up executable path, do not edit ---
import sys
import inspect
this_file_loc = (inspect.stack()[0][1])
main_dir_loc = this_file_loc[:this_file_loc.index('ca_descriptions')]
sys.path.append(main_dir_loc)
sys.path.append(main_dir_loc + 'capyle')
sys.path.append(main_dir_loc + 'capyle/ca')
sys.path.append(main_dir_loc + 'capyle/guicomponents')
# ---

from capyle.ca import Grid2D, Neighbourhood, CAConfig, randomise2d
import capyle.utils as utils
import numpy as np

from enum import Enum

class Tile(Enum):
    LAKE = 0
    
    CHAPARREL = 1
    FOREST    = 2
    SCRUB     = 3

    CHAPARREL_BURNING = 4
    FOREST_BURNING    = 5
    SCRUB_BURNING     = 6

    CHAPARREL_BURNT   = 7
    FOREST_BURNT      = 8
    SCRUB_BURNT       = 9

    def burn(s):
        return s + 3

colours = {
        Tile.LAKE         : (0.239, 0.69, 0.941),
        Tile.CHAPARREL    : (0.749, 0.749, 0),
        Tile.FOREST       : (0.31, 0.384, 0.153),
        Tile.SCRUB        : (0.996, 1, 0)
    }
    
def make_other_colours():
    for i in range(1,4):
        # remove the green from on_fire tiles to make them look onfireyer (custom colours would be better)
        colours[Tile(i+3)] = (colours[Tile(i)][0], 0, colours[Tile(i)][2])
        # darken tiles to make them look burnt out
        colours[Tile(i+6)] = tuple([c * 0.25 for c in colours[Tile(i)]])


def transition_func(grid, neighbourstates, neighbourcounts):
    # dead = state == 0, live = state == 1
    # unpack state counts for state 0 and state 1
    dead_neighbours, live_neighbours = neighbourcounts
    # create boolean arrays for the birth & survival rules
    # if 3 live neighbours and is dead -> cell born
    birth = (live_neighbours == 3) & (grid == 0)
    # if 2 or 3 live neighbours and is alive -> survives
    survive = ((live_neighbours == 2) | (live_neighbours == 3)) & (grid == 1)
    # Set all cells to 0 (dead)
    grid[:, :] = 0
    # Set cells to 1 where either cell is born or survives
    grid[birth | survive] = 1
    return grid


def setup(args):
    config_path = args[0]
    config = utils.load(config_path)
    # ---THE CA MUST BE RELOADED IN THE GUI IF ANY OF THE BELOW ARE CHANGED---
    config.title = "Conway's game of life"
    config.dimensions = 2
    config.states = tuple([s.value for s in Tile])
    # ------------------------------------------------------------------------

    # ---- Override the defaults below (these may be changed at anytime) ----

    make_other_colours()
    config.state_colors = list(colours.values())
    # config.num_generations = 150
    # config.grid_dims = (200,200)

    # ----------------------------------------------------------------------

    if len(args) == 2:
        config.save()
        sys.exit()

    return config


def main():
    # Open the config object
    config = setup(sys.argv[1:])

    # Create grid object
    grid = Grid2D(config, transition_func)

    # Run the CA, save grid state every generation to timeline
    timeline = grid.run()

    # save updated config to file
    config.save()
    # save timeline to file
    utils.save(timeline, config.timeline_path)


if __name__ == "__main__":
    main()

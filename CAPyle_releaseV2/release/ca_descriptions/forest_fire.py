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

import random
from enum import IntEnum

# IntEnums compare to Ints, i.e. Tile.LAKE == 0
class Tile(IntEnum):
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

    def ignite(s):
        return s + 3

    def flammable(t):
        return t == CHAPARREL or t == FOREST or t == SCRUB

colours = {
        Tile.LAKE         : (0.239, 0.69, 0.941),
        Tile.CHAPARREL    : (0.749, 0.749, 0),
        Tile.FOREST       : (0.31, 0.384, 0.153),
        Tile.SCRUB        : (0.996, 1, 0)
    }

# flammability affects how easily a terrain type catches
# higher is more flammable
flammability = {
    Tile.CHAPARREL  : 0.2,
    Tile.FOREST     : 0.05,
    Tile.SCRUB      : 1
}    

# extinguishing factor affects how long a terrain type burns
# higher is more likely to go out
extinguishing_factor = {
    Tile.CHAPARREL_BURNING : 1/24,
    Tile.FOREST_BURNING    : 1/72,
    Tile.SCRUB_BURNING     : 1
}
    
def make_other_colours():
    for i in range(1,4):
        # remove the green from on_fire tiles to make them look onfireyer (custom colours would be better)
        colours[Tile(i+3)] = (colours[Tile(i)][0], 0, colours[Tile(i)][2])
        # darken tiles to make them look burnt out
        colours[Tile(i+6)] = tuple([c * 0.25 for c in colours[Tile(i)]])

def transition_func(grid, neighbourstates, neighbourcounts):
    
    # mask 1: lake tiles remain lake
    # we are going to note down the lake tiles at the start so we dont have to worry about them while we BURN
    lake = (grid == Tile.LAKE)

    # set tiles on fire
    # get a map of how many burning neighbours each grid square has
    burning_neighbour_count = np.add(
        np.add(neighbourcounts[Tile.CHAPARREL_BURNING], neighbourcounts[Tile.FOREST_BURNING]),
        neighbourcounts[Tile.SCRUB_BURNING])
    print(f"{burning_neighbour_count=}")
    # multiply each tile by a random 0..1, 
    c = np.multiply(burning_neighbour_count, np.random.rand(*burning_neighbour_count.shape))

    # all tiles where the resulting value is below the threshold probability are to be set on fire
    for (t, f) in flammability.items(): 
        grid = np.where((grid == t) & (c > 0) & (c < f), Tile.ignite(t), grid)

    # put the lakes back
    grid[lake] = Tile.LAKE
    return grid


def setup(args):
    config_path = args[0]
    config = utils.load(config_path)
    # ---THE CA MUST BE RELOADED IN THE GUI IF ANY OF THE BELOW ARE CHANGED---
    config.title = "🔥🔥🔥"
    config.dimensions = 2
    config.states = tuple([s.value for s in Tile])
    # ------------------------------------------------------------------------

    # ---- Override the defaults below (these may be changed at anytime) ----

    make_other_colours()
    config.state_colors = list(colours.values())
    # config.num_generations = 150
    config.grid_dims = (10,10)

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

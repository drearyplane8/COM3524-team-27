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

import map

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

    TOWN              = 10
    DUMMY             = 11
    DUMMY_2           = 12
    TOWN_BURNING      = 13
    DUMMY_3           = 14
    DUMMY_4           = 15
    TOWN_BURNT        = 16

    def ignite(s):
        return s + 3 

    def extinguish(s):
        return s + 3 

# need not be a dict but it makes it more explicit
colours = {
        Tile.LAKE              : (0.239, 0.69, 0.941),
        Tile.CHAPARREL         : (0.749, 0.749, 0),
        Tile.FOREST            : (0.31, 0.384, 0.153),
        Tile.SCRUB             : (0.996, 1, 0),
        Tile.CHAPARREL_BURNING : (0.8, 0.36, 0),
        Tile.FOREST_BURNING    : (0.769, 0.149, 0.024),
        Tile.SCRUB_BURNING     : (1, 0.753, 0),
        Tile.CHAPARREL_BURNT   : (0.633, 0.576, 0.525),
        Tile.FOREST_BURNT      : (0.267, 0.271, 0.259),
        Tile.SCRUB_BURNT       : (0.435, 0.4, 0.294),
        Tile.TOWN              : (0,0,0),
        11                     : (1,1,1),
        12                     : (1,1,1),
        Tile.TOWN_BURNING      : (1,0,0),
        14                     : (1,1,1),
        15                     : (1,1,1),
        Tile.TOWN_BURNT        : (0.5, 0.5, 0.5)
    }

# flammability affects how easily a terrain type catches
# higher is more flammable
flammability = {
    Tile.CHAPARREL  : 0.2,
    Tile.FOREST     : 0.025,
    Tile.SCRUB      : 1,
    Tile.TOWN       : 1
}    

# extinguishing factor affects how long a terrain type burns
# higher is more likely to go out
extinguishing_factor = {
    Tile.CHAPARREL_BURNING : 1/48,
    Tile.FOREST_BURNING    : 1/90,
    Tile.SCRUB_BURNING     : 0.5,
    Tile.TOWN_BURNING      : 0.5
}
    

def transition_func(grid, neighbourstates, neighbourcounts):

    # Record lake tiles
    lake = (grid == Tile.LAKE)

    # Extinguish burning tiles according to their type
    extinguish_noise = np.random.rand(*grid.shape) # if we're having performance issues, we could consider using the same noise as for burning
    for (t, e) in extinguishing_factor.items():
        extinguish = (grid == t) & (extinguish_noise < e)
        grid[extinguish] = Tile.extinguish(t)



    # Light tiles on fire according to their burning neighbour #, type

    # get a map of how many burning neighbours each grid square has
    burning_neighbour_count = neighbourcounts[Tile.CHAPARREL_BURNING] + neighbourcounts[Tile.FOREST_BURNING] + neighbourcounts[Tile.SCRUB_BURNING] + neighbourcounts[Tile.TOWN_BURNING]
    # multiply each tile by a random 0..1, 
    c = np.multiply(burning_neighbour_count, np.random.rand(*grid.shape))

    # all tiles where the resulting value is below the threshold probability are to be set on fire
    for (t, f) in flammability.items(): 
        alight = (grid == t) & (c > 0) & (c < flammability[t]) # make sure tiles with 0 burning neighbours are not lit
        grid[alight] = Tile.ignite(t)

    # Put the lakes back        
    grid[lake] = Tile.LAKE
    return grid


def scale(map, sf):
    return map.repeat(sf, axis=0).repeat(sf, axis=1)

def setup(args):
    # pre-given stuff - dont change
    config_path = args[0]
    config = utils.load(config_path)

    # basic config
    config.title = "🔥🔥🔥"
    config.dimensions = 2

    #set states and colours
    config.states = tuple([s.value for s in Tile])
    config.state_colors = list(colours.values())
    
    # disable wrap 
    config.wrap = False

    # set fire starting points:
    POWER_PLANT = True
    INCINERATOR = True
    TOWN = True

    # set grid and appropriate size
    sf = 4 
    scaled_map = scale(map.map, sf)

    if INCINERATOR:
        scaled_map[0][-1] = Tile.ignite(scaled_map[0][-1]) 
    if POWER_PLANT:
        scaled_map[0][2 * sf] = Tile.ignite(scaled_map[0][2 * sf])
    if TOWN and sf >= 2 and sf % 2 == 0: # sf necessary to represent town as an area target
        scaled_map[-2*sf : int(-1.5*sf), int(5.5*sf) : 6*sf] = Tile.TOWN


    shape = np.shape(map.map)
    config.set_initial_grid(scaled_map)
    config.set_grid_dims(
        (shape[0] * sf, shape[1]* sf))

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

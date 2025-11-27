# COM 3524 – System Tools

This repository is a fork of the original COM3524 repo, with all the other tools removed, and our forest fire CA added.

---

## Prerequisites
Before starting, ensure the following softwares and tools are installed on your machine:

- [Python 3.8+](https://www.python.org/downloads/)
- `pip` (Python package manager for installing necessary dependencies)

Firstly, please install all required packages. This tool does not use any packages that CAPyle doesn't use by default. 

## Running

Run `python run_tool.py` in the repository root. This will not open a menu; it will launch CAPyle automatically. Once it launches, use the dialog to open forest_fire.py, and press "Apply Configuration and Run CA".

Only the # of generations is modifiable in the GUI — dimensions and grid are both set in the setup function. We recommend a limit of 200 generations at `sf = 1`, 300 at `sf = 2`, and 500 at `sf = 4` for reasonable runtimes, but there are no hard limits.


## Changing Parameters

Change the `sf` variable in `setup()` in order to change the scale the grid is represented at. Only positive integer values are supported.

Changing `sf` will not modify any of the transition rules, so generation counts are *not* comparable across grid scales. 

Change the `WIND_DIR` and `WIND_SPEED_MULT` variables above `transition_func(...)` to change the wind direction or speed. `WIND_DIR` takes values from the `Wind` enum, corresponding to the eight cardinal and intercardinal directions, although currently only the cardinals are supported.

Change the `POWER_PLANT`, `INCINERATOR`, and `TOWN` variables in `setup()` to control whether those POIs are shown on the map. The Town can only be displayed when `sf` is even and greater than one. 

## Changing the Grid

Due to CAPyle's limitations, the integrated grid editor will not work when a grid is pre-loaded. Therefore, if you wish to change the grid, i.e. to start a fire in a different location, you must do so manually. This can be done by editing `CAPyle_releaseV2/release/ca_descriptions/map.py`, which includes the map as an array literal in the lowest resolution that can accurately display the map given in the brief: each array element represents a 2.5kmx2.5km square. The values are tile values from the `Tile` enum.
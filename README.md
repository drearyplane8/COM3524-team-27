# COM 3524 – System Tools

This repository is a fork of the original COM3524 repo, with all the other tools removed, and our forest fire CA added.

## Features

- Cross-platform support (Linux, macOS, Windows)

---
## Prerequisites
Before starting, ensure the following softwares and tools are installed on your machine:

- [Python 3.8+](https://www.python.org/downloads/)
- `pip` (Python package manager for installing necessary dependencies)

Firstly, please install all required packages. This tool does not use any packages that CAPyle doesn't use by default. 

## Running

Run `python run_tool.py` in the repository root. Once it launches, use the dialog to open forest_fire.py, and press "Apply Configuration and Run CA".

Only the # of generations is modifiable — dimensions and grid are both set in the setup function.

## Changing Parameters

Change the `sf` variable in `setup()` in order to change the scale the grid is represented at. Only positive integer values are supported, and only even values greater than 2 will display the town on the grid.

Changing `sf` will *not* modify any of the transition rules, so generation counts are not comparable across grid scales. 

Change the `WIND_DIR` and `WIND_SPEED_MULT` variables above `transition_func(...)` to change the wind direction or speed. `WIND_DIR` takes values from the `Wind` enum, corresponding to the eight cardinal and intercardinal directions, although currently only the cardinals are supported.
from __future__ import annotations

from minigrid.core.world_object import Lava, Goal
from minigrid.core.grid import Grid

from minigrid_json.grid_json import GridJson


if __name__ == "__main__":
    print("Creating a grid.")
    WIDTH = 50
    HEIGHT = 50

    grid = Grid(WIDTH, HEIGHT)
    grid.wall_rect(0, 0, WIDTH, HEIGHT)

    grid.set(12, 31, Lava())
    grid.set(12, 32, Lava())
    grid.set(2, 2, Lava())
    grid.set(12, 19, Lava())
    grid.set(25, 25, Goal())

    print("Exporting the Grid as a JSON file.")
    GridJson.export(grid, "desc.json", "simple_env")

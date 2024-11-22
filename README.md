# Minigrid JSON
A portable representation of Minigrid environments.

## Quick Usage

This package provides two main capabilities: exporting and loading Minigrid grids. In either case,
first import the `GridJson` class.
```
from minigrid_json.grid_json import GridJson
```

1. To export a grid, add the following code to your Minigrid (sub)class:
```
def export(self, description_path: str, env_name: str = "random"):
    GridJson.export(grid, description_path, env_name)
```

Here, `description_path` is the complete path (including the JSON file name) where 
you would like to save the file and `env_name` is the name of the environment.

2. To load a grid, add the following code to your Minigrid (sub)class:
```
def _gen_grid(self, width: int | None = None, height: int | None = None) -> Grid:
    self.grid = GridJson.load(self.description_path, grid_fn=Grid)

    # The rest of the typical _gen_grid code.
```
Here, `_gen_grid` is similar to the original generate grid function. However, we ignore
the width and height arguments since the description stores the width and height. The load
function will place all world objects that were in the grid when it was saved.

For more detailed usage, please look at the scripts in the `tests` directory.


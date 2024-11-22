from __future__ import annotations
import copy
import json
import os
from typing import Any, Callable

from minigrid.core.grid import Grid
from minigrid.core.world_object import (
    WorldObj,
    Goal,
    Floor,
    Lava,
    Wall,
    Door,
    Key,
    Ball,
    Box,
)

from minigrid_json.description import (
    GridEnvDesc,
    GridObjectDesc,
    GridPositionDesc,
)


DEFAULT_OBJECT_DICT = {
    "goal": Goal(),
    "floor": Floor(),
    "lava": Lava(),
    "wall": Wall(),
    "door": Door("yellow"),
    "key": Key(),
    "ball": Ball(),
    "box": Box("red"),
}


class GridJson:

    @staticmethod
    def load(
        description_path: str,
        grid_fn: Callable[[int, int, Any], Grid],
        grid_fn_options: dict[str, Any] = dict(),
        object_dict: dict[str, WorldObj] = DEFAULT_OBJECT_DICT,
    ) -> Grid | None:
        if not os.path.exists(description_path):
            raise FileNotFoundError(f"Description not found: {description_path}")

        with open(description_path, mode="r") as fp:
            desc_dict: dict[str, Any] = json.load(fp)

        if len(desc_dict) == 0:
            print("WARNING: No environment information was found.")
            return None

        # Generate the description and the resulting grid.
        description = GridEnvDesc.create(desc_dict)
        grid: Grid = grid_fn(
            width=description.width, height=description.height, **grid_fn_options
        )

        # grid.wall_rect(0, 0, description.width, description.height)
        for obj in description.objects:

            object_instance = object_dict.get(obj.name, None)
            if object_instance is None:
                raise ValueError(f"Object {obj.name} does not exist!")

            for pos in obj.positions:
                grid.set(i=pos.x, j=pos.y, v=copy.deepcopy(object_instance))

        return grid

    @staticmethod
    def export(
        grid: Grid,
        description_path: str,
        env_name: str = "unknown",
    ) -> None:
        description = GridJson.convert_grid_to_description(grid=grid, env_name=env_name)
        GridJson.export_description(
            description=description, description_path=description_path
        )

    @staticmethod
    def convert_grid_to_description(
        grid: Grid, env_name: str = "unknown"
    ) -> GridEnvDesc:
        object_dict: dict[str, GridObjectDesc] = dict()
        for x in range(grid.width):
            for y in range(grid.height):
                if (obj := grid.get(x, y)) is not None:
                    if obj.type not in object_dict:
                        object_dict[obj.type] = GridObjectDesc(
                            name=obj.type, positions=list()
                        )
                    object_dict[obj.type].positions.append(GridPositionDesc(x=x, y=y))

        description = GridEnvDesc(
            name=env_name,
            width=grid.width,
            height=grid.height,
            objects=list(object_dict.values()),
        )
        return description

    @staticmethod
    def export_description(description: GridEnvDesc, description_path: str) -> None:
        if os.path.exists(description_path):
            raise FileExistsError

        with open(description_path, mode="w") as fp:
            json.dump(description.export(), fp, indent=4)

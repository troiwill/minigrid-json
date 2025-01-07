from __future__ import annotations
import copy
import json
import os
from typing import Any, Callable

from minigrid.core.constants import IDX_TO_OBJECT
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
    WorldObjectDescriptor,
)


class GridJson:

    @staticmethod
    def load(
        description_path: str,
        grid_fn: Callable[[int, int, Any], Grid],
        grid_fn_options: dict[str, Any] = dict(),
        object_dict: dict[int, WorldObj] = dict(),
    ) -> Grid:
        """
        Loads a grid from a JSON description file.

        Args:
            description_path (str): Path to the JSON description file.
            grid_fn (Callable[[int, int, Any], Grid]): Function to create the grid.
            grid_fn_options (dict[str, Any], optional): Additional options for grid_fn. Defaults to an empty dict.
            object_dict (dict[int, WorldObj], optional): Dictionary mapping object IDs to WorldObj classes. Defaults to an empty dict.

        Returns:
            Grid: The loaded grid.

        Raises:
            FileNotFoundError: If the description file is not found.
            ValueError: If the description is empty or an object in the description doesn't exist in the object_dict.
        """
        if not os.path.exists(description_path):
            raise FileNotFoundError(f"Description not found: {description_path}")

        with open(description_path, mode="r") as fp:
            desc_dict: dict[str, Any] = json.load(fp)

        if len(desc_dict) == 0:
            raise ValueError("No environment information was found.")

        # Generate the description and the resulting grid.
        env_desc = GridEnvDesc.create(desc_dict)
        grid: Grid = grid_fn(
            width=env_desc.width, height=env_desc.height, **grid_fn_options
        )

        for obj in env_desc.objects:
            # Determine if there is a decoder for the given object.
            obj_type: int = obj.descriptor[0]
            obj_decoder = object_dict.get(obj_type, WorldObj)

            # Decode the object given the descriptor.
            object_instance = obj_decoder.decode(*obj.descriptor)

            # Add the object at the given positions.
            for pos in obj.positions:
                grid.set(i=pos.x, j=pos.y, v=copy.deepcopy(object_instance))

        return grid

    @staticmethod
    def export(
        grid: Grid,
        description_path: str,
        env_name: str = "unknown",
    ) -> None:
        """
        Exports a given grid to a JSON description file.

        Args:
            grid (Grid): The grid to export.
            description_path (str): Path where the JSON description will be saved.
            env_name (str, optional): Name of the environment. Defaults to "unknown".

        Raises:
            FileExistsError: If the description_path already exists.
        """
        # Create the description.
        description = GridJson.convert_grid_to_description(grid=grid, env_name=env_name)

        # Save the description to disk.
        GridJson.export_description(
            description=description, description_path=description_path
        )

    @staticmethod
    def convert_grid_to_description(
        grid: Grid, env_name: str = "unknown"
    ) -> GridEnvDesc:
        """
        Converts a Grid object to a GridEnvDesc object.

        Args:
            grid (Grid): The grid to convert.
            env_name (str, optional): Name of the environment. Defaults to "unknown".

        Returns:
            GridEnvDesc: A description of the grid environment.
        """
        # A dictionary mapping an object's encoded 3-tuple descriptor ->
        object_dict: dict[WorldObjectDescriptor, GridObjectDesc] = dict()

        # Iterate over all the cells within the Minigrid.
        for x in range(grid.width):
            for y in range(grid.height):
                # If there is an object at the cell (x, y), record it's information.
                if (obj := grid.get(x, y)) is not None:
                    # Init the dictionary with the descriptor if the descriptor does not exist.
                    descriptor = obj.encode()
                    if descriptor not in object_dict:
                        object_dict[descriptor] = GridObjectDesc(
                            descriptor=descriptor, positions=list()
                        )

                    # Add the position this object was at.
                    object_dict[descriptor].positions.append(GridPositionDesc(x=x, y=y))

        # Create a Grid description with all the world objects.
        description = GridEnvDesc(
            name=env_name,
            width=grid.width,
            height=grid.height,
            objects=list(object_dict.values()),
        )
        return description

    @staticmethod
    def export_description(description: GridEnvDesc, description_path: str) -> None:
        """
        Exports a GridEnvDesc object to a JSON file.

        Args:
            description (GridEnvDesc): The grid environment description to export.
            description_path (str): Path where the JSON description will be saved.

        Raises:
            FileExistsError: If the description_path already exists.
        """
        if os.path.exists(description_path):
            raise FileExistsError

        with open(description_path, mode="w") as fp:
            json.dump(description.export(), fp, indent=4)

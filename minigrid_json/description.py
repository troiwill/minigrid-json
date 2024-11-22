from __future__ import annotations
from collections import OrderedDict
from typing import Any

from pydantic import BaseModel, NonNegativeInt, PositiveInt


class GridPositionDesc(BaseModel):
    x: NonNegativeInt
    y: NonNegativeInt

    def export(self) -> dict[str, int]:
        return {"x": self.x, "y": self.y}

    @staticmethod
    def create(pos_desc: dict[str, int]) -> GridPositionDesc:
        return GridPositionDesc(**pos_desc)


class GridObjectDesc(BaseModel):
    name: str
    positions: list[GridPositionDesc]

    def export(self) -> dict[str, Any]:
        return OrderedDict(
            [
                ("name", self.name),
                ("positions", list(pos.export() for pos in self.positions)),
            ]
        )

    @staticmethod
    def create(obj_desc: dict[str, Any]) -> GridObjectDesc:
        obj_desc["positions"] = list(
            GridPositionDesc.create(pos_desc) for pos_desc in obj_desc["positions"]
        )
        return GridObjectDesc(**obj_desc)


class GridEnvDesc(BaseModel):
    name: str
    width: PositiveInt
    height: PositiveInt
    objects: list[GridObjectDesc]

    def export(self) -> dict[str, Any]:
        return OrderedDict(
            [
                ("name", self.name),
                ("width", self.width),
                ("height", self.height),
                ("objects", list(obj.export() for obj in self.objects)),
            ]
        )

    @staticmethod
    def create(env_desc: dict[str, Any]) -> GridEnvDesc:
        # Parse environment objects.
        env_desc["objects"] = list(
            GridObjectDesc.create(obj_desc) for obj_desc in env_desc["objects"]
        )
        return GridEnvDesc(**env_desc)

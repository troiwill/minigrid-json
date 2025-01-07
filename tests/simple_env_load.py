from __future__ import annotations
from typing import Any

from gymnasium.core import ObsType
from minigrid.core.grid import Grid
from minigrid.core.mission import MissionSpace
from minigrid.minigrid_env import MiniGridEnv

from minigrid_json.grid_json import GridJson


class SimpleTestEnv(MiniGridEnv):

    def __init__(
        self,
    ):
        super().__init__(
            mission_space=MissionSpace(SimpleTestEnv._gen_mission),
            width=50,
            height=50,
            render_mode="human",
        )

        self.grid: Grid
        self.start_pos = (4, 4)
        self.start_dir = 0

    def _gen_grid(self, width: int | None = None, height: int | None = None) -> None:
        self.grid = GridJson.load("desc.json", grid_fn=Grid)

        # Place the agent and set the mission.
        self._place_agent()
        self.mission = self._gen_mission()

    def _place_agent(self) -> None:
        if self.start_pos is not None:
            self.agent_pos = self.start_pos
            self.agent_dir = self.start_dir
        else:
            self.place_agent()

        self.mission = SimpleTestEnv._gen_mission()

    @staticmethod
    def _gen_mission():
        return "test mission"


if __name__ == "__main__":
    env = SimpleTestEnv()
    env.reset()
    env.render()
    _ = input("Press enter to exit.")

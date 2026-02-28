"""Runtime manager for NeuraEdge execution."""

import numpy as np
from typing import Dict, List, Optional


class RuntimeManager:
    """Manages runtime execution and scheduling."""

    def __init__(self, num_tiles: int):
        self.num_tiles = num_tiles
        self.task_queue = []
        self.completed_tasks = []
        self.current_time = 0.0
        self.power_state = [1.0] * num_tiles  # Power scaling per tile (0-1)

    def submit_task(self, task_config: Dict):
        """
        Submit execution task.

        Args:
            task_config: Task configuration dict
        """
        task = {
            "id": len(self.task_queue),
            "config": task_config,
            "status": "pending",
            "start_time": None,
            "end_time": None,
        }
        self.task_queue.append(task)

    def execute_task(self, task_id: int, executor) -> Dict:
        """
        Execute task on hardware.

        Args:
            task_id: Task ID
            executor: Execution function

        Returns:
            Task results
        """
        task = self.task_queue[task_id]
        task["status"] = "running"
        task["start_time"] = self.current_time

        try:
            result = executor(task["config"])
            task["status"] = "completed"
            task["result"] = result
        except Exception as e:
            task["status"] = "failed"
            task["error"] = str(e)
            result = None

        task["end_time"] = self.current_time
        self.completed_tasks.append(task)

        return result

    def set_power_state(self, tile_id: int, power_scaling: float):
        """
        Set power scaling for tile.

        Args:
            tile_id: Target tile
            power_scaling: Power scaling factor (0-1)
        """
        if tile_id < self.num_tiles:
            self.power_state[tile_id] = max(0.1, min(1.0, power_scaling))

    def advance_time(self, delta_t: float = 1.0):
        """Advance simulation time."""
        self.current_time += delta_t

    def get_execution_stats(self) -> Dict:
        """Get execution statistics."""
        completed = len([t for t in self.completed_tasks if t["status"] == "completed"])
        failed = len([t for t in self.completed_tasks if t["status"] == "failed"])

        return {
            "current_time": self.current_time,
            "tasks_completed": completed,
            "tasks_failed": failed,
            "power_states": self.power_state.copy(),
        }

    def reset(self):
        """Reset runtime manager."""
        self.task_queue = []
        self.completed_tasks = []
        self.current_time = 0.0
        self.power_state = [1.0] * self.num_tiles

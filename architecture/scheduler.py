"""
Scheduler for tile-level task execution.
"""

from typing import List, Dict
from dataclasses import dataclass


@dataclass
class Task:
    """Compute task for a tile."""

    task_id: int
    tile_id: int
    layer_id: int
    priority: int = 0


class TileScheduler:
    """Schedules compute tasks across tiles."""

    def __init__(self, num_tiles: int):
        self.num_tiles = num_tiles
        self.task_queue = []
        self.completed_tasks = []
        self.current_cycle = 0

    def enqueue_task(self, task: Task):
        """Add task to schedule."""
        self.task_queue.append(task)

    def get_next_task(self, tile_id: int) -> Task:
        """Get next task for tile."""
        for task in self.task_queue:
            if task.tile_id == tile_id:
                self.task_queue.remove(task)
                return task
        return None

    def mark_task_complete(self, task: Task):
        """Mark task as completed."""
        self.completed_tasks.append(task)

    def advance_cycle(self):
        """Advance scheduler cycle."""
        self.current_cycle += 1

    def is_idle(self) -> bool:
        """Check if all tasks complete."""
        return len(self.task_queue) == 0

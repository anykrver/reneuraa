"""
Arbitration schemes for multi-tile routing.
"""

from typing import List, Dict
from enum import Enum


class ArbitrationPolicy(Enum):
    """Arbitration policies for router conflicts."""

    ROUND_ROBIN = "round_robin"
    PRIORITY = "priority"
    FIFO = "fifo"


class Arbiter:
    """Handles arbitration between competing packets."""

    def __init__(self, policy: ArbitrationPolicy = ArbitrationPolicy.ROUND_ROBIN):
        self.policy = policy
        self.last_winner = 0
        self.priority_table = {}

    def arbitrate(self, request_list: List[int]) -> int:
        """
        Arbitrate between multiple requests.

        Args:
            request_list: List of requesting tile IDs

        Returns:
            Winning tile ID
        """
        if not request_list:
            return -1

        if self.policy == ArbitrationPolicy.ROUND_ROBIN:
            return self._round_robin(request_list)
        elif self.policy == ArbitrationPolicy.PRIORITY:
            return self._priority(request_list)
        elif self.policy == ArbitrationPolicy.FIFO:
            return request_list[0]
        else:
            return request_list[0]

    def _round_robin(self, request_list: List[int]) -> int:
        """Round-robin arbitration."""
        idx = (self.last_winner + 1) % len(request_list)
        winner = request_list[idx]
        self.last_winner = idx
        return winner

    def _priority(self, request_list: List[int]) -> int:
        """Priority-based arbitration."""
        # Higher tile ID = higher priority (simplified)
        return max(request_list)

    def set_priority(self, tile_id: int, priority: int):
        """Set priority for tile."""
        self.priority_table[tile_id] = priority

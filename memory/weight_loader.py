"""
Weight loader for programming crossbar arrays.
"""

import numpy as np
from typing import Optional


class WeightLoader:
    """Handles weight programming to tiles."""

    def __init__(self, num_tiles: int, tile_size: int):
        self.num_tiles = num_tiles
        self.tile_size = tile_size
        self.loaded_weights = {}

    def load_weights(self, tile_id: int, weights: np.ndarray) -> bool:
        """
        Load weights for tile.

        Args:
            tile_id: Target tile
            weights: Weight matrix

        Returns:
            True if successful
        """
        if weights.shape != (self.tile_size, self.tile_size):
            return False

        self.loaded_weights[tile_id] = weights.copy()
        return True

    def get_weights(self, tile_id: int) -> Optional[np.ndarray]:
        """Retrieve loaded weights for tile."""
        return self.loaded_weights.get(tile_id)

    def partial_program(self, tile_id: int, weights: np.ndarray, row_start: int, col_start: int) -> bool:
        """
        Partially program weights (region update).

        Args:
            tile_id: Target tile
            weights: Partial weight matrix
            row_start: Starting row
            col_start: Starting column

        Returns:
            True if successful
        """
        if tile_id not in self.loaded_weights:
            self.loaded_weights[tile_id] = np.zeros((self.tile_size, self.tile_size))

        rows, cols = weights.shape
        self.loaded_weights[tile_id][
            row_start : row_start + rows,
            col_start : col_start + cols
        ] = weights

        return True

    def verify_loaded(self, tile_id: int, expected: np.ndarray) -> bool:
        """Verify loaded weights match expected."""
        if tile_id not in self.loaded_weights:
            return False
        return np.allclose(self.loaded_weights[tile_id], expected)

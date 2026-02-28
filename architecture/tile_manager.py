"""
Tile manager for multi-tile coordination.
"""

import numpy as np
from typing import List
from architecture.neuratile import NeuraTile
from device_layer.base_device import DeviceModel


class TileManager:
    """Manages multiple NeuraTiles."""

    def __init__(self, num_tiles: int, tile_size: int, device_model: DeviceModel):
        """
        Args:
            num_tiles: Number of tiles
            tile_size: Size of each tile (tile_size x tile_size)
            device_model: Device model for all tiles
        """
        self.num_tiles = num_tiles
        self.tile_size = tile_size
        self.tiles = [
            NeuraTile(tile_id=i, size=tile_size, device_model=device_model)
            for i in range(num_tiles)
        ]

    def program_tile(self, tile_id: int, weights: np.ndarray):
        """
        Program weights into specific tile.

        Args:
            tile_id: Target tile
            weights: Weight matrix
        """
        if tile_id >= self.num_tiles:
            raise ValueError(f"Tile {tile_id} out of range")
        self.tiles[tile_id].program_weights(weights)

    def execute(self, tile_id: int, inputs: np.ndarray, dt: float = 1.0) -> np.ndarray:
        """
        Execute computation on tile.

        Args:
            tile_id: Target tile
            inputs: Input vector
            dt: Time step

        Returns:
            Spike output
        """
        return self.tiles[tile_id].execute_layer(inputs, dt)

    def get_tile(self, tile_id: int) -> NeuraTile:
        """Get tile by ID."""
        return self.tiles[tile_id]

    def reset_all(self):
        """Reset all tiles."""
        for tile in self.tiles:
            tile.reset()

    def get_power_summary(self) -> dict:
        """Get power consumption across all tiles."""
        total_energy = sum(tile.power_monitor.get_total_energy() for tile in self.tiles)
        return {
            "total_energy": total_energy,
            "per_tile": [tile.power_monitor.get_total_energy() for tile in self.tiles],
        }

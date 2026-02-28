"""
Tile-local buffer for on-chip data storage.
"""

import numpy as np


class TileBuffer:
    """Local buffer on each tile."""

    def __init__(self, tile_id: int, size_kB: int = 16):
        """
        Args:
            tile_id: Tile identifier
            size_kB: Buffer size in kilobytes
        """
        self.tile_id = tile_id
        self.size_bytes = size_kB * 1024
        self.buffer = np.zeros(self.size_bytes, dtype=np.uint8)
        self.write_ptr = 0
        self.read_ptr = 0
        self.occupancy = 0

    def write(self, data: np.ndarray) -> bool:
        """
        Write data to buffer.

        Returns:
            True if successful, False if overflow
        """
        data_size = data.nbytes
        if self.occupancy + data_size > self.size_bytes:
            return False

        end_ptr = (self.write_ptr + data_size) % self.size_bytes
        if end_ptr >= self.write_ptr:
            self.buffer[self.write_ptr : end_ptr] = data.flat
        else:
            self.buffer[self.write_ptr :] = data.flat[: self.size_bytes - self.write_ptr]
            self.buffer[: end_ptr] = data.flat[self.size_bytes - self.write_ptr :]

        self.write_ptr = end_ptr
        self.occupancy += data_size
        return True

    def read(self, num_bytes: int) -> np.ndarray:
        """
        Read data from buffer.

        Returns:
            Data array
        """
        if num_bytes > self.occupancy:
            num_bytes = self.occupancy

        end_ptr = (self.read_ptr + num_bytes) % self.size_bytes
        if end_ptr >= self.read_ptr:
            data = self.buffer[self.read_ptr : end_ptr].copy()
        else:
            data = np.concatenate([
                self.buffer[self.read_ptr :],
                self.buffer[: end_ptr]
            ])

        self.read_ptr = end_ptr
        self.occupancy -= num_bytes
        return data

    def get_occupancy(self) -> float:
        """Return occupancy (0-1)."""
        return self.occupancy / self.size_bytes

    def clear(self):
        """Clear buffer."""
        self.write_ptr = 0
        self.read_ptr = 0
        self.occupancy = 0

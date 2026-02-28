"""
Mesh network topology for NeuraEdge multi-tile system.
"""

import numpy as np
from typing import Tuple, List


class MeshNetwork:
    """2D mesh network for tile interconnection."""

    def __init__(self, rows: int, cols: int):
        """
        Args:
            rows: Number of rows
            cols: Number of columns
        """
        self.rows = rows
        self.cols = cols
        self.num_tiles = rows * cols

    def get_tile_coordinates(self, tile_id: int) -> Tuple[int, int]:
        """Convert tile ID to (row, col)."""
        return (tile_id // self.cols, tile_id % self.cols)

    def get_tile_id(self, row: int, col: int) -> int:
        """Convert (row, col) to tile ID."""
        return row * self.cols + col

    def get_neighbors(self, tile_id: int) -> List[int]:
        """Get neighboring tile IDs (N, S, E, W)."""
        row, col = self.get_tile_coordinates(tile_id)
        neighbors = []

        # North
        if row > 0:
            neighbors.append(self.get_tile_id(row - 1, col))
        # South
        if row < self.rows - 1:
            neighbors.append(self.get_tile_id(row + 1, col))
        # East
        if col < self.cols - 1:
            neighbors.append(self.get_tile_id(row, col + 1))
        # West
        if col > 0:
            neighbors.append(self.get_tile_id(row, col - 1))

        return neighbors

    def manhattan_distance(self, tile_a: int, tile_b: int) -> int:
        """Calculate Manhattan distance between tiles."""
        row_a, col_a = self.get_tile_coordinates(tile_a)
        row_b, col_b = self.get_tile_coordinates(tile_b)
        return abs(row_a - row_b) + abs(col_a - col_b)

    def route_path(self, source: int, dest: int) -> List[int]:
        """
        Find path from source to destination (dimension-order routing).

        Args:
            source: Source tile ID
            dest: Destination tile ID

        Returns:
            Path as list of tile IDs
        """
        src_row, src_col = self.get_tile_coordinates(source)
        dst_row, dst_col = self.get_tile_coordinates(dest)

        path = [source]
        current = source

        # Route in row direction first, then column
        while src_row != dst_row:
            if src_row < dst_row:
                src_row += 1
                current = self.get_tile_id(src_row, src_col)
            else:
                src_row -= 1
                current = self.get_tile_id(src_row, src_col)
            path.append(current)

        while src_col != dst_col:
            if src_col < dst_col:
                src_col += 1
                current = self.get_tile_id(src_row, src_col)
            else:
                src_col -= 1
                current = self.get_tile_id(src_row, src_col)
            path.append(current)

        return path

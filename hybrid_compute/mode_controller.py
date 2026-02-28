"""
Mode controller for switching between dense and SNN modes.
"""

from enum import Enum
from hybrid_compute.dense_mode import DenseMode
from hybrid_compute.snn_mode import SNNMode
from architecture.tile_manager import TileManager
import numpy as np


class ComputeMode(Enum):
    """Compute mode options."""

    DENSE = "dense"
    SNN = "snn"
    HYBRID = "hybrid"


class ModeController:
    """Controls mode switching and execution."""

    def __init__(self, tile_manager: TileManager, num_layers: int, layer_sizes: list):
        """
        Args:
            tile_manager: TileManager instance
            num_layers: Number of neural network layers
            layer_sizes: Layer dimensions
        """
        self.tile_manager = tile_manager
        self.dense_mode = DenseMode(num_layers, layer_sizes)
        self.snn_mode = SNNMode(tile_manager)
        self.current_mode = ComputeMode.SNN
        self.mode_switches = 0

    def switch_mode(self, mode: ComputeMode):
        """
        Switch execution mode.

        Args:
            mode: Target compute mode
        """
        self.current_mode = mode
        self.mode_switches += 1

    def forward(self, inputs: np.ndarray, tile_id: int = 0) -> np.ndarray:
        """
        Execute forward pass in current mode.

        Args:
            inputs: Input data
            tile_id: Target tile (for SNN mode)

        Returns:
            Output from current mode
        """
        if self.current_mode == ComputeMode.DENSE:
            return self.dense_mode.forward(inputs)
        elif self.current_mode == ComputeMode.SNN:
            return self.snn_mode.forward(inputs, tile_id)
        else:  # HYBRID
            # Hybrid: use SNN for sparse, Dense for dense
            sparsity = np.count_nonzero(inputs) / len(inputs.flat)
            if sparsity < 0.1:
                return self.snn_mode.forward(inputs, tile_id)
            else:
                return self.dense_mode.forward(inputs)

    def get_mode_statistics(self) -> dict:
        """Get mode switching statistics."""
        return {
            "current_mode": self.current_mode.value,
            "mode_switches": self.mode_switches,
        }

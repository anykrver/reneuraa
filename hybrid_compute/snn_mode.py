"""
Spiking Neural Network (SNN) mode.
"""

import numpy as np
from architecture.neuratile import NeuraTile
from architecture.tile_manager import TileManager


class SNNMode:
    """Spiking neural network inference mode."""

    def __init__(self, tile_manager: TileManager):
        """
        Args:
            tile_manager: TileManager instance
        """
        self.tile_manager = tile_manager
        self.timesteps = 100  # Default simulation timesteps
        self.spike_history = []

    def forward(self, inputs: np.ndarray, tile_id: int = 0, timesteps: int = None) -> np.ndarray:
        """
        Forward pass through SNN.

        Args:
            inputs: Input spike train (timesteps, neurons) or (neurons,)
            tile_id: Target tile
            timesteps: Number of simulation timesteps

        Returns:
            Spike output statistics
        """
        if timesteps is None:
            timesteps = self.timesteps

        spike_counts = np.zeros(self.tile_manager.tile_size)

        # Ensure inputs are (timesteps, neurons)
        if inputs.ndim == 1:
            inputs = np.tile(inputs, (timesteps, 1))
        elif inputs.shape[0] != timesteps:
            # Truncate or pad inputs to match timesteps
            if inputs.shape[0] > timesteps:
                inputs = inputs[:timesteps]
            else:
                padding = np.zeros((timesteps - inputs.shape[0], inputs.shape[1]))
                inputs = np.vstack([inputs, padding])

        # Simulate SNN
        for t in range(timesteps):
            input_vec = inputs[t]
            spikes = self.tile_manager.execute(tile_id, input_vec, dt=1.0)
            if isinstance(spikes, np.ndarray):
                spike_counts[spikes] += 1

        return spike_counts

    def set_timesteps(self, timesteps: int):
        """Set default simulation timesteps."""
        self.timesteps = timesteps

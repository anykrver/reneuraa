"""
Analog MAC (multiply-accumulate) for dense computation.
"""

import numpy as np


class AnalogMAC:
    """Analog MAC using crossbar + ADC/DAC."""

    def __init__(self, matrix_size: int):
        self.matrix_size = matrix_size
        self.weights = np.zeros((matrix_size, matrix_size))

    def program_weights(self, weights: np.ndarray):
        """Program weight matrix."""
        self.weights = weights.copy()

    def compute(self, inputs: np.ndarray) -> np.ndarray:
        """
        Analog MAC computation.

        Args:
            inputs: Input vector

        Returns:
            Output vector (matrix @ inputs)
        """
        return self.weights @ inputs

    def compute_batch(self, inputs: np.ndarray) -> np.ndarray:
        """
        Batch MAC computation.

        Args:
            inputs: Batch of input vectors (batch_size, matrix_size)

        Returns:
            Batch of outputs
        """
        return inputs @ self.weights.T

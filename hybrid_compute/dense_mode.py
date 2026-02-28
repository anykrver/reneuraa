"""
Dense inference mode (standard neural network).
"""

import numpy as np


class DenseMode:
    """Dense neural network inference mode."""

    def __init__(self, num_layers: int, layer_sizes: list):
        """
        Args:
            num_layers: Number of layers
            layer_sizes: Layer dimensions
        """
        self.num_layers = num_layers
        self.layer_sizes = layer_sizes
        self.weights = [np.zeros((layer_sizes[i], layer_sizes[i + 1]))
                       for i in range(num_layers - 1)]
        self.biases = [np.zeros(size) for size in layer_sizes[1:]]

    def forward(self, inputs: np.ndarray) -> np.ndarray:
        """
        Forward pass through dense network.

        Args:
            inputs: Input vector

        Returns:
            Output vector
        """
        activations = inputs
        for i, (w, b) in enumerate(zip(self.weights, self.biases)):
            activations = w.T @ activations + b
            # ReLU activation (except last layer)
            if i < len(self.weights) - 1:
                activations = np.maximum(activations, 0)
        return activations

    def set_weights(self, layer_idx: int, weights: np.ndarray):
        """Set weights for layer."""
        self.weights[layer_idx] = weights.copy()

    def set_biases(self, layer_idx: int, biases: np.ndarray):
        """Set biases for layer."""
        self.biases[layer_idx] = biases.copy()

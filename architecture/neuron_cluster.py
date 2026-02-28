"""
Neuron cluster for NeuraEdge tiles.
Contains array of LIF neurons and aggregates spike information.
"""

import numpy as np
from architecture.lif_neuron import LIFNeuron
from typing import List, Tuple


class NeuronCluster:
    """Cluster of LIF neurons (one per output line of crossbar)."""

    def __init__(self, size: int, threshold: float = 1.0):
        """
        Args:
            size: Number of neurons
            threshold: Spike threshold
        """
        self.size = size
        self.neurons = [LIFNeuron(threshold=threshold) for _ in range(size)]
        self.spike_buffer = []
        self.membrane_potentials = np.zeros(size)

    def integrate(self, input_currents: np.ndarray, dt: float = 1.0) -> List[int]:
        """
        Integrate input currents and generate spikes.

        Args:
            input_currents: Output from crossbar (size,)
            dt: Time step

        Returns:
            List of neuron indices that spiked
        """
        assert input_currents.shape == (self.size,)
        spikes = []

        for i in range(self.size):
            if self.neurons[i].integrate(input_currents[i], dt):
                spikes.append(i)

        # Update membrane potentials for monitoring
        self.membrane_potentials = np.array(
            [neuron.voltage for neuron in self.neurons]
        )

        return spikes

    def get_membrane_potentials(self) -> np.ndarray:
        """Return current membrane potentials."""
        return self.membrane_potentials.copy()

    def get_spike_counts(self) -> np.ndarray:
        """Return cumulative spike counts."""
        return np.array([neuron.spike_count for neuron in self.neurons])

    def reset(self):
        """Reset all neurons."""
        for neuron in self.neurons:
            neuron.reset()
        self.spike_buffer = []
        self.membrane_potentials = np.zeros(self.size)

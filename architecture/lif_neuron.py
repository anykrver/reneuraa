"""
LIF (Leaky Integrate-and-Fire) neuron model for NeuraEdge.
"""

import numpy as np


class LIFNeuron:
    """Leaky Integrate-and-Fire neuron."""

    def __init__(self, threshold: float = 1.0, tau_membrane: float = 20.0):
        """
        Args:
            threshold: Spike threshold voltage
            tau_membrane: Membrane time constant (ms)
        """
        self.threshold = threshold
        self.tau_membrane = tau_membrane
        self.voltage = 0.0
        self.is_refractory = False
        self.refractory_period = 2.0  # ms
        self.refractory_timer = 0.0
        self.spike_count = 0

    def integrate(self, input_current: float, dt: float = 1.0):
        """
        Integrate input current using Euler method.
        dV/dt = -(V - V_rest) / tau + I / C

        Args:
            input_current: Input current (sum of crossbar outputs)
            dt: Time step (ms)
        """
        if self.is_refractory:
            self.refractory_timer -= dt
            if self.refractory_timer <= 0:
                self.is_refractory = False
            self.voltage = 0.0
            return False

        # Leaky integration
        decay = np.exp(-dt / self.tau_membrane)
        self.voltage = self.voltage * decay + input_current * (1 - decay)

        # Check threshold
        if self.voltage >= self.threshold:
            self.voltage = 0.0
            self.is_refractory = True
            self.refractory_timer = self.refractory_period
            self.spike_count += 1
            return True

        return False

    def reset(self):
        """Reset neuron state."""
        self.voltage = 0.0
        self.is_refractory = False
        self.refractory_timer = 0.0
        self.spike_count = 0

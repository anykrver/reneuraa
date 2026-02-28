"""
Noise models for device variation and reliability analysis.
"""

import numpy as np
from typing import Callable


class GaussianNoise:
    """Gaussian noise model."""

    def __init__(self, std_dev: float):
        self.std_dev = std_dev

    def sample(self) -> float:
        return np.random.normal(0, self.std_dev)


class LogNormalNoise:
    """Log-normal noise model (realistic for PCM/ReRAM)."""

    def __init__(self, sigma: float):
        self.sigma = sigma

    def sample(self) -> float:
        return np.random.lognormal(0, self.sigma) - 1.0


class RandomTelegraphNoise:
    """RTN: random two-level fluctuations."""

    def __init__(self, amplitude: float, frequency: float):
        self.amplitude = amplitude
        self.frequency = frequency
        self.state = np.random.choice([-1, 1])

    def sample(self) -> float:
        if np.random.rand() < self.frequency:
            self.state = -self.state
        return self.amplitude * self.state


class StuckAtFault:
    """Stuck-at fault generator for reliability testing."""

    def __init__(self, fault_rate: float):
        self.fault_rate = fault_rate
        self.is_faulty = np.random.rand() < fault_rate
        self.stuck_value = np.random.choice([-1, 1]) if self.is_faulty else 0

    def apply(self, value: float) -> float:
        if self.is_faulty:
            return self.stuck_value
        return value

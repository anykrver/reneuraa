"""
Drift models for temporal degradation of memristive devices.
"""

import numpy as np


class ConductanceDrift:
    """Time-dependent conductance decay (ReRAM/PCM)."""

    def __init__(self, drift_coefficient: float):
        self.drift_coefficient = drift_coefficient
        self.accumulated_drift = 0.0

    def update(self, time_elapsed: float, current_conductance: float) -> float:
        """
        Calculate drift effect over time.
        Returns: conductance after drift
        """
        drift = current_conductance * self.drift_coefficient * (time_elapsed / 1000)
        self.accumulated_drift += drift
        return -drift


class TemperatureDrift:
    """Temperature-dependent drift (PCM more sensitive)."""

    def __init__(self, temp_coefficient: float = 0.001):
        self.temp_coefficient = temp_coefficient

    def apply(self, conductance: float, temperature: float) -> float:
        """Apply temperature-dependent drift."""
        delta_t = temperature - 25.0  # Reference 25C
        return conductance * (1 - self.temp_coefficient * delta_t / 100)


class MultiLevelCellDegradation:
    """Degradation specific to MLC operation."""

    def __init__(self, degradation_rate: float):
        self.degradation_rate = degradation_rate
        self.cycle_count = 0

    def increment_cycle(self):
        self.cycle_count += 1

    def get_degradation_factor(self) -> float:
        """Return conductance degradation factor (multiplier < 1)."""
        return 1.0 - (self.degradation_rate * self.cycle_count)

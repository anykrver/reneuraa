"""
SRAM fallback model for NeuraEdge.
Used when ReRAM/PCM unavailable or for comparison.
"""

from device_layer.base_device import DeviceModel
import numpy as np


class SRAMFallbackModel(DeviceModel):
    """Ideal SRAM device model (minimal noise/drift)."""

    def __init__(self, max_conductance: float = 1e-4, min_conductance: float = 1e-6):
        super().__init__("SRAM")
        self.max_conductance = max_conductance
        self.min_conductance = min_conductance
        self.current_conductance = (max_conductance + min_conductance) / 2
        self.noise_std = 0.001  # Much lower noise
        self.drift_coefficient = 0.0001  # Negligible drift

    def program(self, conductance: float) -> float:
        """Program with minimal variation."""
        target = np.clip(conductance, self.min_conductance, self.max_conductance)
        variation = np.random.normal(0, self.noise_std * target)
        self.current_conductance = np.clip(target + variation,
                                          self.min_conductance,
                                          self.max_conductance)
        return self.current_conductance

    def read(self, voltage: float) -> float:
        """Ideal linear Ohmic behavior."""
        return self.current_conductance * voltage

    def update_drift(self, time_elapsed: float):
        """SRAM has negligible drift."""
        pass

    def inject_noise(self) -> float:
        """Return minimal noise."""
        return np.random.normal(0, self.noise_std * self.current_conductance)

"""
PCM (Phase Change Memory) device model for NeuraEdge.
Implements chalcogenide glass conductance dynamics.
"""

from device_layer.base_device import DeviceModel
import numpy as np


class PCMModel(DeviceModel):
    """Phase Change Memory device model."""

    def __init__(self, max_conductance: float = 1e-4, min_conductance: float = 1e-6):
        super().__init__("PCM")
        self.max_conductance = max_conductance
        self.min_conductance = min_conductance
        self.current_conductance = (max_conductance + min_conductance) / 2
        self.drift_coefficient = 0.05
        self.noise_std = 0.03
        self.crystallinity = 0.5

    def program(self, conductance: float) -> float:
        """Program to target conductance with PCM-specific variation."""
        target = np.clip(conductance, self.min_conductance, self.max_conductance)
        variation = np.random.normal(0, self.noise_std * target)
        self.current_conductance = np.clip(target + variation,
                                          self.min_conductance,
                                          self.max_conductance)
        return self.current_conductance

    def read(self, voltage: float) -> float:
        """Conductance-dependent I-V with temperature effects."""
        base_current = self.current_conductance * voltage
        return base_current

    def update_drift(self, time_elapsed: float):
        """PCM has stronger drift than ReRAM."""
        drift = self.current_conductance * self.drift_coefficient * (time_elapsed / 1000)
        self.current_conductance = np.clip(self.current_conductance - drift,
                                          self.min_conductance,
                                          self.max_conductance)

    def inject_noise(self) -> float:
        """Return log-normal noise (more realistic for PCM)."""
        return np.random.lognormal(0, self.noise_std * 0.5) - 1.0

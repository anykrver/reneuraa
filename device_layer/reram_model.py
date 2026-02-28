"""
ReRAM (Resistive RAM) device model for NeuraEdge.
Implements conductive filament dynamics and nonlinear I-V behavior.
"""

from device_layer.base_device import DeviceModel
import numpy as np


class ReRAMModel(DeviceModel):
    """Resistive RAM device model."""

    def __init__(self, max_conductance: float = 1e-4, min_conductance: float = 1e-6):
        super().__init__("ReRAM")
        self.max_conductance = max_conductance
        self.min_conductance = min_conductance
        self.current_conductance = (max_conductance + min_conductance) / 2
        self.drift_coefficient = 0.001
        self.noise_std = 0.02

    def program(self, conductance: float) -> float:
        """Program to target conductance with variation."""
        target = np.clip(conductance, self.min_conductance, self.max_conductance)
        # Add programming variation
        variation = np.random.normal(0, self.noise_std * target)
        self.current_conductance = np.clip(target + variation,
                                          self.min_conductance,
                                          self.max_conductance)
        return self.current_conductance

    def read(self, voltage: float) -> float:
        """Ohmic current: I = G * V + nonlinearity."""
        ohmic = self.current_conductance * voltage
        nonlinearity = 0.1 * (voltage ** 2) * self.current_conductance
        return ohmic + nonlinearity

    def update_drift(self, time_elapsed: float):
        """Simulate temporal drift (conductance decay)."""
        drift = self.current_conductance * self.drift_coefficient * (time_elapsed / 1000)
        self.current_conductance = np.clip(self.current_conductance - drift,
                                          self.min_conductance,
                                          self.max_conductance)

    def inject_noise(self) -> float:
        """Return Gaussian noise contribution."""
        return np.random.normal(0, self.noise_std * self.current_conductance)

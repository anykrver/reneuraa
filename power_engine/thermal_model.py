"""
Thermal model for temperature-dependent device behavior.
"""

import numpy as np


class ThermalModel:
    """Simplified thermal model."""

    def __init__(self, ambient_temp: float = 25.0, junction_to_ambient_resistance: float = 10.0):
        """
        Args:
            ambient_temp: Ambient temperature (°C)
            junction_to_ambient_resistance: Thermal resistance (°C/W)
        """
        self.ambient_temp = ambient_temp
        self.rja = junction_to_ambient_resistance
        self.junction_temp = ambient_temp
        self.power = 0.0

    def update(self, power_watts: float, time_step_seconds: float = 0.001):
        """
        Update junction temperature.

        Args:
            power_watts: Current power dissipation (W)
            time_step_seconds: Simulation time step
        """
        self.power = power_watts
        # Steady-state junction temperature
        steady_state_temp = self.ambient_temp + power_watts * self.rja
        # Simple RC thermal model
        tau_thermal = 0.1  # Thermal time constant (seconds)
        self.junction_temp += (steady_state_temp - self.junction_temp) * (
            1 - np.exp(-time_step_seconds / tau_thermal)
        )

    def get_temperature(self) -> float:
        """Return current junction temperature."""
        return self.junction_temp

    def get_temperature_coefficient(self, parameter: str = "conductance") -> float:
        """
        Get temperature coefficient for device parameter.

        Args:
            parameter: 'conductance', 'leakage', etc.

        Returns:
            Temperature coefficient (per °C)
        """
        temp_excess = self.junction_temp - 25.0
        if parameter == "conductance":
            return 1 - 0.001 * temp_excess  # -0.1% per °C
        elif parameter == "leakage":
            return 1 + 0.05 * temp_excess  # +5% per °C
        else:
            return 1.0

"""
Voltage scaling model for power management.
"""

import numpy as np


class VoltageModel:
    """Models voltage-dependent power and performance."""

    def __init__(self, nominal_voltage: float = 0.8):
        """
        Args:
            nominal_voltage: Nominal supply voltage (V)
        """
        self.nominal_voltage = nominal_voltage
        self.current_voltage = nominal_voltage

    def set_voltage(self, voltage: float):
        """Set supply voltage."""
        if voltage < 0.5:
            raise ValueError("Voltage too low")
        self.current_voltage = voltage

    def power_scaling_factor(self) -> float:
        """
        Power scales as V^2 for dynamic power, plus leakage.

        Returns:
            Power multiplier relative to nominal
        """
        v_ratio = self.current_voltage / self.nominal_voltage
        # P_dynamic ~ V^2, P_leakage ~ V (simplified)
        return 0.7 * (v_ratio ** 2) + 0.3 * v_ratio

    def frequency_scaling_factor(self) -> float:
        """
        Frequency scales approximately linearly with voltage (simplified).

        Returns:
            Frequency multiplier relative to nominal
        """
        v_ratio = self.current_voltage / self.nominal_voltage
        return max(v_ratio - 0.2, 0.5)  # Minimum 50% frequency

    def delay_scaling_factor(self) -> float:
        """
        Delay increases as voltage decreases.

        Returns:
            Delay multiplier (higher = slower)
        """
        return 1.0 / self.frequency_scaling_factor()

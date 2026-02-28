"""
Power estimator for real-time power tracking.
"""

import numpy as np
from power_engine.energy_model import EnergyModel


class PowerEstimator:
    """Real-time power consumption estimator."""

    def __init__(self, energy_model: EnergyModel = None):
        self.energy_model = energy_model or EnergyModel()
        self.measurements = []
        self.current_power = 0.0

    def estimate_power(
        self,
        activity_rate: float,
        matrix_size: int,
        spike_rate: float,
        frequency_mhz: float = 100.0
    ) -> float:
        """
        Estimate instantaneous power.

        Args:
            activity_rate: Fraction of crossbar active (0-1)
            matrix_size: Crossbar size
            spike_rate: Fraction of neurons spiking (0-1)
            frequency_mhz: Clock frequency

        Returns:
            Power estimate (mW)
        """
        # Operations per cycle
        ops_dac = matrix_size * activity_rate * frequency_mhz / 1000
        ops_adc = matrix_size * activity_rate * frequency_mhz / 1000
        num_spikes = matrix_size * spike_rate

        # Energy per cycle
        energy_cycle = self.energy_model.total_energy(
            num_inputs=matrix_size,
            num_outputs=matrix_size,
            matrix_size=matrix_size,
            num_reads=int(activity_rate * matrix_size),
            num_spikes=int(num_spikes)
        )

        # Power = Energy * Frequency
        power_mw = energy_cycle * (frequency_mhz / 1000) / 1000  # Convert pJ to mW

        self.current_power = power_mw
        self.measurements.append(power_mw)

        return power_mw

    def get_average_power(self) -> float:
        """Return average measured power."""
        if not self.measurements:
            return 0.0
        return np.mean(self.measurements)

    def get_peak_power(self) -> float:
        """Return peak measured power."""
        if not self.measurements:
            return 0.0
        return np.max(self.measurements)

    def reset(self):
        """Reset measurements."""
        self.measurements = []
        self.current_power = 0.0
